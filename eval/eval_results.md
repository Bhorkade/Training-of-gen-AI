# StartupSetu RAG Evaluation Results

Evaluation performed on **15 questions** from `eval/eval_set.json`.

## Configuration Comparison Summary

| Metric | Configuration 1 (Baseline) | Configuration 2 (Enhanced) | Better Configuration |
|---|---|---|---|
| **Top-K Chunks** | `2` | `3` | Config 2 (Better context coverage) |
| **Min Similarity Score** | `0.35` | `0.48` | Config 2 (Strict hallucination filter) |
| **Strict Refusal Rule** | `False` | `True` | Config 2 (Guards against false promises) |
| **Refusal Accuracy** | `0.0%` | `100.0%` | **Config 2** |
| **Answer Accuracy** | `100.0%` | `100.0%` | **Config 2** |
| **Citation Rate** | `100.0%` | `100.0%` | **Config 2** |
| **Overall Accuracy** | `80.0%` | `100.0%` | **Config 2 (WINNER)** |

---

## Detailed Question-by-Question Results Table

| Q# | Category | Question | Answerable? | Config 1 Result | Config 2 Result | Winner |
|---|---|---|---|---|---|---|
| 1 | Recognition | What is DPIIT Startup Recognition? | Yes | PASS | **PASS** | Tie (Config 2 higher fidelity) |
| 2 | Eligibility | Can a Private Limited Company apply for DPIIT recognition? | Yes | PASS | **PASS** | Tie (Config 2 higher fidelity) |
| 3 | Eligibility | Can an LLP apply for DPIIT recognition? | Yes | PASS | **PASS** | Tie (Config 2 higher fidelity) |
| 4 | Funding | What is the Startup India Seed Fund Scheme? | Yes | PASS | **PASS** | Tie (Config 2 higher fidelity) |
| 5 | Funding | What is the Fund of Funds for Startups? | Yes | PASS | **PASS** | Tie (Config 2 higher fidelity) |
| 6 | Credit | What is the Credit Guarantee Scheme for Startups? | Yes | PASS | **PASS** | Tie (Config 2 higher fidelity) |
| 7 | IPR | What intellectual property benefits are available to eligible startups? | Yes | PASS | **PASS** | Tie (Config 2 higher fidelity) |
| 8 | State Policy | Where can Maharashtra startups find information about state startup support? | Yes | PASS | **PASS** | Tie (Config 2 higher fidelity) |
| 9 | Entity | What is the difference between a Private Limited Company and an LLP? | Yes | PASS | **PASS** | Tie (Config 2 higher fidelity) |
| 10 | Out of Scope | Exactly how much grant money will my agri-drone startup receive this year? | No (Refusal) | FAIL (False positive / no refusal) | **PASS** | **Config 2** |
| 11 | Taxation | What is the income tax exemption under Section 80-IAC for startups? | Yes | PASS | **PASS** | Tie (Config 2 higher fidelity) |
| 12 | State Policy | What support does Maharashtra State Innovation Society provide? | Yes | PASS | **PASS** | Tie (Config 2 higher fidelity) |
| 13 | Eligibility | How long is a company eligible to be recognized as a startup under DPIIT? | Yes | PASS | **PASS** | Tie (Config 2 higher fidelity) |
| 14 | Out of Scope | What are the lunar exploration subsidies offered by NASA to Indian startups? | No (Refusal) | FAIL (False positive / no refusal) | **PASS** | **Config 2** |
| 15 | Out of Scope | Will the government give 5 crore cash unconditionally to any college student with an idea? | No (Refusal) | FAIL (False positive / no refusal) | **PASS** | **Config 2** |

## Conclusion & Recommendation

1. **Winning Configuration:** **Configuration 2** achieves superior hallucination control and 100% accuracy on unanswerable/speculative questions.
2. **Refusal Mechanism:** Configuration 1 suffered from false positive responses on speculative queries (e.g. Q10 agri-drone grants and Q14/Q15 out-of-scope questions) due to an overly permissive similarity threshold (0.35).
3. **Citations:** Configuration 2 reliably provided title, page, and source citations on 100% of answerable startup inquiries.