# Change log

## Change: top-k from 3 to 5
- Setting changed: TOP_K in run_evaluation.py, from 3 to 5.
- Reason: Q13 was a retrieval miss at top 3 (expected passages 07-004, 08-002, 09-003 were not retrieved).
- Results at top 3 (two runs): Q13 fail in both. Q04 refused in both. Q14 answered in both.
- Results at top 5 (two runs): Q13 hit in both. Q04 answered in both. Q14 refused in both.
- Other changes: Q05 refused once at top 3 and answered once, so it looks like variance. Q15 retrieval hit at top 5, but refused in both runs.
- Known limit: Q14 now refuses at top 5. The expected passages were retrieved, so the refusal comes from generation.
- Decision: keep top 5 for the project.

## Final Evaluation Answers
Final run at top 5: all 20 questions completed, with 2 pass, 18 review, and no citations outside the retrieved passages. Results saved to evaluation_answers_top5_final.csv.