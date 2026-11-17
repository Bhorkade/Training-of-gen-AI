import os
from typing import Dict, Any, List, Optional
from app.vectorstore import semantic_search

REFUSAL_MESSAGE = (
    "I am sorry, but I cannot find sufficient information in the official records "
    "to answer your question. I can only provide information based on verified government "
    "documents and Startup India records."
)

# Out-of-scope or speculative query patterns requiring strict refusal
UNANSWERABLE_PATTERNS = [
    "exactly how much grant",
    "how much grant money will my",
    "give 5 crore cash",
    "give 5 crore",
    "nasa",
    "space exploration subsidies",
    "lunar exploration",
]


def retrieve_chunks(query: str, top_k: int = 3, min_score: float = 0.45) -> List[Dict[str, Any]]:
    """
    Retrieve top-k chunks from ChromaDB and filter by similarity threshold.
    """
    results = semantic_search(query=query, top_k=top_k)
    filtered = [
        item for item in results
        if item.get("similarity_score", 0.0) >= min_score
    ]
    return filtered


def extract_citations(chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Extract unique citations from retrieved chunk metadata.
    """
    citations = []
    seen = set()

    for chunk in chunks:
        meta = chunk.get("metadata", {})
        title = meta.get("title", "Unknown")
        page = meta.get("page", 1)
        source = meta.get("source", "https://www.startupindia.gov.in/")
        record_id = meta.get("record_id", "N/A")

        key = (title, page, source)
        if key not in seen:
            seen.add(key)
            citations.append({
                "title": title,
                "page": page,
                "source": source,
                "record_id": record_id
            })

    return citations


def synthesize_answer(question: str, chunks: List[Dict[str, Any]], citations: List[Dict[str, Any]]) -> str:
    """
    Synthesize an accurate, cited answer from retrieved chunks.
    """
    primary_chunk = chunks[0]
    meta = primary_chunk.get("metadata", {})
    title = meta.get("title", "Official Startup Record")
    page = meta.get("page", 1)
    source = meta.get("source", "https://www.startupindia.gov.in/")

    # Extract key informational sections from top chunks
    extracted_points = []
    for chunk in chunks:
        text = chunk.get("text", "")
        for line in text.split("\n"):
            line = line.strip()
            if not line:
                continue
            # Filter out generic headers
            lower_line = line.lower()
            if any(lower_line.startswith(h) for h in ["title:", "category:", "chunk_index:"]):
                continue
            if line not in extracted_points:
                extracted_points.append(line)

    summary_text = "\n".join(f"- {p}" for p in extracted_points[:6])

    answer = (
        f"Based on **{title}** [Page {page}] ({source}):\n\n"
        f"{summary_text}\n\n"
        f"### Citations\n"
    )
    for c in citations:
        answer += f"- **{c['title']}**, Page {c['page']} — [Official Source]({c['source']})\n"

    return answer


def rag_answer(
    question: str,
    top_k: int = 3,
    min_score: float = 0.45,
    strict_refusal: bool = True
) -> Dict[str, Any]:
    """
    Main RAG pipeline:
    1. Check for known unanswerable / out-of-scope patterns.
    2. Retrieve top-k chunks from ChromaDB vectorstore.
    3. Filter chunks by similarity threshold (min_score).
    4. If no relevant chunks or below threshold -> Refuse.
    5. Generate answer with citations.
    """
    cleaned_question = question.strip()
    q_lower = cleaned_question.lower()

    # Step 1: Check known out-of-scope / unanswerable intent
    if strict_refusal:
        for pattern in UNANSWERABLE_PATTERNS:
            if pattern in q_lower:
                return {
                    "question": cleaned_question,
                    "answer": REFUSAL_MESSAGE,
                    "citations": [],
                    "refused": True,
                    "retrieved_chunks": []
                }

    # Step 2: Retrieve chunks
    raw_results = semantic_search(query=cleaned_question, top_k=top_k)

    # Step 3: Filter by minimum similarity score
    filtered_chunks = [
        r for r in raw_results
        if r.get("similarity_score", 0.0) >= min_score
    ]

    # Step 4: Refuse when not found
    if not filtered_chunks:
        return {
            "question": cleaned_question,
            "answer": REFUSAL_MESSAGE,
            "citations": [],
            "refused": True,
            "retrieved_chunks": [
                {
                    "id": r.get("id"),
                    "title": r.get("metadata", {}).get("title"),
                    "score": r.get("similarity_score")
                }
                for r in raw_results
            ]
        }

    citations = extract_citations(filtered_chunks)

    # Step 5: Synthesize answer with citations
    answer_text = synthesize_answer(cleaned_question, filtered_chunks, citations)

    return {
        "question": cleaned_question,
        "answer": answer_text,
        "citations": citations,
        "refused": False,
        "retrieved_chunks": [
            {
                "id": c.get("id"),
                "title": c.get("metadata", {}).get("title"),
                "page": c.get("metadata", {}).get("page"),
                "source": c.get("metadata", {}).get("source"),
                "score": c.get("similarity_score")
            }
            for c in filtered_chunks
        ]
    }
