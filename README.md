# RAG Document Q&A

A small question-answering system over a set of sample documents. It finds the most relevant passages for a question, then asks Gemini to answer using only those passages, with citations.

## Setup

1. Create a virtual environment with Python 3.12:
   `py -3.12 -m venv .venv`
2. Activate it:
   `.venv\Scripts\Activate.ps1`
3. Install the packages:
   `pip install -r requirements.txt`
4. Copy `.env.example` to `.env` and replace `your-key-here` with your Gemini API key.

The `.env` file stays on your computer. `.gitignore` keeps it out of GitHub.

## How it works

1. **Documents:** The sample text is in `documents/`, and `sources.csv` records each document's ID, title, category, and approval status.
2. **Chunks:** `chunks_paragraph.json` splits each document into paragraphs. `add_sections.py` labels each chunk with a section.
3. **Index:** `index_paragraph.faiss` stores an embedding for each chunk. Searches compare the question's embedding with these.
4. **Retrieval:** `retrieve.py` finds the most similar passages for a question, using the top 5 by default.
5. **Prompt:** `build_prompt.py` combines the rules, the passages, and the question into one prompt.
6. **Answer:** `answer.py` retrieves the passages, builds the prompt, asks Gemini, and lists the sources.

## Scripts

| File | What it does |
|---|---|
| `retrieve.py` | Shows the top passages for one question |
| `answer.py` | Answers one question with citations |
| `build_prompt.py` | Builds the prompt sent to Gemini |
| `top_k_compare.py` | Scores top-k settings over the evaluation questions |
| `build_index_pairs.py`, `chunk_pairs.py`, `top_k_compare_pairs.py` | Test the two-paragraph chunking setting |
| `run_evaluation.py` | Runs all evaluation questions and writes `evaluation_answers.csv` |


## Testing

1. **Retrieval check:** `python retrieve.py "How do machines learn from examples?"` shows the top passages for one question.
2. **Top-k check:** `python top_k_compare.py` reports how often the expected passage appears in the top 1, 3, and 5 results, using the 15 earlier questions.
3. **Full evaluation:** `python run_evaluation.py` runs all 20 questions in `evaluation_questions.csv` and writes `evaluation_answers.csv`. Each answer is marked pass, fail, or review. A person reads each review row.

### Results

- **Top-k:** With paragraph chunks, the expected passage appeared in 14 of 15 questions at top 1, and in all 15 at top 3 and top 5.
- **Chunking:** Two-paragraph chunks scored 15 of 15 at top 1. This test favours larger chunks, because a chunk counts as a hit if either paragraph matches, so we kept paragraph chunks.
- **Final run (top 5):** 20 questions, 2 pass, 18 review, 0 fail. No answer cited a passage outside the retrieved set.

The decisions and the reasons for them are in `change_log.md`. The known risks are in `risks.md`.

## Limitations

- The documents are sample text written for this project, not real sources.
- The answer key was written by us, so the results depend on our judgement of which passages answer each question.
- The test set has 20 questions. It's a small check, not a full evaluation.
- Model answers vary between runs. Exact wording can't be tested, only meaning and citations.
- Questions with false premises or several readings sometimes get "Not enough information" even when some passages are relevant (Q14, Q19 at top 5).
- Each answer is checked for citations to passages that were retrieved, but a person still has to read each answer for unsupported claims.
- The index is built once. If the documents change, rebuild it.
- The app sends questions and passages to the Gemini API. Check Google's current terms before using real documents.