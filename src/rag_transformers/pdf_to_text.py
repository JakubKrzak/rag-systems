"""This file is for convert pdf to text, 
    read pdf and save text to folder metadata"""

from pathlib import Path
from pypdf import PdfReader

#id
id_pdf = [
    "1706.03762",
    "1803.02155",
    "1810.04805",
    "1901.02860",
    "2006.03654",
    "2009.06732",
    "2004.05150",
]
counter = 0 #Counter for number of finish pdf

for id in id_pdf:
    
    #pdf path
    pdf_path = Path(f"/home/kuba/RAG/rag-systems/data/raw_pdfs/{id}.pdf")

    if not pdf_path.exists():
        raise FileNotFoundError(f"File doesnt exist: {pdf_path}")

    #Open pdf
    reader = PdfReader(pdf_path)
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
    out_path = Path(f"/home/kuba/RAG/rag-systems/data/metadata/{id}.txt")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(full_text, encoding="utf-8")
    counter += 1

    print(f"Text was save to {out_path}")

    print(f"PDF nr {counter}|{id} have {len(reader.pages)} pages")