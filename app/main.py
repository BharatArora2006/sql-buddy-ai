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

def get_kpis(db):

    total_queries = (
        db.query(QueryHistory)
        .count()
    )

    total_rows = (
        db.query(
            func.sum(QueryHistory.row_count)
        )
        .scalar()
    ) or 0

    avg_runtime = (
        db.query(
            func.avg(QueryHistory.execution_time_ms)
        )
        .scalar()
    ) or 0

    today = datetime.utcnow().date()

    queries_today = (
        db.query(QueryHistory)
        .filter(
            func.date(QueryHistory.created_at)
            == today
        )
        .count()
    )

    return {
        "total_queries": total_queries,
        "total_rows": total_rows,
        "avg_runtime": round(avg_runtime, 2),
        "queries_today": queries_today
    }

@app.on_event("startup")
def startup():

    Base.metadata.create_all(bind=engine)


@app.get("/")
def health_check():

    return {
        "message": "SQL Buddy Running"
    }

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
            **kpis
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

        prompt = build_prompt(
            question,
            documents
        )

        sql = generate_sql(prompt)

        logger.info(f"Question: {question}")
        logger.info(f"Generated SQL: {sql}")

        review = review_sql(sql)

        validate_sql(sql)

        # START TIMER
        start_time = time.time()

        results = execute_sql(
            sql
        )

        # STOP TIMER
        execution_time_ms = int(
            (time.time() - start_time) * 1000
        )
        row_count = len(results)

        db = SessionLocal()

        history = QueryHistory(
            question=question,
            generated_sql=sql,
            row_count=row_count,
            execution_time_ms=execution_time_ms
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
                **kpis
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
            **kpis
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