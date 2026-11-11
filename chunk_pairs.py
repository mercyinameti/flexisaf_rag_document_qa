# chunk_pairs.py
# Splits each document into chunks of two paragraphs and writes chunks_pairs.json.

import csv
import json
from pathlib import Path

OUTPUT_FILE = "chunks_pairs.json"
PARAGRAPHS_PER_CHUNK = 2

chunks = []
with open("sources.csv", encoding="utf-8", newline="") as file:
    for source in csv.DictReader(file):
        text = Path("documents", source["file_name"]).read_text(encoding="utf-8")
        blocks = [block.strip() for block in text.split("\n\n") if block.strip()]
        body = blocks[1:]  # The first block is the title.

        for start in range(0, len(body), PARAGRAPHS_PER_CHUNK):
            group = body[start:start + PARAGRAPHS_PER_CHUNK]
            first = start + 1
            last = start + len(group)
            chunks.append({
                "chunk_id": f"{source['doc_id']}-P{first:03d}-{last:03d}",
                "paragraph_ids": [f"{source['doc_id']}-{n:03d}" for n in range(first, last + 1)],
                "doc_id": source["doc_id"],
                "title": source["title"],
                "category": source["category"],
                "date_written": source["date_written"],
                "section": f"Paragraphs {first}-{last}",
                "text": "\n\n".join(group),
            })

with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
    json.dump(chunks, file, ensure_ascii=False, indent=2)

print(f"Wrote {len(chunks)} chunks to {OUTPUT_FILE}")