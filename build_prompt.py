# build_prompt.py
# Builds the prompt sent to Gemini: the rules, the retrieved passages, and the question.

RULES = (
    "Answer the question using only the passages below. "
    "If the passages do not contain the answer, reply exactly: Not enough information. "
    "After each factual sentence, cite the chunk ID it came from in square brackets, such as [08-002]. "
    "Cite only chunk IDs that appear in the passages."
)


def build_prompt(question, passages):
    # Each passage is a dict with a chunk_id and a text field.
    blocks = [f"[{p['chunk_id']}]\n{p['text']}" for p in passages]
    return f"{RULES}\n\nPassages:\n\n" + "\n\n".join(blocks) + f"\n\nQuestion: {question}\nAnswer:"


if __name__ == "__main__":
    sample = [
        {"chunk_id": "08-002", "text": "Some information should rarely be shared with an AI tool at all."},
        {"chunk_id": "08-001", "text": "AI systems often learn from data, and that data can include personal information."},
    ]
    print(build_prompt("Should I share my bank card number with an AI tool?", sample))