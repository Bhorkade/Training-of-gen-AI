# StartupSetu — Master Progress Tracker (Days 01 – 15)

This document tracks the complete development lifecycle, deliverables, tests, and verification checkpoints for the **StartupSetu** project under the 15-day AI Training curriculum.

---

## Executive Summary Checklist

| Metric | Target | Achieved Status | Verification |
|---|---|---|---|
| **Curriculum Days Completed** | Days 01 – 14 | **100% Completed** | All build labs implemented & pushed |
| **Automated Tests** | $\ge 8$ Tests | **25 Tests Passing** | `pytest -q` 100% green |
| **Code Quality / Linting** | Zero Errors | **Ruff Clean** | `ruff check .` passing |
| **Git Milestones / Tags** | Checkpoint 1, 2, Final | **All Tags Created** | `checkpoint-1`, `checkpoint-2`, `final` |
| **Continuous Integration** | Automated CI | **Green Badge** | GitHub Actions Workflow `#45153795945` |
| **Cloud Deployment** | Public URL | **Render CD Blueprint** | API `/health` & Streamlit UI configured |
| **Demo Day Readiness** | 100% | **READY** | Pitches, architecture & viva prep completed |

---

## Daily Progress & Deliverables Tracker

### Block 1: Foundations (Days 01 – 05)

- [x] **Day 01 — Your First Python Programs & Git Setup**
  - **Forenoon:** Created project directory, authored `day01_intro.py` (variables, f-strings, interactive inputs).
  - **Afternoon:** Created public GitHub repo `Bhorkade/Training-of-gen-AI`, authored `day01_menu.py` (while loop interactive console menu).
  - **Status:** **CLOSED & VERIFIED** (Commits: `day-01: ...`).

- [x] **Day 02 — Collections, Functions & Clean Architecture**
  - **Forenoon:** Built `data/sample_records.py` with 20 real Startup India records, category counter, and keyword search in `day02_tasks.py`.
  - **Afternoon:** Refactored into modular `app/records.py` (`load_records()`, `search()`, `count_by()`, `get_by_id()`), `app/cli.py`, `.venv`, and `requirements.txt`.
  - **Status:** **CLOSED & VERIFIED** (Commits: `day-02: ...`).

- [x] **Day 03 — Real Data Ingestion, DataClasses & Requests**
  - **Forenoon:** Added real government records dataset `data/raw/startupsetu_master.csv`, wrote `app/ingest.py`, and serialized cleaned data into `data/records.json`.
  - **Afternoon:** Created `Record` dataclass in `app/models.py`, authored `app/fetch.py` for downloading official startup documents with error handling.
  - **Status:** **CLOSED & VERIFIED** (Commits: `day-03: ...`).

- [x] **Day 04 — FastAPI Web Service, Pandas & TF-IDF Smart Search**
  - **Forenoon:** Built `app/main.py` exposing `GET /health`, `GET /records`, `GET /records/{id}`, `GET /search`, and `POST /questions` (persisting to `data/questions.json`).
  - **Afternoon:** Authored `analysis/explore.py` (pandas exploration) and `app/smart_search.py` (TF-IDF + cosine similarity ranking).
  - **Status:** **CLOSED & VERIFIED** (Commits: `day-04: ...`, Tag: `week-1`).

- [x] **Day 05 — Deep Learning, LLM Foundations & Checkpoint 1**
  - **Forenoon:** Authored `docs/how_llms_work.md` with neural network diagrams, tokenization, transformer attention, and 10 real evaluation queries.
  - **Afternoon:** Passed Checkpoint 1 technical review; verified `/health`, `/records`, and `/search` via Swagger UI.
  - **Status:** **CLOSED & VERIFIED** (Tag: `checkpoint-1`).

---

### Block 2: GenAI Core & Agentic Systems (Days 06 – 10)

- [x] **Day 06 — LLM Integration & Prompt Engineering**
  - **Forenoon:** Authored `app/llm.py` wrapping Gemini API with `.env` secret management; exposed `POST /chat`.
  - **Afternoon:** Created `prompts/` (`system.txt`, `dpiit_recognition.txt`, `schemes_benefits.txt`) and evaluated Basic vs Improved prompts in `eval/prompt_compare.md`.
  - **Status:** **CLOSED & VERIFIED** (Commits: `day-06: ...`).

- [x] **Day 07 — Semantic Search & ChromaDB Vector Store**
  - **Forenoon:** Created `app/chunking.py` (preserving `title`, `page`, `source` metadata) and `app/embed.py` using Sentence Transformers (`all-MiniLM-L6-v2`); recorded search evaluation in `eval/search_results.md`.
  - **Afternoon:** Built `app/vectorstore.py` with persistent ChromaDB collection; added `GET /search/semantic` endpoint.
  - **Status:** **CLOSED & VERIFIED** (Commits: `day-07: ...`).

- [x] **Day 08 — RAG Pipeline with Strict Citations & Refusal Evaluation**
  - **Forenoon:** Implemented `app/rag.py` with chunk retrieval, score thresholding, structured synthesis, and `POST /ask`.
  - **Afternoon:** Created 15-question benchmark in `eval/eval_set.json`, ran `eval/run_eval.py` comparing Baseline RAG (80% accuracy) vs Enhanced Strict RAG (100% accuracy); documented results in `eval/eval_results.md`.
  - **Status:** **CLOSED & VERIFIED** (Commits: `day-08: ...`).

- [x] **Day 09 — Agent Tools, Hand-Written ReAct Loop & LangGraph with Memory**
  - **Forenoon:** Implemented domain tools in `app/tools.py` (`check_dpiit_eligibility`, `get_scheme_details`, `query_rag`, `submit_dpiit_application`) and custom ReAct loop `app/agent_loop.py`.
  - **Afternoon:** Built stateful LangGraph agent in `app/graph.py` with `MemorySaver` thread persistence and Human-in-the-Loop (HITL) approval gate for application drafts; exposed `POST /agent`.
  - **Status:** **CLOSED & VERIFIED** (Commits: `day-09: ...`).

- [x] **Day 10 — Streamlit Interactive UI, Eligibility Form & Checkpoint 2**
  - **Forenoon:** Developed `ui/app.py` with dual-mode chat (`/ask` & `/agent`), signature 4-pillar DPIIT statutory eligibility form (`st.form`), inline citation links, action approval buttons, and feedback logging to `data/feedback.json`.
  - **Afternoon:** Passed Checkpoint 2 live RAG demonstration and test review.
  - **Status:** **CLOSED & VERIFIED** (Tag: `checkpoint-2`).

---

### Block 3: Production Engineering & Cloud Deployment (Days 11 – 15)

- [x] **Day 11 — Automated Testing Suite & Docker Containerization**
  - **Forenoon:** Authored 20 unit/integration tests across 5 modules in `tests/`; passed `ruff check .` with zero errors.
  - **Afternoon:** Containerized application with multi-stage production `Dockerfile`, `docker-compose.yml`, and `.dockerignore`.
  - **Status:** **CLOSED & VERIFIED** (Commits: `day-11: ...`).

- [x] **Day 12 — Continuous Integration (CI), Feature PR & Cloud CD**
  - **Forenoon:** Added GitHub Actions CI workflow `.github/workflows/ci.yml`; opened and merged [Pull Request #1](https://github.com/Bhorkade/Training-of-gen-AI/pull/1) from `feat/ci-workflow-day12` with green CI badge.
  - **Afternoon:** Configured Render CD blueprint `render.yaml` for automated deployment from `main`.
  - **Status:** **CLOSED & VERIFIED** (Commits: `day-12: ...`).

- [x] **Day 13 — Observability, Query Caching, Guardrails & Portfolio Resume**
  - **Forenoon:** Added request latency & token telemetry to `POST /ask`, in-memory cache `ASK_CACHE` (99.3% latency reduction), 500-char input limit, and prompt-injection tests (test suite expanded to 25 passing tests).
  - **Afternoon:** Authored comprehensive `README.md` Production notes with concrete numbers, full Mermaid architecture diagram, and portfolio profile in `docs/resume.md`.
  - **Status:** **CLOSED & VERIFIED** (Commit: `8cb9b90`).

- [x] **Day 14 — Interview Preparation, Render 512MB Optimization & Final Sprint**
  - **Forenoon:** Authored `docs/interview.md` featuring 60-second, 3-minute, and 10-minute pitches, answers to top 10 technical questions, system design sequence diagram, and Python/FastAPI viva drills.
  - **Afternoon:** Optimized container build for Render free tier (CPU-only PyTorch, lazy model loading in `app/embed.py`, thread stack limits); created `PROGRESS.md` with all items closed; validated all 25 tests; prepared for final demo.
  - **Status:** **CLOSED & VERIFIED** (Tag: `final`).

- [ ] **Day 15 — Demo Day & Final Viva**
  - Forenoon: Final EXAMATE assessment & project demo (Part 1).
  - Afternoon: Project showcase & results (Part 2).
  - Status: **SCHEDULED / READY**.

---

## Production Verification Summary

- **Test Suite Status:** 25 passed in 3.08s (`pytest -q` 100% green).
- **Linter Status:** `ruff check .` passed with zero errors or warnings.
- **Git Branch:** Clean working tree on `main` tracking `origin/main`.
- **Git Tags:** `checkpoint-1`, `checkpoint-2`, `final`.
