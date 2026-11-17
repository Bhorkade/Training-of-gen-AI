# StartupSetu - AI-Powered Startup Guidance Platform

StartupSetu is an AI-powered platform that helps students and entrepreneurs understand startup registration, DPIIT recognition, government schemes, funding opportunities, and startup benefits in India.

## Technologies Used
- Python
- FastAPI
- Pandas
- JSON
- Scikit-learn (TF-IDF)
- Sentence Transformers
- ChromaDB
- REST API

## Development Progress

### Day 01 - Project Introduction
- Defined project objectives and problem statement.
- Planned the project structure.

### Day 02 - Data Collection
- Created sample startup records.
- Implemented keyword search and category-wise counting.

### Day 03 - Data Processing
- Collected government startup data.
- Implemented CSV data ingestion.
- Cleaned and converted records into JSON.

### Day 04 - FastAPI Development
- Created a FastAPI application.
- Developed endpoints for health checks, records, and search.

### Day 05 - Smart Search
- Implemented TF-IDF-based search.
- Used cosine similarity to find relevant records.
- Tested sample questions.

### Day 06 - Prompt Engineering & LLM Evaluation
- Integrated Gemini LLM with system and task-specific prompts (`prompts/`).
- Conducted comparative evaluation between Basic and Improved prompt versions across 10 StartupSetu questions.
- Recorded confidence and winner analysis in `eval/prompt_compare.md`.

### Day 07 - Semantic Search with ChromaDB
- Implemented document chunking retaining `source`, `page`, and `title` metadata in `app/chunking.py`.
- Embedded records with Sentence Transformers (`all-MiniLM-L6-v2`) and stored in ChromaDB vector store.
- Integrated `/search/semantic` endpoint in FastAPI.
- Evaluated top semantic hits and relevance across 10 questions in `eval/search_results.md`.

### Day 08 - RAG Pipeline with Citations & Refusal Evaluation
- Developed the RAG pipeline module in `app/rag.py` with chunk retrieval, score filtering, structured synthesis, citation formatting, and refusal mechanisms.
- Implemented the `POST /ask` endpoint in `app/main.py` allowing users to query startup policies with verifiable citations (`source`, `page`, `title`).
- Created an evaluation dataset of 15 queries in `eval/eval_set.json` including answerable and unanswerable edge cases.
- Implemented `eval/run_eval.py` to compare two RAG pipeline configurations:
  - **Configuration 1 (Baseline RAG):** `top_k=2`, `min_score=0.35`, lenient refusal rule.
  - **Configuration 2 (Enhanced RAG):** `top_k=3`, `min_score=0.48`, strict refusal rule.
- Recorded evaluation results in `eval/eval_results.md` showing **Configuration 2** is the superior configuration (100% accuracy vs 80.0%).

## Day 08 RAG Evaluation Results

### Configuration Comparison Summary

| Metric | Configuration 1 (Baseline) | Configuration 2 (Enhanced) | Better Configuration |
|---|---|---|---|
| **Top-K Chunks** | `2` | `3` | Config 2 (Better context coverage) |
| **Min Similarity Score** | `0.35` | `0.48` | Config 2 (Strict hallucination filter) |
| **Strict Refusal Rule** | `False` | `True` | Config 2 (Guards against false promises) |
| **Refusal Accuracy** | `0.0%` | `100.0%` | **Config 2** |
| **Answer Accuracy** | `100.0%` | `100.0%` | **Config 2** |
| **Citation Rate** | `100.0%` | `100.0%` | **Config 2** |
| **Overall Accuracy** | `80.0%` | `100.0%` | **Config 2 (WINNER)** |

### Detailed Evaluation Table (15 Test Rows)

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

### Better Configuration Analysis
**Configuration 2** was chosen as the winning production configuration for StartupSetu:
1. **Zero Hallucination on Unanswerable Inquiries:** By maintaining a similarity score threshold of `0.48` and enforcing strict refusal rules, it refused 100% of out-of-scope or speculative queries (such as speculative grant numbers in Q10, NASA subsidies in Q14, and unconditional cash grants in Q15).
2. **Reliable Citations:** All 12 answerable queries retrieved official government records with exact document titles, page numbers, and official portal URLs.

## Project Status
RAG pipeline, API integration (`POST /ask`), and comparative evaluation completed. Project development is ongoing.

## Developer
Shrikar Bhorkade
