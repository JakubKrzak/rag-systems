import json
from pathlib import Path
from openai import OpenAI

client = OpenAI()

INPUT_DIR = Path(f"/home/kuba/rag-systems/data/chunks")
OUTPUT_DIR = Path(f"/home/kuba/rag-systems/data/embeddings")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

for chunks_file in INPUT_DIR.glob("*.jsonl"):
    paper_id = chunks_file.stem
    out_file = OUTPUT_DIR / f"{paper_id}.jsonl"

    if not chunks_file.exists():
        raise FileNotFoundError(f"File doesnt exist: {INPUT_DIR / paper_id}")
    
    #Open directory
    read_file = chunks_file.open("r", encoding="utf-8")
    write_file = out_file.open("w", encoding="utf-8")
    
    #embedding through the entire file
    for line in read_file:
        record = json.loads(line)
        text = record["text"]

        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        embedding = response.data[0].embedding

        final_record = {
            "paper_id": record["paper_id"],
            "chunk_id": record["chunk_id"],
            "text": text,
            "embedding": embedding,
        }

        write_file.write(
            json.dumps(final_record, ensure_ascii=False) + "\n"
        )

    read_file.close()
    write_file.close()

    print(f"File saved: {out_file}")
