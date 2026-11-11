# Risks

## Hallucination
- The model refused on some answerable questions even when the expected passage was retrieved. Q04 refused at top 3 in both runs. Q05 refused once at top 3.
- At top 5, Q14 and Q19 refused even though relevant passages were retrieved.
- The citation check catches citations to passages that weren't retrieved. It does not catch claims that have no citation, so unsupported statements can pass the automatic check. Those need a person to read the answer.
- The model's wording varies between runs for the same question. The meaning stayed mostly stable, but exact wording can't be tested.
- The answer key was written by us, and the test set has 20 questions, so the results are a small check, not proof.

## Privacy
- Each question and its retrieved passages are sent to the Gemini API. A user who types personal information into a question sends it to Gemini.
- The corpus is our own sample text, with no real personal data. Before using real documents, check how Google handles API data under its current terms. We have not checked those terms.

## Freshness
- The index is built from a fixed set of documents at one point in time. The model only knows what's in those documents, so it can't answer about recent events (Q20 shows this).
- If the documents change, the index must be rebuilt. Otherwise the answers will be out of date.

## Cost
- Each question makes two API calls: one for the embedding and one for the answer.
- The free tier allows 15 generation requests per minute. The first full run hit that limit, so the script now pauses 5 seconds after each question.
- Paid use is charged per token. Check current pricing before estimating costs.

## Latency
- A full run of 20 questions takes several minutes, because of the pauses and the API calls.
- Each request has a 20-second timeout. Without a timeout, a stalled connection can block the run indefinitely.
- A network failure (the getaddrinfo error) stopped one run partway, and that run produced no output file.