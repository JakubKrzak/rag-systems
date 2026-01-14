"""This file is for convert pdf to text, 
    read pdf and save text to folder metadata"""

from pathlib import Path
from pypdf import PdfReader

PDFS_DIR = Path("/home/kuba/rag-systems/data/raw_pdfs")
METADATA_DIR = Path(f"/home/kuba/rag-systems/data/metadata")
METADATA_DIR.mkdir(parents=True, exist_ok=True)

counter = 0 

for paper in PDFS_DIR.glob("*.pdf"):
    paper_id = paper.stem
    out_file = METADATA_DIR / f"{paper_id}.txt"

    if not paper.exists():
        raise FileNotFoundError(f"File doesnt exist: {PDFS_DIR / paper_id}")

    if out_file.exists():
        print(f"File {paper_id} was save before ", out_file)
        continue

    #Open pdf
    reader = PdfReader(paper)
    print(f"Number of pages: {len(reader.pages)}")

    #Saving text
    full_text = ""

    #Loop for extract text from pdf
    for page_number, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            full_text += text + "\n"
        print(f"processed page: {page_number}")

    #Saving extract text to txt
    out_file.write_text(full_text, encoding="utf-8")
    counter += 1

    print(f"Text was save to {out_file}")
    print(f"PDF nr {counter}|{paper_id} have {len(reader.pages)} pages")