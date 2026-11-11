# run_evaluation.py
# Runs each question in evaluation_questions.csv through retrieval and generation,
# then writes one row per question to evaluation_answers.csv.

import csv
import json
import os
import re
from collections import Counter

import faiss
import time
import numpy as np
from dotenv import load_dotenv
from google import genai
from google.genai import types

from build_prompt import build_prompt

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"), http_options=types.HttpOptions(timeout=20000))

INDEX_FILE = "index_paragraph.faiss"
CHUNKS_FILE = "chunks_paragraph.json"
QUESTIONS_FILE = "evaluation_questions.csv"
OUTPUT_FILE = "evaluation_answers.csv"
MODEL = "gemini-3.5-flash-lite"
TOP_K = 5

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


def status_for(question_type, expected, retrieved, cited, says_not_enough):
    # Any cited ID that was not retrieved is a failure.
    if cited - retrieved:
        return "fail"
    # Unanswerable questions pass only when the model declines and cites nothing.
    if question_type == "unanswerable":
        return "pass" if says_not_enough and not cited else "fail"
    # Answerable questions need the expected passage in the top results, then a person reads the answer.
    if question_type == "answerable":
        return "review" if expected & retrieved else "fail"
    # Ambiguous and misleading questions always need a person to read the answer.
    return "review"


rows = []
for item in questions:
    _, positions = index.search(embed_query(item["question"]), TOP_K)
    passages = [chunks[p] for p in positions[0]]
    retrieved = {p["chunk_id"] for p in passages}

    response = client.models.generate_content(
        model=MODEL,
        contents=build_prompt(item["question"], passages),
        config=types.GenerateContentConfig(temperature=0),
    )
    answer = response.text.strip()
    cited = set(re.findall(r"\d{2}-\d{3}", answer))
    expected = {x for x in item["expected_chunk_ids"].split(";") if x}
    says_not_enough = "not enough information" in answer.lower()

    if not expected:
        expected_hit = "n/a"
    elif expected & retrieved:
        expected_hit = "yes"
    else:
        expected_hit = "no"
    
    time.sleep(5)

    rows.append({
        "question_id": item["question_id"],
        "question_type": item["question_type"],
        "retrieved_ids": ";".join(p["chunk_id"] for p in passages),
        "expected_hit": expected_hit,
        "answer": answer.replace("\n", " "),
        "cited_ids": ";".join(sorted(cited)),
        "cited_not_retrieved": ";".join(sorted(cited - retrieved)),
        "status": status_for(item["question_type"], expected, retrieved, cited, says_not_enough),
    })

with open(OUTPUT_FILE, "w", encoding="utf-8", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=list(rows[0].keys()))
    writer.writeheader()
    writer.writerows(rows)

print(f"Wrote {len(rows)} rows to {OUTPUT_FILE}")
print(Counter(row["status"] for row in rows))