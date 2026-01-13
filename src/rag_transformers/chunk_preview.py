"""the file is intended to divide the text into 
    chunks and save them in data/chunks in the jsonl format"""

from langchain_text_splitters import RecursiveCharacterTextSplitter
from pathlib import Path
import json

#path
processed_data_path = "/home/kuba/RAG/rag-systems/data/processed_data"
chunks_path = "/home/kuba/RAG/rag-systems/data/chunks"

input_dir = Path(processed_data_path)
output_dir = Path(chunks_path)

#Parameters
CHUNK_SIZE = 2500
CHUNK_OVERLAP = 250

#id txt file
id_txt = [
    "1706.03762",
    "1803.02155",
    "1810.04805",
    "1901.02860",
    "2006.03654",
    "2009.06732",
    "2004.05150",
]

#RCTS splitter
splitter =  RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
)


counter = 0
for paper_id in id_txt:
    input_path_txt = input_dir / f"{paper_id}.txt"
    output_path_jsonl = output_dir / f"{paper_id}.jsonl"

    if not input_path_txt.exists():
        print(f"[file skipping id {id}], there is no file in this location {input_path_txt}")
        continue

    text = input_path_txt.read_text(encoding="utf-8")

    chunks = splitter.split_text(text)

    counter += 1
    print(f"Text nr {counter} | number of chunks: {len(chunks)}")

    with output_path_jsonl.open("w", encoding="utf-8") as f:
        for chunk_id, chunk_text in enumerate(chunks):
            record = {
                "paper_id": paper_id,
                "chunk_id": chunk_id,
                "text": chunk_text,
            }
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    
    print(f"File {paper_id} has been saved in {output_dir}")
