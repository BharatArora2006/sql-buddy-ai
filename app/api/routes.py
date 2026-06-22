from fastapi import APIRouter

from app.schemas.question import QuestionRequest

from app.rag.retriever import retrieve_context
from app.rag.prompt_builder import build_prompt

from app.llm.groq_client import generate_sql

from app.sql.sql_cleaner import clean_sql
from app.sql.validator import validate_sql
from app.sql.executor import execute_sql


router = APIRouter()


@router.post("/ask")
def ask_question(request: QuestionRequest):

    result = retrieve_context(
        request.question
    )

    documents = result["documents"][0]

    prompt = build_prompt(
        request.question,
        documents
    )

    sql = generate_sql(prompt)

    sql = clean_sql(sql)

    validate_sql(sql)

    results = execute_sql(sql)

    return {
        "question": request.question,
        "generated_sql": sql,
        "results": results[:50]
    }