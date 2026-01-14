"""This file is for downloading scientific papers 
    from website arxiv.org and save them to folder raw_pdfs"""

from pathlib import Path
import requests

#path to store downloaded pdfs
PDFS_DIR = Path("/home/kuba/rag-systems/data/raw_pdfs")
PDFS_DIR.mkdir(parents=True, exist_ok=True)


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

#Loop to download each pdf
for paper_id in ARXIV_ID:
    url = f"https://arxiv.org/pdf/{paper_id}.pdf"
    out_file = PDFS_DIR / f"{paper_id}.pdf"

    if out_file.exists():
        print(f"File {paper_id} was save before ", out_file)
        continue

    print("downloading: ", paper_id)

    response =  requests.get(url)
    response.raise_for_status()

    out_file.write_bytes(response.content)

    print(f"Save: {out_file}")