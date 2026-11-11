# Failure record

## Retrieval failure: Q13
- Question: What are some precautions when using AI?
- Expected passages: 07-004, 08-002, 09-003
- Retrieved top 3: 09-004, 09-001, 08-004
- Result: none of the expected passages were in the top 3.
- Answer: grounded in the retrieved passages, with no invalid citations.
- Status: recorded for step 19 (top-k change to 5).

## Generation failure: Q04
- Question: What is the difference between narrow AI and general AI?
- Retrieved top 3: 04-003, 04-001, 04-004 (04-001 is an expected passage)
- Result: "Not enough information." in both runs, despite the expected passage being retrieved.
- Status: the model refused when the evidence was present.