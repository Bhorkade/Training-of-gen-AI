
import json
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

from app.llm import generate_response
from app.records import load_records, get_by_id
from app.smart_search import smart_search
from app.vectorstore import semantic_search as vector_semantic_search

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
            detail=f"Semantic search error: {str(error)}"
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
            detail=f"AI service error: {str(error)}"
        )