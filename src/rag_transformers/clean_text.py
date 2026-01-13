from pathlib import Path
import re

#path
metadata_path = "/home/kuba/rag-systems/data/metadata"
processed_data_path = "/home/kuba/rag-systems/data/processed_data"

#Folders
input_dir = Path(metadata_path)
output_dir = Path(processed_data_path)
output_dir.mkdir(parents=True, exist_ok=True)

#Cleaning txt
counter = 0
for txt_path in input_dir.glob("*.txt"):
    print(f"Cleaning: {txt_path.name}")

    text = txt_path.read_text(encoding="utf-8")

    #Replace multiple spaces with a single space
    text = re.sub(r"[ \t]+", " ", text)

    #Remove blank lines
    text = re.sub(r"\n\s*\n+", "\n\n", text)

    #Trim whitespaces
    text = text.strip()

    out_path = output_dir / txt_path.name
    out_path.write_text(text, encoding="utf-8")
    counter += 1

    print(f"PDF nr {counter}, Saved cleaned: {out_path}")
    