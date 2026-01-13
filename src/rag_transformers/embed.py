import json
from pathlib import Path
from openai import OpenAI

paper_id = "1706.03762"
jsonl_path = Path(f"/home/kuba/rag-systems/data/chunks/{paper_id}.jsonl")

if not jsonl_path.exists():
    raise FileNotFoundError(f"File not exist: {jsonl_path}")

first_line = jsonl_path.open("r", encoding="utf-8").readline()
record = json.loads(first_line)

text = record["text"]

client = OpenAI()

response = client.embeddings.create(
    model="text-embedding-3-small",
    input=text
)

embedding = response.data[0].embedding

print("paper_id", record["paper_id"])
print("chunk_id", record["chunk_id"])
print(f"text lenght: {len(text)}")
print(f"embedding lenght: {len(embedding)}")
print(f"first 5 values {embedding[:5]}")
