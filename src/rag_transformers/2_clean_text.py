"""Script for cleaning txt, remove white spaces, blank lines
    and save final text"""

from pathlib import Path
import re

#path
METADATA_DIR = Path("/home/kuba/rag-systems/data/metadata")
PROCESSED_DIR = Path("/home/kuba/rag-systems/data/processed_data")
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

#Cleaning txt
for paper in METADATA_DIR.glob("*.txt"):
    paper_id = paper.stem
    out_file = PROCESSED_DIR / f"{paper_id}.txt"

    if not paper.exists():
        raise FileNotFoundError(f"File was not found: {METADATA_DIR / f'{paper_id}.txt'}")
    
    if out_file.exists():
        print(f"File {paper_id} was saved before ", out_file)
        continue
    
    print(f"Cleaning: {paper_id}")

    text = paper.read_text(encoding="utf-8")

    #Replace multiple spaces with a single space
    text = re.sub(r"[ \t]+", " ", text)

    #Remove blank lines
    text = re.sub(r"\n\s*\n+", "\n\n", text)

    #Trim whitespaces
    text = text.strip()

    out_file.write_text(text, encoding="utf-8")

    print(f"PDF nr {paper_id}, Saved cleaned: {out_file}")
    