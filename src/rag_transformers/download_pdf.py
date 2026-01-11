"""This file is for downloading scientific papers 
    from website arxiv.org and save them to folder raw_pdfs"""

from pathlib import Path
import requests

#arxiv id scientific papers
ARXIV_ID = [
    "1706.03762",
    "1803.02155",
    "1810.04805",
    "1901.02860",
    "2006.03654",
    "2009.06732",
    "2004.05150",
]

#path to store downloaded pdfs
out_dir = Path("/home/kuba/RAG/rag-systems/data/raw_pdfs")
out_dir.mkdir(parents=True, exist_ok=True)

#Loop to download each pdf
for id in ARXIV_ID:
    url = f"https://arxiv.org/pdf/{id}.pdf"
    out_path = out_dir / f"{id}.pdf"

    if out_path.exists():
        print("File was save before ", out_path)
        continue

    print("downloading: ", id)

    response =  requests.get(url)
    response.raise_for_status()

    out_path.write_bytes(response.content)

    print("Save: ", out_path)