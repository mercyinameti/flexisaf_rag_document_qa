# add_sections.py
# Adds a section field to each chunk in chunks.json, then saves the file.

import json
import re

CHUNKS_FILE = "chunks.json"

with open(CHUNKS_FILE, encoding="utf-8") as file:
    chunks = json.load(file)

for chunk in chunks:
    # The number after the last dash in the chunk ID is the paragraph's position in its document.
    position = int(chunk["chunk_id"].split("-")[-1])
    # Document 06 starts each paragraph with a label such as "Myth 3:", so I use that label when it's present.
    label = re.match(r"(Myth \d+):", chunk["text"])
    chunk["section"] = label.group(1) if label else f"Paragraph {position}"

with open(CHUNKS_FILE, "w", encoding="utf-8") as file:
    json.dump(chunks, file, indent=2, ensure_ascii=False)

print(f"Added a section to {len(chunks)} chunks.")