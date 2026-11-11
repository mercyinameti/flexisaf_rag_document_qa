# answer.py
# Retrieves passages for a question, builds the prompt, and asks Gemini for an answer.

import json
import os
import sys

import faiss
import numpy as np
from dotenv import load_dotenv
from google import genai
from google.genai import types

from build_prompt import build_prompt

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"), http_options=types.HttpOptions(timeout=20000))

INDEX_FILE = "index_paragraph.faiss"
CHUNKS_FILE = "chunks_paragraph.json"
MODEL = "gemini-3.5-flash-lite"
TOP_K = 3

question = " ".join(sys.argv[1:]) or "How do machines learn from examples?"

index = faiss.read_index(INDEX_FILE)
with open(CHUNKS_FILE, encoding="utf-8") as file:
    chunks = json.load(file)

embedded = client.models.embed_content(
    model="gemini-embedding-001",
    contents=question,
    config=types.EmbedContentConfig(task_type="RETRIEVAL_QUERY"),
)
query = np.array([embedded.embeddings[0].values], dtype="float32")
faiss.normalize_L2(query)
_, positions = index.search(query, TOP_K)
passages = [chunks[p] for p in positions[0]]

prompt = build_prompt(question, passages)
response = client.models.generate_content(
    model=MODEL,
    contents=prompt,
    config=types.GenerateContentConfig(temperature=0),
)
print(response.text)

import re

retrieved_ids = {p["chunk_id"] for p in passages}
cited_ids = set(re.findall(r"\d{2}-\d{3}", response.text))
print("Cited:", sorted(cited_ids) or "none")
print("Cited but not retrieved:", sorted(cited_ids - retrieved_ids) or "none")

print("\nSources:")
for chunk_id in sorted(cited_ids & retrieved_ids):
    chunk = next(p for p in passages if p["chunk_id"] == chunk_id)
    print(f"- {chunk_id}: {chunk['title']}, {chunk['section']}")