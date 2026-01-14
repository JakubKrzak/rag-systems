"""the file is intended to divide the text into 
    chunks and save them in data/chunks in the jsonl format"""

from langchain_text_splitters import RecursiveCharacterTextSplitter
from pathlib import Path
import json

#path
PROCESSED_DIR = Path("/home/kuba/rag-systems/data/processed_data")
CHUNKS_DIR = Path("/home/kuba/rag-systems/data/chunks")
CHUNKS_DIR.mkdir(parents=True, exist_ok=True)

#Parameters
CHUNK_SIZE = 2500
CHUNK_OVERLAP = 250

#RCTS splitter
splitter =  RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
)

for paper in PROCESSED_DIR.glob("*.txt"):
    paper_id = paper.stem
    out_file = CHUNKS_DIR / f"{paper_id}.jsonl"

    if not paper.exists():
        raise FileNotFoundError(f"File doesnt exist: {PROCESSED_DIR / f'{paper_id}.txt'}")

    if out_file.exists():
        print(f"File {paper_id} was saved before ", out_file)
        continue

    text = paper.read_text(encoding="utf-8")

    chunks = splitter.split_text(text)

    print(f"Text nr {paper_id} | number of chunks: {len(chunks)}")

    write_file = out_file.open("w", encoding="utf-8")

    for chunk_id, chunk_text in enumerate(chunks):
        record = {
            "paper_id": paper_id,
            "chunk_id": chunk_id,
            "text": chunk_text,
        }
        write_file.write(json.dumps(record, ensure_ascii=False) + "\n")
    
    print(f"File {paper_id} has been saved in {out_file}")
