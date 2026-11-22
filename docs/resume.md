# StartupSetu - Engineering Portfolio & Resume Showcase

## Executive Summary
**StartupSetu** is a production-grade, agentic AI advisory platform engineered to help Indian entrepreneurs, founders, and students navigate DPIIT startup recognition, government schemes (Seed Fund Scheme, 80-IAC Tax Exemption, Credit Guarantee Scheme), statutory compliance, and funding opportunities.

Designed with a defense-in-depth architecture, StartupSetu combines stateful multi-turn agentic workflows (LangGraph), deterministic retrieval-augmented generation (RAG with ChromaDB & Sentence Transformers), statutory policy guardrails, low-latency in-memory caching, and end-to-end CI/CD automation.

---

## Technical Stack & Architecture

| Layer | Technologies & Frameworks | Key Purpose |
|---|---|---|
| **API Gateway & Core Backend** | Python 3.14, FastAPI, Pydantic, Uvicorn | High-throughput async REST endpoints (`/health`, `/records`, `/search`, `/ask`, `/agent`, `/eligibility`) |
| **Agentic AI & Orchestration** | LangGraph, ReAct Agent Loop, `MemorySaver` | Stateful conversational memory, tool orchestration, and Human-in-the-Loop (HITL) approval gates |
| **Vector Store & Embeddings** | ChromaDB, Sentence Transformers (`all-MiniLM-L6-v2`), Scikit-learn (TF-IDF) | Dense semantic search, metadata chunking, and dual-strategy retrieval |
| **Safety, Guardrails & Caching** | Custom In-Memory LRU Cache, Prompt Injection Guardrails | 500-char input validation, adversarial injection refusal, < 2ms cached responses, token & latency telemetry |
| **User Interface** | Streamlit, Requests | Dual-mode chat interface, statutory 4-pillar eligibility evaluation form, citation rendering, feedback capture |
| **DevOps & Quality Assurance** | Docker, Docker Compose, GitHub Actions (CI), Render (CD), Pytest, Ruff | Automated linting, 25-test regression suite, multi-container orchestration, continuous deployment from `main` |

---

## Core Engineering Accomplishments

### 1. High-Precision RAG with Zero-Hallucination Guardrails
- Engineered a modular RAG pipeline in `app/rag.py` utilizing ChromaDB and `all-MiniLM-L6-v2` embeddings with structured metadata (`source`, `page`, `title`, `record_id`).
- Implemented a strict cosine similarity cutoff ($0.48$) and adversarial pattern detector to eliminate hallucinations on out-of-scope or speculative queries (e.g., NASA subsidies, arbitrary cash grants).
- **Result:** Achieved **100% accuracy** on a 15-question benchmark evaluation set (compared to 80% on baseline RAG), with 100% citation rate linking directly to official government gazettes.

### 2. Stateful Agentic Workflows & Human-in-the-Loop (HITL) Safety
- Architected an agentic engine using LangGraph with graph-based control flow and `MemorySaver` state checkpointer for multi-turn conversational context.
- Implemented human-in-the-loop approval gates that automatically interrupt execution before mutating state or persisting registration applications (`data/applications.json`), resuming seamlessly upon human confirmation (`approved=True`).
- Designed a custom ReAct fallback loop (`app/agent_loop.py`) for deterministic domain tool execution (`check_dpiit_eligibility`, `get_scheme_details`, `query_rag`, `submit_dpiit_application`).

### 3. Production Performance & Latency Optimization
- Built an in-memory query cache for the `/ask` endpoint, drastically slashing response times from $\approx 210\text{ ms}$ (uncached ChromaDB embedding and vector search) to $< 1.5\text{ ms}$ on cache hits (**99.2% latency reduction**).
- Implemented real-time token consumption estimation (prompt tokens, completion tokens, total tokens) and latency tracking logged per request for observability and cost governance.
- Hardened the public gateway with strict input validation limits (capped at 500 characters) and prompt-injection mitigations, neutralizing adversarial jailbreaks (`system override`, `ignore previous instructions`).

### 4. Interactive Full-Stack User Experience
- Built an interactive Streamlit UI (`ui/app.py`) featuring a signature **'Am I a startup?'** form evaluating the 4 statutory criteria under Ministry of Commerce Gazette Notification G.S.R. 127(E):
  1. Statutory entity type (Pvt Ltd, LLP, Partnership)
  2. Operational age ($\le 10$ years)
  3. Annual turnover threshold ($\le ₹100\text{ Cr}$)
  4. Innovation & scalable business model
- Rendered inline government citations with deep links and interactive approval buttons for agent actions, alongside a persistent feedback rating system (`data/feedback.json`).

### 5. Production DevOps, CI/CD & Cloud Deployment
- Containerized the full application stack using production `Dockerfile` and `docker-compose.yml` linking the API backend and Streamlit frontend.
- Created an automated GitHub Actions CI pipeline (`.github/workflows/ci.yml`) enforcing `ruff check .` and executing 25 unit/integration tests on every push and pull request.
- Configured Continuous Deployment (CD) from `main` to Render via `render.yaml`, maintaining live public endpoints for API health, Swagger documentation, and the Streamlit UI.

---

## Production Metrics Summary

| Metric | Uncached Pipeline | In-Memory Cached Pipeline | Improvement / Benchmark |
|---|---|---|---|
| **Response Latency** | $\approx 185 - 240\text{ ms}$ | $< 1.5\text{ ms}$ | **99.2% Latency Reduction** |
| **P95 Latency** | $220\text{ ms}$ | $< 2\text{ ms}$ | High-concurrency stability |
| **Token Consumption** | $\approx 210$ tokens / query | $0$ tokens (Cached) | **100% Token & Cost Savings on Repeat Queries** |
| **Refusal Accuracy** | $100.0\%$ | $100.0\%$ | 0% Hallucinations on adversarial / unanswerable queries |
| **Citation Fidelity** | $100.0\%$ | $100.0\%$ | All answers cite official Gazette / Startup India URLs |
| **Input Security Limit** | 500 characters | 500 characters | HTTP 400 Bad Request on oversized payloads |
| **Automated Test Coverage**| 25 Tests Passing | 25 Tests Passing | 100% Green in CI pipeline |

---

## Ready-to-Use Resume Bullet Points

### Option A: AI / GenAI Software Engineer
- **Engineered StartupSetu**, an agentic AI advisory platform using **FastAPI, LangGraph, ChromaDB, and Streamlit**, delivering verified startup compliance guidance with 100% citation accuracy.
- **Implemented a strict-refusal RAG pipeline** using Sentence Transformers and cosine similarity thresholds ($0.48$), eliminating hallucinations on out-of-scope policies and adversarial prompt injections.
- **Designed a stateful LangGraph agent** with `MemorySaver` and human-in-the-loop (HITL) approval gates to safely govern mutating startup registration actions.
- **Optimized API latency by 99%** ($210\text{ms} \rightarrow <2\text{ms}$) by implementing an in-memory query cache with per-request token estimation and latency telemetry.
- **Automated CI/CD workflows** with GitHub Actions and Docker Compose, achieving 100% pass rates across 25 unit/integration tests and deploying to Render.

### Option B: Backend & Machine Learning Systems Engineer
- **Built production RAG & Agent backend** in Python/FastAPI for Startup India advisory services, integrating dense vector retrieval, custom domain tools, and prompt defense mechanisms.
- **Developed low-latency query caching and security guardrails**, capping inputs at 500 characters and neutralizing prompt injection attacks (`system override`, `ignore previous instructions`).
- **Constructed statutory evaluation tools** assessing company incorporation dates, entity structures, and turnover limits based on Gazette Notification G.S.R. 127(E).
- **Established enterprise CI/CD standards** with Ruff linting, Pytest test suites, multi-stage Docker builds, and Render continuous deployment.
