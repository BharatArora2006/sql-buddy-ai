import json
import os

from chromadb import PersistentClient

from app.rag.chunker import chunk_table_metadata


client = PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection(
    name="enterprise_sql_metadata"
)

METADATA_FOLDER = "metadata"

doc_id = 1


for filename in os.listdir(METADATA_FOLDER):

    if not filename.endswith(".json"):
        continue

    print(f"Opening {filename}")

    filepath = os.path.join(
        METADATA_FOLDER,
        filename
    )

    with open(filepath, "r") as f:

        data = json.load(f)

    print(f"Loaded {filename}")

    chunks = chunk_table_metadata(data)

    for chunk in chunks:

        collection.add(
            documents=[chunk],
            ids=[str(doc_id)],
            metadatas=[
                {
                    "source": filename,
                    "type": filename.replace(".json", "")
                }
            ]
        )

        print(
            f"Stored chunk {doc_id} from {filename}"
        )

        doc_id += 1

print("\nMetadata ingestion complete")