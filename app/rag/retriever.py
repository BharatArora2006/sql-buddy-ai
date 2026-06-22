# app/rag/retriever.py

from chromadb import PersistentClient


client = PersistentClient(
    path="./chroma_db"
)

collection = client.get_collection(
    "enterprise_sql_metadata"
)


def retrieve_context(question):

    results = collection.query(
        query_texts=[question],
        n_results=5
    )

    return results

if __name__ == "__main__":

    result = retrieve_context(
        "Show active employees receiving payments"
    )

    print("\nDOCUMENTS RETRIEVED:\n")

    for doc in result["documents"][0]:

        print("=" * 80)
        print(doc)