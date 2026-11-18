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
- LangGraph
- Streamlit
- Pytest
- Ruff
- Docker & Docker Compose



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

### Day 09 - Agent Tools, Loop & LangGraph with Memory and Approval
- **Domain Tools (`app/tools.py`):**
  - `check_dpiit_eligibility`: Evaluates startup eligibility based on entity type, age (<=10 years), turnover (<= ₹100 Cr), and innovation/scalability.
  - `get_scheme_details`: Provides real-time lookup for official schemes (Seed Fund, 80-IAC, CGSS, SIPP, MSInS).
  - `query_rag`: Direct retrieval of verified policy playbooks with citations.
  - `submit_dpiit_application`: Mutating action recording registration drafts into `data/applications.json`.
- **Hand-written Agent Loop (`app/agent_loop.py`):**
  - ReAct Reason-Act-Observe cycle with tool parsing and fallback heuristic reasoning.
- **LangGraph Agent (`app/graph.py`):**
  - Stateful graph with `MemorySaver` for multi-turn session persistence.
  - **Human-in-the-Loop (Approval Step):** Sensitive operations like `submit_dpiit_application` pause execution and require explicit human confirmation (`approved=True`) before persisting.
  - Integrated `POST /agent` endpoint in FastAPI.

### Day 10 - Streamlit Interactive UI & Feedback System
- Built dual-mode interactive chat interface in `ui/app.py` supporting `/ask` (Direct RAG) and `/agent` (LangGraph Autonomous Agent).
- Direct visualization of verified government citations (page numbers, titles, official links).
- Interactive Human Approval interface: displays `✅ Approve Action` and `❌ Reject Action` buttons when mutating actions are requested.
- User feedback mechanism: Thumbs Up / Down ratings saved persistently in `data/feedback.json`.

![StartupSetu UI Chat Screen](docs/ui_chat_screen.png)

### Day 11 - Testing Suite, Code Quality & Docker Containerization
- **Automated Test Suite (`tests/`):**
  - Created 20 comprehensive automated unit and integration tests across 5 modules:
    - `tests/test_health.py`: Verifies `GET /health` system readiness.
    - `tests/test_records.py`: Tests data loading, pagination, and ID retrieval (including 404 handling).
    - `tests/test_search.py`: Tests TF-IDF smart search, query matching, and parameter validation.
    - `tests/test_rag.py`: Tests `POST /ask` with mock/fake LLM synthesis, citation extraction, and strict refusal on out-of-scope queries.
    - `tests/test_agent.py`: Validates DPIIT eligibility evaluation logic, scheme lookup, application creation, hand-written agent loop, and LangGraph human approval step.
  - All 20 tests pass (`pytest -q` 100% green).
- **Code Quality & Linting:**
  - Configured `pyproject.toml` with Ruff standards.
  - Passed `ruff check .` with zero linting or formatting errors.
- **Docker Containerization:**
  - Authored production `Dockerfile` with multi-service support.
  - Created `.dockerignore` to keep image builds lightweight and secure.
  - Configured multi-container orchestration with `docker-compose.yml` linking the FastAPI backend (`api`) and Streamlit frontend (`ui`).

---

## Run with Docker

StartupSetu can be launched with Docker and Docker Compose.

### 1. Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.
- A valid Gemini API Key (set in `.env`).

### 2. Configure Environment
Create or edit your `.env` file in the project root:
```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
GEMINI_MODEL=gemini-3.8-flash
```

### 3. Build and Start Services
Run the following command from the project root:
```bash
docker compose up --build
```

To run in detached mode (background):
```bash
docker compose up -d --build
```

### 4. Access the Application
Once running, the following services are available:

| Service | URL | Description |
|---|---|---|
| **Streamlit Interactive UI** | [http://localhost:8501](http://localhost:8501) | Full chat UI with dual modes, citations, approval buttons, and feedback. |
| **FastAPI Interactive Docs (Swagger)** | [http://localhost:8000/docs](http://localhost:8000/docs) | Interactive OpenAPI documentation for all endpoints. |
| **API Health Check** | [http://localhost:8000/health](http://localhost:8000/health) | System health and readiness verification. |
| **RAG Query Endpoint** | `POST http://localhost:8000/ask` | Direct RAG queries with citations and refusal filters. |
| **LangGraph Agent Endpoint** | `POST http://localhost:8000/agent` | Autonomous agent with memory and human-in-the-loop approval. |

### 5. Stopping the Containers
To stop and remove containers and networks:
```bash
docker compose down
```

---

## Developer
Shrikar Bhorkade
