from fastapi import FastAPI
from fastapi import Request
from fastapi import Form

from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from sqlalchemy import func
from datetime import datetime

from app.database.database import engine
from app.database.database import Base

from app.database.models import *

from app.rag.retriever import retrieve_context
from app.rag.prompt_builder import build_prompt

from app.llm.groq_client import generate_sql

from app.sql.validator import validate_sql
from app.sql.executor import execute_sql
from app.sql.review import review_sql

from app.utils.query_cache import last_results

import time
from app.database.database import SessionLocal
from app.database.models import QueryHistory
from app.database.schema_validator import validate_schema


from app.utils.logger import logger


from fastapi.responses import StreamingResponse
import pandas as pd
import io


app = FastAPI(
    title="Enterprise SQL Assistant",
    version="1.0.0"
)


templates = Jinja2Templates(
    directory="app/templates"
)


app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static"
)

from sqlalchemy import func
from datetime import datetime

def get_kpis(db):

    total_queries = db.query(QueryHistory).count()

    total_rows = (
        db.query(func.sum(QueryHistory.row_count))
        .scalar()
    ) or 0

    avg_runtime = (
        db.query(func.avg(QueryHistory.execution_time_ms))
        .scalar()
    ) or 0

    today = datetime.utcnow().date()

    queries_today = (
        db.query(QueryHistory)
        .filter(
            func.date(QueryHistory.created_at) == today
        )
        .count()
    )

    evaluated_queries = (
        db.query(QueryHistory)
        .filter(QueryHistory.response_time_ms != None)
        .count()
    )

    valid_sql = (
        db.query(QueryHistory)
        .filter(QueryHistory.is_valid_sql == True)
        .count()
    )

    successful_execution = (
        db.query(QueryHistory)
        .filter(QueryHistory.execution_success == True)
        .count()
    )

    hallucinations = (
        db.query(QueryHistory)
        .filter(QueryHistory.hallucination_detected == True)
        .count()
    )

    avg_llm_response_time = (
        db.query(func.avg(QueryHistory.response_time_ms))
        .scalar()
    ) or 0

    sql_validity_rate = (
        round((valid_sql / evaluated_queries) * 100, 2)
        if evaluated_queries else 0
    )

    execution_success_rate = (
        round((successful_execution / evaluated_queries) * 100, 2)
        if evaluated_queries else 0
    )

    hallucination_rate = (
        round((hallucinations / evaluated_queries) * 100, 2)
        if evaluated_queries else 0
    )

    return {

        "total_queries": total_queries,

        "total_rows": total_rows,

        "avg_runtime": round(avg_runtime, 2),

        "queries_today": queries_today,

        "evaluated_queries": evaluated_queries,

        "sql_validity_rate": sql_validity_rate,

        "execution_success_rate": execution_success_rate,

        "avg_llm_response_time": round(avg_llm_response_time, 2),

        "hallucination_rate": hallucination_rate

    }
@app.on_event("startup")
def startup():

    Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return RedirectResponse(
        url="/dashboard",
        status_code=302
    )

@app.get("/dashboard")
def dashboard(request: Request):

    db = SessionLocal()

    recent_queries = (
        db.query(QueryHistory)
        .order_by(QueryHistory.id.desc())
        .limit(10)
        .all()
    )

    # KPIs
    kpis = get_kpis(db)
    llm_metrics = get_llm_metrics(db)

    db.close()

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "question": "",
            "generated_sql": "",
            "results": [],
            "review": [],
            "sql_error": "",
            "metadata_docs": [],
            "recent_queries": recent_queries,

            # KPI Cards
            **kpis,
            **llm_metrics
        }
    )

@app.get("/download-csv")
def download_csv():

    if not last_results:

        return {
            "message": "No results available"
        }

    df = pd.DataFrame(last_results)

    output = io.StringIO()

    df.to_csv(
        output,
        index=False
    )

    output.seek(0)

    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={
            "Content-Disposition":
            "attachment; filename=query_results.csv"
        }
    )

@app.post("/ask-ui")
def ask_ui(
    request: Request,
    question: str = Form(...)
):

    question = question.strip()
    response_time_ms = 0
    execution_time_ms = 0

    if not question:

        return templates.TemplateResponse(
            request=request,
            name="dashboard.html",
            context={
                "question": "",
                "generated_sql": "Please enter a question.",
                "review": review,
                "results": [],
                "sql_error": "",
                "metadata_docs": []
            }
        )

    try:

        result = retrieve_context(
            question
        )

        documents = result["documents"][0]

        # print("\n========== DOCUMENTS ==========\n")

        # for i, doc in enumerate(documents):

        #     print(f"Document {i+1}")

        #     print(doc)

        #     print("--------------------------------")

        prompt = build_prompt(
            question,
            documents
        )

        start_time = time.time()

        sql = generate_sql(prompt)
        response_time_ms = int((time.time() - start_time) * 1000)
        # print("######## LLM RESPONSE TIME ########", response_time_ms)

        hallucination_result = validate_schema(sql)
        # print("Hallucination Result:", hallucination_result)

        logger.info(f"Hallucination Result: {hallucination_result}")
        hallucination_detected = hallucination_result["hallucination"]
        hallucination_score = hallucination_result["score"]
        hallucinated_objects = hallucination_result["objects"]
      

        if hallucination_detected:

            db = SessionLocal()

            history = QueryHistory(

                question=question,

                generated_sql=sql,

                row_count=0,

                execution_time_ms=0,

                response_time_ms=response_time_ms,

                is_valid_sql=False,

                execution_success=False,

                hallucination_detected=True
            )

            db.add(history)
            db.commit()
            
            recent_queries = (

                db.query(QueryHistory)

                .order_by(QueryHistory.id.desc())

                .limit(10)

                .all()

            )

            kpis = get_kpis(db)
            print("==========KPI===============",kpis)

            db.close()

            return templates.TemplateResponse(

                request=request,

                name="dashboard.html",

                context={

                    "question": question,

                    "generated_sql": sql,

                    "results": [],

                    "review": [

                        "❌ Schema Validation Failed"

                    ],

                    "sql_error":

                        "The generated SQL references objects that do not exist.<br><br>"

                        + "<br>".join(hallucinated_objects),

                    "metadata_docs": documents,

                    "recent_queries": recent_queries,

                    **kpis

                }

            )

        
        
        logger.info(f"Question: {question}")
        logger.info(f"Generated SQL: {sql}")

        review = review_sql(sql)

        is_valid_sql = False
        execution_success = False
        execution_time_ms = 0 

        try:

            validate_sql(sql)

            is_valid_sql = True

            # START TIMER
            start_time = time.time()

            results = execute_sql(
                sql
            )

            # STOP TIMER
            execution_time_ms = int(
                (time.time() - start_time) * 1000
            )
            execution_success = True
        except Exception as e:

            results = []

            execution_success = False

            logger.error(str(e))

        
        row_count = len(results)

        db = SessionLocal()

        history = QueryHistory(
            question=question,
            generated_sql=sql,
            row_count=row_count,
            execution_time_ms=execution_time_ms,

            is_valid_sql=is_valid_sql,
            execution_success=execution_success,
            response_time_ms=response_time_ms,

            hallucination_detected=hallucination_detected,
            hallucination_score=hallucination_score

        )

        db.add(history)
    
        db.commit()
   
        recent_queries = (
            db.query(QueryHistory)
            .order_by(QueryHistory.id.desc())
            .limit(10)
            .all()
        )
        
        db.close()


        last_results.clear()
        last_results.extend(results)

        db = SessionLocal()

        recent_queries = (
            db.query(QueryHistory)
            .order_by(QueryHistory.id.desc())
            .limit(10)
            .all()
        )

        kpis = get_kpis(db)
        llm_metrics = get_llm_metrics(db)

        db.close()

        return templates.TemplateResponse(
            request=request,
            name="dashboard.html",
            context={
                "question": question,
                "generated_sql": sql,
                "results": results,
                "review": review,
                "sql_error": "",
                "metadata_docs": documents,
                "recent_queries": recent_queries,
                
                # KPIs
                **kpis,
                **llm_metrics
                
            }
        )

    except Exception as e:

        db = SessionLocal()

        recent_queries = (
            db.query(QueryHistory)
            .order_by(QueryHistory.id.desc())
            .limit(10)
            .all()
        )

        kpis = get_kpis(db)

        db.close()

        return templates.TemplateResponse(
            request=request,
            name="dashboard.html",
            context={
                "question": question,
                "generated_sql": f"ERROR: {str(e)}",
                "results": [],
                "review": [
                    "❌ Query Failed"
                ],
                "sql_error": str(e),
                "metadata_docs": [],
                "recent_queries": [],
                # KPIs

                **kpis
            }
        )

@app.get("/rerun-query/{query_id}")
def rerun_query(
    query_id: int,
    request: Request
):
    db = SessionLocal()

    query_obj = (
        db.query(QueryHistory)
        .filter(
            QueryHistory.id == query_id
        )
        .first()
    )

    db.close()

    if not query_obj:

        db = SessionLocal()

        recent_queries = (
            db.query(QueryHistory)
            .order_by(QueryHistory.id.desc())
            .limit(10)
            .all()
        )

        kpis = get_kpis(db)

        return templates.TemplateResponse(
            request=request,
            name="dashboard.html",
            context={
                "question": "",
                "generated_sql": "Query not found",
                "results": [],
                "sql_error": "",
                "review": [],
                "metadata_docs": [],
                "recent_queries": [],
                
                # KPI Cards
                **kpis
            }
        )

  
    question = query_obj.question

    result = retrieve_context(question)

    documents = result["documents"][0]

    prompt = build_prompt(
        question,
        documents
    )

    sql = generate_sql(prompt)

    logger.info(f"Rerun Question: {question}")
    logger.info(f"Generated SQL: {sql}")

    validate_sql(sql)

    results = execute_sql(sql)

    review = review_sql(sql)

    db = SessionLocal()

    recent_queries = (
        db.query(QueryHistory)
        .order_by(
            QueryHistory.id.desc()
        )
        .limit(10)
        .all()
    )

    db.close()
    db = SessionLocal()

    recent_queries = (
        db.query(QueryHistory)
        .order_by(QueryHistory.id.desc())
        .limit(10)
        .all()
    )

    kpis = get_kpis(db)

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "question": question,
            "generated_sql": sql,
            "results": results,
            "sql_error": "",
            "review": review,
            "metadata_docs": documents,
            "recent_queries": recent_queries,

            # KPIs
            **kpis
        }
    )

@app.post("/execute-sql")
def execute_custom_sql(
    request: Request,
    edited_sql: str = Form(...),
    original_sql: str = Form(...)
):

    try:

        validate_sql(edited_sql)

        results = execute_sql(edited_sql)

        review = review_sql(edited_sql)

        sql_error = ""

    except Exception as e:

        results = []

        review = [
            "❌ SQL Execution Failed"
        ]

        logger.error(str(e))

        sql_error = (
            "Database execution failed. "
            "Please review the SQL and try again."
        )

    db = SessionLocal()

    recent_queries = (
        db.query(QueryHistory)
        .order_by(QueryHistory.id.desc())
        .limit(10)
        .all()
    )

    # KPI DATA
    kpis = get_kpis(db)
    llm_metrics = get_llm_metrics(db)

    db.close()

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "question": "",
            "generated_sql": original_sql,
            "edited_sql": edited_sql,
            "results": results,
            "review": review,
            "sql_error": sql_error,
            "metadata_docs": [],
            "recent_queries": recent_queries,

            # KPI Cards
            **kpis,
            **llm_metrics
        }
    )

@app.get("/about")
def about(
    request: Request
):

    return templates.TemplateResponse(
        request=request,
        name="about.html",
        context={}
    )

@app.get("/ask-ui")
def ask_ui_get():

    return RedirectResponse(
        url="/dashboard",
        status_code=302
    )

@app.get("/execute-sql")
def execute_sql_get():

    return RedirectResponse(
        url="/dashboard",
        status_code=302
    )


def get_llm_metrics(db):

    evaluated_queries = (
        db.query(QueryHistory)
        .filter(
            QueryHistory.response_time_ms.isnot(None)
        )
        .count()
    )

    if evaluated_queries == 0:

        return {
            "sql_validity_rate": 0,
            "execution_success_rate": 0,
            "avg_llm_response_time": 0,
            "hallucination_rate": 0,
            "evaluated_queries": 0
        }

    valid_queries = (
        db.query(QueryHistory)
        .filter(
            QueryHistory.is_valid_sql == True,
            QueryHistory.response_time_ms.isnot(None)
        )
        .count()
    )

    successful_queries = (
        db.query(QueryHistory)
        .filter(
            QueryHistory.execution_success == True,
            QueryHistory.response_time_ms.isnot(None)
        )
        .count()
    )

    hallucinated_queries = (
        db.query(QueryHistory)
        .filter(
            QueryHistory.hallucination_detected == True,
            QueryHistory.response_time_ms.isnot(None)
        )
        .count()
    )

    avg_response_time = (
        db.query(
            func.avg(
                QueryHistory.response_time_ms
            )
        )
        .filter(
            QueryHistory.response_time_ms.isnot(None)
        )
        .scalar()
    ) or 0

    return {

        "sql_validity_rate":
            round(
                (valid_queries / evaluated_queries) * 100,
                1
            ),

        "execution_success_rate":
            round(
                (successful_queries / evaluated_queries) * 100,
                1
            ),

        "avg_llm_response_time":
            round(avg_response_time),

        "hallucination_rate":
            round(
                (hallucinated_queries / evaluated_queries) * 100,
                1
            ),

        "evaluated_queries":
            evaluated_queries
    }