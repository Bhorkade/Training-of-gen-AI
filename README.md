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

## Project Status
Semantic search and prompt evaluation successfully completed. Project development is ongoing.

## Developer
Shrikar Bhorkade
