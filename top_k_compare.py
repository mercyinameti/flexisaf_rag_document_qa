# top_k_compare.py
# Runs each question in evaluation_questions.csv at each top-k setting and reports hit rates.

import csv
import json
import os

import faiss
import numpy as np
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"), http_options=types.HttpOptions(timeout=20000))

INDEX_FILE = "index_paragraph.faiss"
CHUNKS_FILE = "chunks_paragraph.json"
QUESTIONS_FILE = "evaluation_questions.csv"
KS = [1, 3, 5]

index = faiss.read_index(INDEX_FILE)
with open(CHUNKS_FILE, encoding="utf-8") as file:
    chunks = json.load(file)
with open(QUESTIONS_FILE, encoding="utf-8", newline="") as file:
    questions = list(csv.DictReader(file))


def embed_query(text):
    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text,
        config=types.EmbedContentConfig(task_type="RETRIEVAL_QUERY"),
    )
    query = np.array([result.embeddings[0].values], dtype="float32")
    faiss.normalize_L2(query)
    return query


hits = {k: 0 for k in KS}
for row in questions:
    expected = set(row["expected_chunk_ids"].split(";"))
    _, positions = index.search(embed_query(row["question"]), max(KS))
    for k in KS:
        retrieved = {chunks[p]["chunk_id"] for p in positions[0][:k]}
        if retrieved & expected:
            hits[k] += 1

print("top_k,hits,questions,hit_rate")
for k in KS:
    print(f"{k},{hits[k]},{len(questions)},{hits[k] / len(questions):.2f}")