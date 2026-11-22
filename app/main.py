import json
import logging
import time
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

from app.graph import run_graph_agent
from app.llm import generate_response
from app.rag import rag_answer
from app.records import get_by_id, load_records
from app.smart_search import smart_search
from app.tools import check_dpiit_eligibility
from app.vectorstore import semantic_search as vector_semantic_search

# --------------------------------------------------
# LOGGING CONFIGURATION & IN-MEMORY CACHE
# --------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("startupsetu")

# In-memory query cache for RAG /ask endpoint: {(normalized_query, top_k): response_data}
ASK_CACHE: dict[tuple[str, int], dict[str, Any]] = {}
MAX_INPUT_LENGTH = 500

# --------------------------------------------------
# APPLICATION CONFIGURATION
# --------------------------------------------------

app = FastAPI(title="StartupSetu API")

BASE_DIR = Path(__file__).resolve().parent.parent

QUESTIONS_FILE = BASE_DIR / "data" / "questions.json"
PROMPTS_DIR = BASE_DIR / "prompts"

# --------------------------------------------------
# REQUEST MODELS
# --------------------------------------------------

class QuestionRequest(BaseModel):
    question: str

class ChatRequest(BaseModel):
    question: str

class AskRequest(BaseModel):
    question: str | None = None
    query: str | None = None
    top_k: int = 3

class AgentRequest(BaseModel):
    query: str | None = None
    message: str | None = None
    thread_id: str | None = None
    approved: bool | None = None

class EligibilityRequest(BaseModel):
    entity_type: str
    incorporation_year: int | None = None
    incorporation_date: str | None = None
    annual_turnover_cr: float = 0.0
    is_innovative: bool = True



# --------------------------------------------------
# PROMPT LOADER
# --------------------------------------------------

def read_prompt(filename: str) -> str:

    prompt_path = PROMPTS_DIR / filename

    if not prompt_path.exists():
        raise FileNotFoundError(
            f"Prompt file not found: {filename}"
        )

    return prompt_path.read_text(encoding="utf-8")

# --------------------------------------------------
# HEALTH CHECK
# GET /health
# --------------------------------------------------

@app.get("/health")
def health():

    return {
        "status": "healthy",
        "message": "StartupSetu API is running"
    }

# --------------------------------------------------
# GET ALL RECORDS
# GET /records?limit=5
# --------------------------------------------------

@app.get("/records")
def get_records(limit: int = Query(default=10, ge=1)):

    records = load_records()

    return records[:limit]

# --------------------------------------------------
# GET RECORD BY ID
# GET /records/{record_id}
# --------------------------------------------------

@app.get("/records/{record_id}")
def get_record(record_id: str):

    records = load_records()

    record = get_by_id(records, record_id)

    if record is None:
        raise HTTPException(
            status_code=404,
            detail="Record not found"
        )

    return record

# --------------------------------------------------
# KEYWORD SEARCH
# GET /search?q=startup
# --------------------------------------------------

@app.get("/search")
def search_records(q: str = Query(..., min_length=1)):

    records = load_records()

    results = smart_search(records, q)

    return {
        "question": q,
        "total_results": len(results),
        "results": results
    }

# --------------------------------------------------
# SEMANTIC SEARCH
# GET /search/semantic?q=startup funding
# --------------------------------------------------

@app.get("/search/semantic")
def semantic_search_endpoint(
    q: str = Query(..., min_length=1),
    top_k: int = Query(default=3, ge=1, le=10)
):

    try:

        results = vector_semantic_search(
            query=q,
            top_k=top_k
        )

        return {
            "question": q,
            "search_type": "semantic",
            "total_results": len(results),
            "results": results
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"Semantic search error: {error!s}"
        )

# --------------------------------------------------
# SAVE USER QUESTION
# POST /questions
# --------------------------------------------------

@app.post("/questions")
def save_question(request: QuestionRequest):

    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty"
        )

    QUESTIONS_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    if QUESTIONS_FILE.exists():

        try:

            with open(
                QUESTIONS_FILE,
                "r",
                encoding="utf-8"
            ) as file:

                questions = json.load(file)

        except json.JSONDecodeError:

            raise HTTPException(
                status_code=500,
                detail="Invalid JSON in questions.json"
            )

    else:
        questions = []

    new_question = {
        "id": len(questions) + 1,
        "question": question
    }

    questions.append(new_question)

    with open(
        QUESTIONS_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            questions,
            file,
            indent=4,
            ensure_ascii=False
        )

    return {
        "message": "Question saved successfully",
        "data": new_question
    }

# --------------------------------------------------
# SELECT TASK PROMPT
# --------------------------------------------------

def select_task_prompt(question: str) -> str:

    question_lower = question.lower()

    dpiit_keywords = [
        "dpiit",
        "recognition",
        "eligibility",
        "startup registration",
        "recognition certificate"
    ]

    if any(
        keyword in question_lower
        for keyword in dpiit_keywords
    ):

        return read_prompt("dpiit_recognition.txt")

    return read_prompt("schemes_benefits.txt")

# --------------------------------------------------
# AI CHAT
# POST /chat
# --------------------------------------------------

@app.post("/chat")
def chat(request: ChatRequest):

    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty"
        )

    try:

        # STEP 1: Load system prompt

        system_prompt = read_prompt("system.txt")

        # STEP 2: Select task prompt

        task_prompt = select_task_prompt(question)

        # STEP 3: Load project records

        records = load_records()

        # STEP 4: Find relevant records

        relevant_records = smart_search(
            records,
            question
        )

        # STEP 5: Prepare context

        context = json.dumps(
            relevant_records,
            indent=2,
            ensure_ascii=False
        )

        # STEP 6: Build final Gemini prompt

        final_prompt = f"""
{system_prompt}

{task_prompt}

Relevant project information:

{context}

User question:

{question}

Instructions:
- Answer using simple English.
- Use relevant project information.
- Do not invent facts or government benefits.
- If information is insufficient, clearly mention it.
- Give a useful and understandable answer.
- Prefer official government information.
"""

        # STEP 7: Generate Gemini response

        answer = generate_response(final_prompt)

        # STEP 8: Return response

        return {
            "answer": answer,
            "confidence": "medium",
            "follow_up": (
                "Would you like to explore related "
                "startup benefits and government schemes?"
            )
        }

    except FileNotFoundError as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )

    except Exception as error:

        raise HTTPException(
            status_code=502,
            detail=f"AI service error: {error!s}"
        )

# --------------------------------------------------
# RAG ASK ENDPOINT
# POST /ask
# --------------------------------------------------

@app.post("/ask")
def ask(request: AskRequest):
    start_time = time.perf_counter()
    q = (request.question or request.query or "").strip()

    if not q:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty"
        )

    if len(q) > MAX_INPUT_LENGTH:
        raise HTTPException(
            status_code=400,
            detail=f"Query exceeds maximum allowed length of {MAX_INPUT_LENGTH} characters"
        )

    cache_key = (q.lower(), request.top_k)

    if cache_key in ASK_CACHE:
        cached_result = ASK_CACHE[cache_key]
        latency_ms = round((time.perf_counter() - start_time) * 1000, 2)
        prompt_tokens = max(1, len(q) // 4)
        completion_tokens = max(1, len(str(cached_result.get("answer", ""))) // 4)
        total_tokens = prompt_tokens + completion_tokens

        logger.info(
            "[/ask] query='%s' latency_ms=%.2f prompt_tokens=%d completion_tokens=%d total_tokens=%d cached=True",
            q[:40],
            latency_ms,
            prompt_tokens,
            completion_tokens,
            total_tokens,
        )

        response_data = dict(cached_result)
        response_data["metrics"] = {
            "latency_ms": latency_ms,
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": total_tokens,
            "cached": True
        }
        return response_data

    try:
        response = rag_answer(
            question=q,
            top_k=request.top_k
        )
        latency_ms = round((time.perf_counter() - start_time) * 1000, 2)
        prompt_tokens = max(1, len(q) // 4)
        completion_tokens = max(1, len(str(response.get("answer", ""))) // 4)
        total_tokens = prompt_tokens + completion_tokens

        logger.info(
            "[/ask] query='%s' latency_ms=%.2f prompt_tokens=%d completion_tokens=%d total_tokens=%d cached=False",
            q[:40],
            latency_ms,
            prompt_tokens,
            completion_tokens,
            total_tokens,
        )

        if len(ASK_CACHE) >= 128:
            oldest_key = next(iter(ASK_CACHE))
            del ASK_CACHE[oldest_key]

        response["metrics"] = {
            "latency_ms": latency_ms,
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": total_tokens,
            "cached": False
        }
        ASK_CACHE[cache_key] = dict(response)
        return response

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"RAG processing error: {error!s}"
        )

# --------------------------------------------------
# LANGGRAPH AGENT ENDPOINT
# POST /agent
# --------------------------------------------------

@app.post("/agent")
def agent_endpoint(request: AgentRequest):
    user_query = (request.query or request.message or "").strip()

    if not user_query and request.approved is None:
        raise HTTPException(
            status_code=400,
            detail="Query or approval decision must be provided"
        )

    try:
        response = run_graph_agent(
            query=user_query,
            thread_id=request.thread_id,
            approved=request.approved
        )
        return response

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Agent execution error: {error!s}"
        )

# --------------------------------------------------
# DPIIT ELIGIBILITY TOOL ENDPOINT
# POST /eligibility
# --------------------------------------------------

@app.post("/eligibility")
def check_eligibility_endpoint(request: EligibilityRequest):
    try:
        response = check_dpiit_eligibility(
            entity_type=request.entity_type,
            incorporation_year=request.incorporation_year,
            annual_turnover_cr=request.annual_turnover_cr,
            is_innovative=request.is_innovative,
            incorporation_date=request.incorporation_date
        )
        return response

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Eligibility evaluation error: {error!s}"
        )


