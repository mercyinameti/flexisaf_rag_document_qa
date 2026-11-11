# retrieve.py
# Finds the chunks closest to a question and prints them with their metadata. No language model is used.

import json
import os
import sys

import faiss
import numpy as np
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()  # Reads GEMINI_API_KEY from the .env file.
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

INDEX_FILE = "index_paragraph.faiss"
CHUNKS_FILE = "chunks_paragraph.json"
TOP_K = 3  # Number of chunks returned for each question.

question = " ".join(sys.argv[1:]) or "How do machines learn from examples?"

index = faiss.read_index(INDEX_FILE)
with open(CHUNKS_FILE, encoding="utf-8") as file:
    chunks = json.load(file)

result = client.models.embed_content(
    model="gemini-embedding-001",
    contents=question,
    config=types.EmbedContentConfig(task_type="RETRIEVAL_QUERY"),
)
query = np.array([result.embeddings[0].values], dtype="float32")
faiss.normalize_L2(query)  # Scales the question vector to match the chunk vectors.

scores, rows = index.search(query, TOP_K)
print(f"Question: {question}\n")
for rank, (score, row) in enumerate(zip(scores[0], rows[0]), start=1):
    chunk = chunks[row]
    print(f"{rank}. {chunk['chunk_id']} | {chunk['title']} | {chunk['section']} | score {score:.3f}")
    print(f"   {chunk['text']}\n")