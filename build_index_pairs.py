# build_index_pairs.py
# Embeds each chunk in chunks_pairs.json and saves the vectors to index_pairs.faiss.

import json
import os

import faiss
import numpy as np
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"), http_options=types.HttpOptions(timeout=20000))

CHUNKS_FILE = "chunks_pairs.json"
INDEX_FILE = "index_pairs.faiss"

with open(CHUNKS_FILE, encoding="utf-8") as file:
    chunks = json.load(file)

result = client.models.embed_content(
    model="gemini-embedding-001",
    contents=[chunk["text"] for chunk in chunks],
    config=types.EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT"),
)
vectors = np.array([item.values for item in result.embeddings], dtype="float32")
faiss.normalize_L2(vectors)

index = faiss.IndexFlatIP(vectors.shape[1])
index.add(vectors)
faiss.write_index(index, INDEX_FILE)

print(f"Indexed {index.ntotal} chunks, each with {vectors.shape[1]} numbers")