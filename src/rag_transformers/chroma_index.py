import json
from pathlib import Path
import chromadb

EMBEDDING_DIR = Path("/home/kuba/rag-systems/data/embeddings")
CHROMA_DIR = Path("/home/kuba/rag-systems/data/chroma")
CHROMA_DIR.mkdir(parents=True, exist_ok=True)
COLLECTION_NAME = "transformers_papers"

client = chromadb.PersistentClient(path=CHROMA_DIR)
collection = client.get_or_create_collection(name=COLLECTION_NAME) 

counter = 0

for emb_file in EMBEDDING_DIR.glob("*.jsonl"):
    read_file = emb_file.open("r", encoding="utf-8")

    for line in read_file:
        record = json.loads(line)

        doc_id = f"{record["paper_id"]}_{record["chunk_id"]}"
        collection.add(
            ids=[doc_id],
            documents=[record["text"]],
            embeddings=[record["embedding"]],
            metadatas=[{"paper_id": record["paper_id"],
                        "chunk_id": record["chunk_id"]}]
        )   
        counter += 1
print(f"Index records: {counter}")
print(f"Chroma directory: {CHROMA_DIR}")
print(f"Collection: {COLLECTION_NAME}")