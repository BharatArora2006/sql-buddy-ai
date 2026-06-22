from app.rag.retriever import retrieve_context
from app.rag.prompt_builder import build_prompt
from app.llm.groq_client import generate_sql

from app.sql.validator import validate_sql
from app.sql.executor import execute_sql


question = "Show Term employees receiving verified payments"

print("\nQUESTION:")
print(question)

result = retrieve_context(question)

documents = result["documents"][0]

print("\nRETRIEVED DOCUMENTS:")

for doc in documents:

    print("=" * 80)
    print(doc)

prompt = build_prompt(
    question,
    documents
)

print("\nPROMPT:")
print(prompt)

sql = generate_sql(prompt)

print("\nGENERATED SQL:")
print(sql)

print("\nCLEAN SQL:")
print(sql)

validate_sql(sql)

results = execute_sql(sql)

print("\nRESULTS:")
print(results[:10])

