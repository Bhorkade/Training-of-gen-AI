# StartupSetu – AI-Powered Startup Guidance Platform

## 1. Project Overview
StartupSetu is an AI-powered platform designed to help students and new entrepreneurs understand the process of starting and registering a startup in India.

The platform provides information about DPIIT Startup Recognition, government benefits, funding opportunities, tax exemptions, and Maharashtra startup incentives.

## 2. Problem Statement
Many students and new entrepreneurs face difficulties understanding startup registration procedures, government policies, available funding schemes, and eligibility requirements.

## 3. Project Objectives
- Explain DPIIT Startup Recognition.
- Provide information about government startup schemes.
- Help founders understand tax benefits and IPR support.
- Provide information about Maharashtra startup incentives.
- Compare Private Limited Company and LLP.
- Help entrepreneurs identify suitable funding opportunities.
- Provide reliable information with official government references.

## 4. Proposed Solution
StartupSetu will use Artificial Intelligence to understand user questions and provide relevant startup information based on official government documents and policies.

## 5. Target Users
- College students
- New entrepreneurs
- Startup founders
- Early-stage businesses

## 6. Technologies Used
- Python
- Artificial Intelligence
- Large Language Models (LLMs)
- Retrieval-Augmented Generation (RAG)
- Database
- Government documents and datasets

## 7. Data Sources
- Startup India
- DPIIT official resources
- Maharashtra Startup Policy
- Government startup schemes and guidelines

## 8. Example Use Case
Two final-year students from Sanjivani University want to establish an agricultural drone-spraying startup.

StartupSetu will help them understand business registration options, DPIIT recognition, government benefits, funding schemes, and Maharashtra-specific incentives.

## 9. Project Development Plan
1. Python fundamentals
2. Data collection and processing
3. Government document integration
4. AI model integration
5. RAG-based question-answering system
6. User interface development
7. Testing and deployment

## 10. Project Status
Currently under development.

## 11. Developer
Shrikar Bhorkade

## 12. Project Vision
To make startup registration, government benefits, and funding information easier to understand and access through Artificial Intelligence.

Day 01 – Project Introduction

Created the StartupSetu project.

Defined the problem statement and project objectives.

Planned the basic project structure.

Day 02 – Startup Data Collection

Created sample startup-related records using Python.

Stored records as a list of dictionaries.

Added keyword-based search functionality.

Implemented category-wise record counting.

Completed Tasks

Added a real government CSV dataset to data/raw/.

Created app/ingest.py for CSV data ingestion.

Implemented data cleaning and record conversion.

Added exception handling for problematic rows.

Converted cleaned CSV records into JSON.

Saved processed data in data/records.json.

Updated load_records() to read records from JSON.

Integrated JSON data with the StartupSetu CLI.

Technologies Used

Python

CSV

JSON

Exception Handling

File Handling

Project Progress

StartupSetu now supports importing real-world data and converting it into a structured format for further processing and AI-powered startup guidance.
# StartupSetu – Daily Progress

## Day 04 – FastAPI Development
- Created a FastAPI application.
- Added APIs for health check and startup records.
- Implemented search functionality.
- Added endpoints to retrieve startup information.

## Day 05 – Smart Search
- Implemented smart search using TF-IDF.
- Used cosine similarity to find relevant records.
- Tested search with 10 sample questions.
- Improved the process of finding relevant startup information.

## Day 06 – Semantic Search with ChromaDB

### Objective
Implement semantic search to retrieve relevant StartupSetu records based on the meaning of a user's query.

### Tasks Completed
- Implemented document chunking using `app/chunking.py`.
- Split startup records into smaller chunks.
- Added metadata such as record ID, title, category, and chunk index.
- Used Sentence Transformers (`all-MiniLM-L6-v2`) to generate text embeddings.
- Stored document embeddings in a persistent ChromaDB vector database.
- Implemented semantic similarity search using cosine distance.
- Created `app/vectorstore.py` to manage indexing and searching.

### Technologies Used
- Python
- Sentence Transformers
- ChromaDB
- Vector Embeddings
- Semantic Search

### Outcome
Successfully implemented semantic search to retrieve relevant startup-related information based on the meaning of user queries.

---

## Day 07 – Semantic Search API Integration

### Objective
Integrate semantic search into the FastAPI application and make it accessible through an API endpoint.

### Tasks Completed
- Integrated the semantic search function into `app/main.py`.
- Created a new GET endpoint: `/search/semantic`.
- Added query parameter `q` to accept user questions.
- Added `top_k` parameter to control the number of search results.
- Tested the API using FastAPI Swagger documentation.
- Verified successful API responses with HTTP 200 OK.
- Updated project dependencies and prepared the code for GitHub.

### Technologies Used
- Python
- FastAPI
- ChromaDB
- Sentence Transformers
- REST API
- Swagger UI

### API Endpoint

**GET** `/search/semantic?q=What is DPIIT Startup Recognition?&top_k=3`

### Outcome
Successfully integrated semantic search with FastAPI.
## Day 06 – Semantic Search with ChromaDB

### Objective
Implement semantic search to retrieve relevant StartupSetu records based on the meaning of a user's query.

### Tasks Completed
- Implemented document chunking using `app/chunking.py`.
- Split startup records into smaller chunks.
- Added metadata such as record ID, title, category, and chunk index.
- Used Sentence Transformers (`all-MiniLM-L6-v2`) to generate text embeddings.
- Stored document embeddings in a persistent ChromaDB vector database.
- Implemented semantic similarity search using cosine distance.
- Created `app/vectorstore.py` to manage indexing and searching.

### Technologies Used
- Python
- Sentence Transformers
- ChromaDB
- Vector Embeddings
- Semantic Search

### Outcome
Successfully implemented semantic search to retrieve relevant startup-related information based on the meaning of user queries.

---

## Day 07 – Semantic Search API Integration

### Objective
Integrate semantic search into the FastAPI application and make it accessible through an API endpoint.

### Tasks Completed
- Integrated the semantic search function into `app/main.py`.
- Created a new GET endpoint: `/search/semantic`.
- Added query parameter `q` to accept user questions.
- Added `top_k` parameter to control the number of search results.
- Tested the API using FastAPI Swagger documentation.
- Verified successful API responses with HTTP 200 OK.
- Updated project dependencies and prepared the code for GitHub.

### Technologies Used
- Python
- FastAPI
- ChromaDB
- Sentence Transformers
- REST API
- Swagger UI

### API Endpoint

**GET** `/search/semantic?q=What is DPIIT Startup Recognition?&top_k=3`

### Outcome
Successfully integrated semantic search with FastAPI.
## Day 06 – Semantic Search with ChromaDB

### Objective
Implement semantic search to retrieve relevant StartupSetu records based on the meaning of a user's query.

### Tasks Completed
- Implemented document chunking using `app/chunking.py`.
- Split startup records into smaller chunks.
- Added metadata such as record ID, title, category, and chunk index.
- Used Sentence Transformers (`all-MiniLM-L6-v2`) to generate text embeddings.
- Stored document embeddings in a persistent ChromaDB vector database.
- Implemented semantic similarity search using cosine distance.
- Created `app/vectorstore.py` to manage indexing and searching.

### Technologies Used
- Python
- Sentence Transformers
- ChromaDB
- Vector Embeddings
- Semantic Search

### Outcome
Successfully implemented semantic search to retrieve relevant startup-related information based on the meaning of user queries.

---

## Day 07 – Semantic Search API Integration

### Objective
Integrate semantic search into the FastAPI application and make it accessible through an API endpoint.

### Tasks Completed
- Integrated the semantic search function into `app/main.py`.
- Created a new GET endpoint: `/search/semantic`.
- Added query parameter `q` to accept user questions.
- Added `top_k` parameter to control the number of search results.
- Tested the API using FastAPI Swagger documentation.
- Verified successful API responses with HTTP 200 OK.
- Updated project dependencies and prepared the code for GitHub.

### Technologies Used
- Python
- FastAPI
- ChromaDB
- Sentence Transformers
- REST API
- Swagger UI

### API Endpoint

**GET** `/search/semantic?q=What is DPIIT Startup Recognition?&top_k=3`

### Outcome
Successfully integrated semantic search with FastAPI.
## Day 06 – Semantic Search with ChromaDB

### Objective
Implement semantic search to retrieve relevant StartupSetu records based on the meaning of a user's query.

### Tasks Completed
- Implemented document chunking using `app/chunking.py`.
- Split startup records into smaller chunks.
- Added metadata such as record ID, title, category, and chunk index.
- Used Sentence Transformers (`all-MiniLM-L6-v2`) to generate text embeddings.
- Stored document embeddings in a persistent ChromaDB vector database.
- Implemented semantic similarity search using cosine distance.
- Created `app/vectorstore.py` to manage indexing and searching.

### Technologies Used
- Python
- Sentence Transformers
- ChromaDB
- Vector Embeddings
- Semantic Search

### Outcome
Successfully implemented semantic search to retrieve relevant startup-related information based on the meaning of user queries.

---

## Day 07 – Semantic Search API Integration

### Objective
Integrate semantic search into the FastAPI application and make it accessible through an API endpoint.

### Tasks Completed
- Integrated the semantic search function into `app/main.py`.
- Created a new GET endpoint: `/search/semantic`.
- Added query parameter `q` to accept user questions.
- Added `top_k` parameter to control the number of search results.
- Tested the API using FastAPI Swagger documentation.
- Verified successful API responses with HTTP 200 OK.
- Updated project dependencies and prepared the code for GitHub.

### Technologies Used
- Python
- FastAPI
- ChromaDB
- Sentence Transformers
- REST API
- Swagger UI

### API Endpoint

**GET** `/search/semantic?q=What is DPIIT Startup Recognition?&top_k=3`

### Outcome
Successfully integrated semantic search with FastAPI.
## Day 06 – Semantic Search with ChromaDB

### Objective
Implement semantic search to retrieve relevant StartupSetu records based on the meaning of a user's query.

### Tasks Completed
- Implemented document chunking using `app/chunking.py`.
- Split startup records into smaller chunks.
- Added metadata such as record ID, title, category, and chunk index.
- Used Sentence Transformers (`all-MiniLM-L6-v2`) to generate text embeddings.
- Stored document embeddings in a persistent ChromaDB vector database.
- Implemented semantic similarity search using cosine distance.
- Created `app/vectorstore.py` to manage indexing and searching.

### Technologies Used
- Python
- Sentence Transformers
- ChromaDB
- Vector Embeddings
- Semantic Search

### Outcome
Successfully implemented semantic search to retrieve relevant startup-related information based on the meaning of user queries.

---

## Day 07 – Semantic Search API Integration

### Objective
Integrate semantic search into the FastAPI application and make it accessible through an API endpoint.

### Tasks Completed
- Integrated the semantic search function into `app/main.py`.
- Created a new GET endpoint: `/search/semantic`.
- Added query parameter `q` to accept user questions.
- Added `top_k` parameter to control the number of search results.
- Tested the API using FastAPI Swagger documentation.
- Verified successful API responses with HTTP 200 OK.
- Updated project dependencies and prepared the code for GitHub.

### Technologies Used
- Python
- FastAPI
- ChromaDB
- Sentence Transformers
- REST API
- Swagger UI

### API Endpoint

**GET** `/search/semantic?q=What is DPIIT Startup Recognition?&top_k=3`

### Outcome
Successfully integrated semantic search with FastAPI.
## Day 06 – Semantic Search with ChromaDB

### Objective
Implement semantic search to retrieve relevant StartupSetu records based on the meaning of a user's query.

### Tasks Completed
- Implemented document chunking using `app/chunking.py`.
- Split startup records into smaller chunks.
- Added metadata such as record ID, title, category, and chunk index.
- Used Sentence Transformers (`all-MiniLM-L6-v2`) to generate text embeddings.
- Stored document embeddings in a persistent ChromaDB vector database.
- Implemented semantic similarity search using cosine distance.
- Created `app/vectorstore.py` to manage indexing and searching.

### Technologies Used
- Python
- Sentence Transformers
- ChromaDB
- Vector Embeddings
- Semantic Search

### Outcome
Successfully implemented semantic search to retrieve relevant startup-related information based on the meaning of user queries.

---

## Day 07 – Semantic Search API Integration

### Objective
Integrate semantic search into the FastAPI application and make it accessible through an API endpoint.

### Tasks Completed
- Integrated the semantic search function into `app/main.py`.
- Created a new GET endpoint: `/search/semantic`.
- Added query parameter `q` to accept user questions.
- Added `top_k` parameter to control the number of search results.
- Tested the API using FastAPI Swagger documentation.
- Verified successful API responses with HTTP 200 OK.
- Updated project dependencies and prepared the code for GitHub.

### Technologies Used
- Python
- FastAPI
- ChromaDB
- Sentence Transformers
- REST API
- Swagger UI

### API Endpoint

**GET** `/search/semantic?q=What is DPIIT Startup Recognition?&top_k=3`

### Outcome
Successfully integrated semantic search with FastAPI.
## Day 06 – Semantic Search with ChromaDB

### Objective
Implement semantic search to retrieve relevant StartupSetu records based on the meaning of a user's query.

### Tasks Completed
- Implemented document chunking using `app/chunking.py`.
- Split startup records into smaller chunks.
- Added metadata such as record ID, title, category, and chunk index.
- Used Sentence Transformers (`all-MiniLM-L6-v2`) to generate text embeddings.
- Stored document embeddings in a persistent ChromaDB vector database.
- Implemented semantic similarity search using cosine distance.
- Created `app/vectorstore.py` to manage indexing and searching.

### Technologies Used
- Python
- Sentence Transformers
- ChromaDB
- Vector Embeddings
- Semantic Search

### Outcome
Successfully implemented semantic search to retrieve relevant startup-related information based on the meaning of user queries.

---

## Day 07 – Semantic Search API Integration

### Objective
Integrate semantic search into the FastAPI application and make it accessible through an API endpoint.

### Tasks Completed
- Integrated the semantic search function into `app/main.py`.
- Created a new GET endpoint: `/search/semantic`.
- Added query parameter `q` to accept user questions.
- Added `top_k` parameter to control the number of search results.
- Tested the API using FastAPI Swagger documentation.
- Verified successful API responses with HTTP 200 OK.
- Updated project dependencies and prepared the code for GitHub.

### Technologies Used
- Python
- FastAPI
- ChromaDB
- Sentence Transformers
- REST API
- Swagger UI

### API Endpoint

**GET** `/search/semantic?q=What is DPIIT Startup Recognition?&top_k=3`

### Outcome
Successfully integrated semantic search with FastAPI.
## Day 06 – Semantic Search with ChromaDB

### Objective
Implement semantic search to retrieve relevant StartupSetu records based on the meaning of a user's query.

### Tasks Completed
- Implemented document chunking using `app/chunking.py`.
- Split startup records into smaller chunks.
- Added metadata such as record ID, title, category, and chunk index.
- Used Sentence Transformers (`all-MiniLM-L6-v2`) to generate text embeddings.
- Stored document embeddings in a persistent ChromaDB vector database.
- Implemented semantic similarity search using cosine distance.
- Created `app/vectorstore.py` to manage indexing and searching.

### Technologies Used
- Python
- Sentence Transformers
- ChromaDB
- Vector Embeddings
- Semantic Search

### Outcome
Successfully implemented semantic search to retrieve relevant startup-related information based on the meaning of user queries.

---

## Day 07 – Semantic Search API Integration

### Objective
Integrate semantic search into the FastAPI application and make it accessible through an API endpoint.

### Tasks Completed
- Integrated the semantic search function into `app/main.py`.
- Created a new GET endpoint: `/search/semantic`.
- Added query parameter `q` to accept user questions.
- Added `top_k` parameter to control the number of search results.
- Tested the API using FastAPI Swagger documentation.
- Verified successful API responses with HTTP 200 OK.
- Updated project dependencies and prepared the code for GitHub.

### Technologies Used
- Python
- FastAPI
- ChromaDB
- Sentence Transformers
- REST API
- Swagger UI

### API Endpoint

**GET** `/search/semantic?q=What is DPIIT Startup Recognition?&top_k=3`

### Outcome
Successfully integrated semantic search with FastAPI.
## Day 06 – Semantic Search with ChromaDB

### Objective
Implement semantic search to retrieve relevant StartupSetu records based on the meaning of a user's query.

### Tasks Completed
- Implemented document chunking using `app/chunking.py`.
- Split startup records into smaller chunks.
- Added metadata such as record ID, title, category, and chunk index.
- Used Sentence Transformers (`all-MiniLM-L6-v2`) to generate text embeddings.
- Stored document embeddings in a persistent ChromaDB vector database.
- Implemented semantic similarity search using cosine distance.
- Created `app/vectorstore.py` to manage indexing and searching.

### Technologies Used
- Python
- Sentence Transformers
- ChromaDB
- Vector Embeddings
- Semantic Search

### Outcome
Successfully implemented semantic search to retrieve relevant startup-related information based on the meaning of user queries.

---

## Day 07 – Semantic Search API Integration

### Objective
Integrate semantic search into the FastAPI application and make it accessible through an API endpoint.

### Tasks Completed
- Integrated the semantic search function into `app/main.py`.
- Created a new GET endpoint: `/search/semantic`.
- Added query parameter `q` to accept user questions.
- Added `top_k` parameter to control the number of search results.
- Tested the API using FastAPI Swagger documentation.
- Verified successful API responses with HTTP 200 OK.
- Updated project dependencies and prepared the code for GitHub.

### Technologies Used
- Python
- FastAPI
- ChromaDB
- Sentence Transformers
- REST API
- Swagger UI

### API Endpoint

**GET** `/search/semantic?q=What is DPIIT Startup Recognition?&top_k=3`

### Outcome
Successfully integrated semantic search with FastAPI.tu – Daily Progress
## Day 06 – Semantic Search with ChromaDB

### Objective
Implement semantic search to retrieve relevant StartupSetu records based on the meaning of a user's query.

### Tasks Completed
- Implemented document chunking using `app/chunking.py`.
- Split startup records into smaller chunks.
- Added metadata such as record ID, title, category, and chunk index.
- Used Sentence Transformers (`all-MiniLM-L6-v2`) to generate text embeddings.
- Stored document embeddings in a persistent ChromaDB vector database.
- Implemented semantic similarity search using cosine distance.
- Created `app/vectorstore.py` to manage indexing and searching.

### Technologies Used
- Python
- Sentence Transformers
- ChromaDB
- Vector Embeddings
- Semantic Search

### Outcome
Successfully implemented semantic search to retrieve relevant startup-related information based on the meaning of user queries.

---

## Day 07 – Semantic Search API Integration

### Objective
Integrate semantic search into the FastAPI application and make it accessible through an API endpoint.

### Tasks Completed
- Integrated the semantic search function into `app/main.py`.
- Created a new GET endpoint: `/search/semantic`.
- Added query parameter `q` to accept user questions.
- Added `top_k` parameter to control the number of search results.
- Tested the API using FastAPI Swagger documentation.
- Verified successful API responses with HTTP 200 OK.
- Updated project dependencies and prepared the code for GitHub.

### Technologies Used
- Python
- FastAPI
- ChromaDB
- Sentence Transformers
- REST API
- Swagger UI

### API Endpoint

**GET** `/search/semantic?q=What is DPIIT Startup Recognition?&top_k=3`

### Outcome
Successfully integrated semantic search with FastAPI.
## Day 06 – Semantic Search with ChromaDB

### Objective
Implement semantic search to retrieve relevant StartupSetu records based on the meaning of a user's query.

### Tasks Completed
- Implemented document chunking using `app/chunking.py`.
- Split startup records into smaller chunks.
- Added metadata such as record ID, title, category, and chunk index.
- Used Sentence Transformers (`all-MiniLM-L6-v2`) to generate text embeddings.
- Stored document embeddings in a persistent ChromaDB vector database.
- Implemented semantic similarity search using cosine distance.
- Created `app/vectorstore.py` to manage indexing and searching.

### Technologies Used
- Python
- Sentence Transformers
- ChromaDB
- Vector Embeddings
- Semantic Search

### Outcome
Successfully implemented semantic search to retrieve relevant startup-related information based on the meaning of user queries.

---

## Day 07 – Semantic Search API Integration

### Objective
Integrate semantic search into the FastAPI application and make it accessible through an API endpoint.

### Tasks Completed
- Integrated the semantic search function into `app/main.py`.
- Created a new GET endpoint: `/search/semantic`.
- Added query parameter `q` to accept user questions.
- Added `top_k` parameter to control the number of search results.
- Tested the API using FastAPI Swagger documentation.
- Verified successful API responses with HTTP 200 OK.
- Updated project dependencies and prepared the code for GitHub.

### Technologies Used
- Python
- FastAPI
- ChromaDB
- Sentence Transformers
- REST API
- Swagger UI

### API Endpoint

**GET** `/search/semantic?q=What is DPIIT Startup Recognition?&top_k=3`

### Outcome
Successfully integrated semantic search with FastAPI.
## Day 06 – Semantic Search with ChromaDB

### Objective
Implement semantic search to retrieve relevant StartupSetu records based on the meaning of a user's query.

### Tasks Completed
- Implemented document chunking using `app/chunking.py`.
- Split startup records into smaller chunks.
- Added metadata such as record ID, title, category, and chunk index.
- Used Sentence Transformers (`all-MiniLM-L6-v2`) to generate text embeddings.
- Stored document embeddings in a persistent ChromaDB vector database.
- Implemented semantic similarity search using cosine distance.
- Created `app/vectorstore.py` to manage indexing and searching.

### Technologies Used
- Python
- Sentence Transformers
- ChromaDB
- Vector Embeddings
- Semantic Search

### Outcome
Successfully implemented semantic search to retrieve relevant startup-related information based on the meaning of user queries.

---

## Day 07 – Semantic Search API Integration

### Objective
Integrate semantic search into the FastAPI application and make it accessible through an API endpoint.

### Tasks Completed
- Integrated the semantic search function into `app/main.py`.
- Created a new GET endpoint: `/search/semantic`.
- Added query parameter `q` to accept user questions.
- Added `top_k` parameter to control the number of search results.
- Tested the API using FastAPI Swagger documentation.
- Verified successful API responses with HTTP 200 OK.
- Updated project dependencies and prepared the code for GitHub.

### Technologies Used
- Python
- FastAPI
- ChromaDB
- Sentence Transformers
- REST API
- Swagger UI

### API Endpoint

**GET** `/search/semantic?q=What is DPIIT Startup Recognition?&top_k=3`

### Outcome
Successfully integrated semantic search with FastAPI.
## Day 06 – Semantic Search with ChromaDB

### Objective
Implement semantic search to retrieve relevant StartupSetu records based on the meaning of a user's query.

### Tasks Completed
- Implemented document chunking using `app/chunking.py`.
- Split startup records into smaller chunks.
- Added metadata such as record ID, title, category, and chunk index.
- Used Sentence Transformers (`all-MiniLM-L6-v2`) to generate text embeddings.
- Stored document embeddings in a persistent ChromaDB vector database.
- Implemented semantic similarity search using cosine distance.
- Created `app/vectorstore.py` to manage indexing and searching.

### Technologies Used
- Python
- Sentence Transformers
- ChromaDB
- Vector Embeddings
- Semantic Search

### Outcome
Successfully implemented semantic search to retrieve relevant startup-related information based on the meaning of user queries.

---

## Day 07 – Semantic Search API Integration

### Objective
Integrate semantic search into the FastAPI application and make it accessible through an API endpoint.

### Tasks Completed
- Integrated the semantic search function into `app/main.py`.
- Created a new GET endpoint: `/search/semantic`.
- Added query parameter `q` to accept user questions.
- Added `top_k` parameter to control the number of search results.
- Tested the API using FastAPI Swagger documentation.
- Verified successful API responses with HTTP 200 OK.
- Updated project dependencies and prepared the code for GitHub.

### Technologies Used
- Python
- FastAPI
- ChromaDB
- Sentence Transformers
- REST API
- Swagger UI

### API Endpoint

**GET** `/search/semantic?q=What is DPIIT Startup Recognition?&top_k=3`

### Outcome
Successfully integrated semantic search with FastAPI.
## Day 06 – Semantic Search with ChromaDB

### Objective
Implement semantic search to retrieve relevant StartupSetu records based on the meaning of a user's query.

### Tasks Completed
- Implemented document chunking using `app/chunking.py`.
- Split startup records into smaller chunks.
- Added metadata such as record ID, title, category, and chunk index.
- Used Sentence Transformers (`all-MiniLM-L6-v2`) to generate text embeddings.
- Stored document embeddings in a persistent ChromaDB vector database.
- Implemented semantic similarity search using cosine distance.
- Created `app/vectorstore.py` to manage indexing and searching.

### Technologies Used
- Python
- Sentence Transformers
- ChromaDB
- Vector Embeddings
- Semantic Search

### Outcome
Successfully implemented semantic search to retrieve relevant startup-related information based on the meaning of user queries.

---

## Day 07 – Semantic Search API Integration

### Objective
Integrate semantic search into the FastAPI application and make it accessible through an API endpoint.

### Tasks Completed
- Integrated the semantic search function into `app/main.py`.
- Created a new GET endpoint: `/search/semantic`.
- Added query parameter `q` to accept user questions.
- Added `top_k` parameter to control the number of search results.
- Tested the API using FastAPI Swagger documentation.
- Verified successful API responses with HTTP 200 OK.
- Updated project dependencies and prepared the code for GitHub.

### Technologies Used
- Python
- FastAPI
- ChromaDB
- Sentence Transformers
- REST API
- Swagger UI

### API Endpoint

**GET** `/search/semantic?q=What is DPIIT Startup Recognition?&top_k=3`

### Outcome
Successfully integrated semantic search with FastAPI.
## Day 06 – Semantic Search with ChromaDB

### Objective
Implement semantic search to retrieve relevant StartupSetu records based on the meaning of a user's query.

### Tasks Completed
- Implemented document chunking using `app/chunking.py`.
- Split startup records into smaller chunks.
- Added metadata such as record ID, title, category, and chunk index.
- Used Sentence Transformers (`all-MiniLM-L6-v2`) to generate text embeddings.
- Stored document embeddings in a persistent ChromaDB vector database.
- Implemented semantic similarity search using cosine distance.
- Created `app/vectorstore.py` to manage indexing and searching.

### Technologies Used
- Python
- Sentence Transformers
- ChromaDB
- Vector Embeddings
- Semantic Search

### Outcome
Successfully implemented semantic search to retrieve relevant startup-related information based on the meaning of user queries.

---

## Day 07 – Semantic Search API Integration

### Objective
Integrate semantic search into the FastAPI application and make it accessible through an API endpoint.

### Tasks Completed
- Integrated the semantic search function into `app/main.py`.
- Created a new GET endpoint: `/search/semantic`.
- Added query parameter `q` to accept user questions.
- Added `top_k` parameter to control the number of search results.
- Tested the API using FastAPI Swagger documentation.
- Verified successful API responses with HTTP 200 OK.
- Updated project dependencies and prepared the code for GitHub.

### Technologies Used
- Python
- FastAPI
- ChromaDB
- Sentence Transformers
- REST API
- Swagger UI

### API Endpoint

**GET** `/search/semantic?q=What is DPIIT Startup Recognition?&top_k=3`

### Outcome
Successfully integrated semantic search with FastAPI.
## Day 06 – Semantic Search with ChromaDB

### Objective
Implement semantic search to retrieve relevant StartupSetu records based on the meaning of a user's query.

### Tasks Completed
- Implemented document chunking using `app/chunking.py`.
- Split startup records into smaller chunks.
- Added metadata such as record ID, title, category, and chunk index.
- Used Sentence Transformers (`all-MiniLM-L6-v2`) to generate text embeddings.
- Stored document embeddings in a persistent ChromaDB vector database.
- Implemented semantic similarity search using cosine distance.
- Created `app/vectorstore.py` to manage indexing and searching.

### Technologies Used
- Python
- Sentence Transformers
- ChromaDB
- Vector Embeddings
- Semantic Search

### Outcome
Successfully implemented semantic search to retrieve relevant startup-related information based on the meaning of user queries.

---

## Day 07 – Semantic Search API Integration

### Objective
Integrate semantic search into the FastAPI application and make it accessible through an API endpoint.

### Tasks Completed
- Integrated the semantic search function into `app/main.py`.
- Created a new GET endpoint: `/search/semantic`.
- Added query parameter `q` to accept user questions.
- Added `top_k` parameter to control the number of search results.
- Tested the API using FastAPI Swagger documentation.
- Verified successful API responses with HTTP 200 OK.
- Updated project dependencies and prepared the code for GitHub.

### Technologies Used
- Python
- FastAPI
- ChromaDB
- Sentence Transformers
- REST API
- Swagger UI

### API Endpoint

**GET** `/search/semantic?q=What is DPIIT Startup Recognition?&top_k=3`

### Outcome
Successfully integrated semantic search with FastAPI.
## Day 06 – Semantic Search with ChromaDB

### Objective
Implement semantic search to retrieve relevant StartupSetu records based on the meaning of a user's query.

### Tasks Completed
- Implemented document chunking using `app/chunking.py`.
- Split startup records into smaller chunks.
- Added metadata such as record ID, title, category, and chunk index.
- Used Sentence Transformers (`all-MiniLM-L6-v2`) to generate text embeddings.
- Stored document embeddings in a persistent ChromaDB vector database.
- Implemented semantic similarity search using cosine distance.
- Created `app/vectorstore.py` to manage indexing and searching.

### Technologies Used
- Python
- Sentence Transformers
- ChromaDB
- Vector Embeddings
- Semantic Search

### Outcome
Successfully implemented semantic search to retrieve relevant startup-related information based on the meaning of user queries.

---

## Day 07 – Semantic Search API Integration

### Objective
Integrate semantic search into the FastAPI application and make it accessible through an API endpoint.

### Tasks Completed
- Integrated the semantic search function into `app/main.py`.
- Created a new GET endpoint: `/search/semantic`.
- Added query parameter `q` to accept user questions.
- Added `top_k` parameter to control the number of search results.
- Tested the API using FastAPI Swagger documentation.
- Verified successful API responses with HTTP 200 OK.
- Updated project dependencies and prepared the code for GitHub.

### Technologies Used
- Python
- FastAPI
- ChromaDB
- Sentence Transformers
- REST API
- Swagger UI

### API Endpoint

**GET** `/search/semantic?q=What is DPIIT Startup Recognition?&top_k=3`

### Outcome
Successfully integrated semantic search with FastAPI.
## Day 06 – Semantic Search with ChromaDB

### Objective
Implement semantic search to retrieve relevant StartupSetu records based on the meaning of a user's query.

### Tasks Completed
- Implemented document chunking using `app/chunking.py`.
- Split startup records into smaller chunks.
- Added metadata such as record ID, title, category, and chunk index.
- Used Sentence Transformers (`all-MiniLM-L6-v2`) to generate text embeddings.
- Stored document embeddings in a persistent ChromaDB vector database.
- Implemented semantic similarity search using cosine distance.
- Created `app/vectorstore.py` to manage indexing and searching.

### Technologies Used
- Python
- Sentence Transformers
- ChromaDB
- Vector Embeddings
- Semantic Search

### Outcome
Successfully implemented semantic search to retrieve relevant startup-related information based on the meaning of user queries.

---

## Day 07 – Semantic Search API Integration

### Objective
Integrate semantic search into the FastAPI application and make it accessible through an API endpoint.

### Tasks Completed
- Integrated the semantic search function into `app/main.py`.
- Created a new GET endpoint: `/search/semantic`.
- Added query parameter `q` to accept user questions.
- Added `top_k` parameter to control the number of search results.
- Tested the API using FastAPI Swagger documentation.
- Verified successful API responses with HTTP 200 OK.
- Updated project dependencies and prepared the code for GitHub.

### Technologies Used
- Python
- FastAPI
- ChromaDB
- Sentence Transformers
- REST API
- Swagger UI

### API Endpoint

**GET** `/search/semantic?q=What is DPIIT Startup Recognition?&top_k=3`

### Outcome
Successfully integrated semantic search with FastAPI.
## Day 06 – Semantic Search with ChromaDB

### Objective
Implement semantic search to retrieve relevant StartupSetu records based on the meaning of a user's query.

### Tasks Completed
- Implemented document chunking using `app/chunking.py`.
- Split startup records into smaller chunks.
- Added metadata such as record ID, title, category, and chunk index.
- Used Sentence Transformers (`all-MiniLM-L6-v2`) to generate text embeddings.
- Stored document embeddings in a persistent ChromaDB vector database.
- Implemented semantic similarity search using cosine distance.
- Created `app/vectorstore.py` to manage indexing and searching.

### Technologies Used
- Python
- Sentence Transformers
- ChromaDB
- Vector Embeddings
- Semantic Search

### Outcome
Successfully implemented semantic search to retrieve relevant startup-related information based on the meaning of user queries.

---

## Day 07 – Semantic Search API Integration

### Objective
Integrate semantic search into the FastAPI application and make it accessible through an API endpoint.

### Tasks Completed
- Integrated the semantic search function into `app/main.py`.
- Created a new GET endpoint: `/search/semantic`.
- Added query parameter `q` to accept user questions.
- Added `top_k` parameter to control the number of search results.
- Tested the API using FastAPI Swagger documentation.
- Verified successful API responses with HTTP 200 OK.
- Updated project dependencies and prepared the code for GitHub.

### Technologies Used
- Python
- FastAPI
- ChromaDB
- Sentence Transformers
- REST API
- Swagger UI

### API Endpoint

**GET** `/search/semantic?q=What is DPIIT Startup Recognition?&top_k=3`

### Outcome
Successfully integrated semantic search with FastAPI.
## Day 06 – Semantic Search with ChromaDB

### Objective
Implement semantic search to retrieve relevant StartupSetu records based on the meaning of a user's query.

### Tasks Completed
- Implemented document chunking using `app/chunking.py`.
- Split startup records into smaller chunks.
- Added metadata such as record ID, title, category, and chunk index.
- Used Sentence Transformers (`all-MiniLM-L6-v2`) to generate text embeddings.
- Stored document embeddings in a persistent ChromaDB vector database.
- Implemented semantic similarity search using cosine distance.
- Created `app/vectorstore.py` to manage indexing and searching.

### Technologies Used
- Python
- Sentence Transformers
- ChromaDB
- Vector Embeddings
- Semantic Search

### Outcome
Successfully implemented semantic search to retrieve relevant startup-related information based on the meaning of user queries.

---

## Day 07 – Semantic Search API Integration

### Objective
Integrate semantic search into the FastAPI application and make it accessible through an API endpoint.

### Tasks Completed
- Integrated the semantic search function into `app/main.py`.
- Created a new GET endpoint: `/search/semantic`.
- Added query parameter `q` to accept user questions.
- Added `top_k` parameter to control the number of search results.
- Tested the API using FastAPI Swagger documentation.
- Verified successful API responses with HTTP 200 OK.
- Updated project dependencies and prepared the code for GitHub.

### Technologies Used
- Python
- FastAPI
- ChromaDB
- Sentence Transformers
- REST API
- Swagger UI

### API Endpoint

**GET** `/search/semantic?q=What is DPIIT Startup Recognition?&top_k=3`

### Outcome
Successfully integrated semantic search with FastAPI.
## Day 06 – Semantic Search with ChromaDB

### Objective
Implement semantic search to retrieve relevant StartupSetu records based on the meaning of a user's query.

### Tasks Completed
- Implemented document chunking using `app/chunking.py`.
- Split startup records into smaller chunks.
- Added metadata such as record ID, title, category, and chunk index.
- Used Sentence Transformers (`all-MiniLM-L6-v2`) to generate text embeddings.
- Stored document embeddings in a persistent ChromaDB vector database.
- Implemented semantic similarity search using cosine distance.
- Created `app/vectorstore.py` to manage indexing and searching.

### Technologies Used
- Python
- Sentence Transformers
- ChromaDB
- Vector Embeddings
- Semantic Search

### Outcome
Successfully implemented semantic search to retrieve relevant startup-related information based on the meaning of user queries.

---

## Day 07 – Semantic Search API Integration

### Objective
Integrate semantic search into the FastAPI application and make it accessible through an API endpoint.

### Tasks Completed
- Integrated the semantic search function into `app/main.py`.
- Created a new GET endpoint: `/search/semantic`.
- Added query parameter `q` to accept user questions.
- Added `top_k` parameter to control the number of search results.
- Tested the API using FastAPI Swagger documentation.
- Verified successful API responses with HTTP 200 OK.
- Updated project dependencies and prepared the code for GitHub.

### Technologies Used
- Python
- FastAPI
- ChromaDB
- Sentence Transformers
- REST API
- Swagger UI

### API Endpoint

**GET** `/search/semantic?q=What is DPIIT Startup Recognition?&top_k=3`

### Outcome
Successfully integrated semantic search with FastAPI.
## Day 06 – Semantic Search with ChromaDB

### Objective
Implement semantic search to retrieve relevant StartupSetu records based on the meaning of a user's query.

### Tasks Completed
- Implemented document chunking using `app/chunking.py`.
- Split startup records into smaller chunks.
- Added metadata such as record ID, title, category, and chunk index.
- Used Sentence Transformers (`all-MiniLM-L6-v2`) to generate text embeddings.
- Stored document embeddings in a persistent ChromaDB vector database.
- Implemented semantic similarity search using cosine distance.
- Created `app/vectorstore.py` to manage indexing and searching.

### Technologies Used
- Python
- Sentence Transformers
- ChromaDB
- Vector Embeddings
- Semantic Search

### Outcome
Successfully implemented semantic search to retrieve relevant startup-related information based on the meaning of user queries.

---

## Day 07 – Semantic Search API Integration

### Objective
Integrate semantic search into the FastAPI application and make it accessible through an API endpoint.

### Tasks Completed
- Integrated the semantic search function into `app/main.py`.
- Created a new GET endpoint: `/search/semantic`.
- Added query parameter `q` to accept user questions.
- Added `top_k` parameter to control the number of search results.
- Tested the API using FastAPI Swagger documentation.
- Verified successful API responses with HTTP 200 OK.
- Updated project dependencies and prepared the code for GitHub.

### Technologies Used
- Python
- FastAPI
- ChromaDB
- Sentence Transformers
- REST API
- Swagger UI

### API Endpoint

**GET** `/search/semantic?q=What is DPIIT Startup Recognition?&top_k=3`

### Outcome
Successfully integrated semantic search with FastAPI.
## Day 06 – Semantic Search with ChromaDB

### Objective
Implement semantic search to retrieve relevant StartupSetu records based on the meaning of a user's query.

### Tasks Completed
- Implemented document chunking using `app/chunking.py`.
- Split startup records into smaller chunks.
- Added metadata such as record ID, title, category, and chunk index.
- Used Sentence Transformers (`all-MiniLM-L6-v2`) to generate text embeddings.
- Stored document embeddings in a persistent ChromaDB vector database.
- Implemented semantic similarity search using cosine distance.
- Created `app/vectorstore.py` to manage indexing and searching.

### Technologies Used
- Python
- Sentence Transformers
- ChromaDB
- Vector Embeddings
- Semantic Search

### Outcome
Successfully implemented semantic search to retrieve relevant startup-related information based on the meaning of user queries.

---

## Day 07 – Semantic Search API Integration

### Objective
Integrate semantic search into the FastAPI application and make it accessible through an API endpoint.

### Tasks Completed
- Integrated the semantic search function into `app/main.py`.
- Created a new GET endpoint: `/search/semantic`.
- Added query parameter `q` to accept user questions.
- Added `top_k` parameter to control the number of search results.
- Tested the API using FastAPI Swagger documentation.
- Verified successful API responses with HTTP 200 OK.
- Updated project dependencies and prepared the code for GitHub.

### Technologies Used
- Python
- FastAPI
- ChromaDB
- Sentence Transformers
- REST API
- Swagger UI

### API Endpoint

**GET** `/search/semantic?q=What is DPIIT Startup Recognition?&top_k=3`

### Outcome
Successfully integrated semantic search with FastAPI.
## Day 06 – Semantic Search with ChromaDB

### Objective
Implement semantic search to retrieve relevant StartupSetu records based on the meaning of a user's query.

### Tasks Completed
- Implemented document chunking using `app/chunking.py`.
- Split startup records into smaller chunks.
- Added metadata such as record ID, title, category, and chunk index.
- Used Sentence Transformers (`all-MiniLM-L6-v2`) to generate text embeddings.
- Stored document embeddings in a persistent ChromaDB vector database.
- Implemented semantic similarity search using cosine distance.
- Created `app/vectorstore.py` to manage indexing and searching.

### Technologies Used
- Python
- Sentence Transformers
- ChromaDB
- Vector Embeddings
- Semantic Search

### Outcome
Successfully implemented semantic search to retrieve relevant startup-related information based on the meaning of user queries.

---

## Day 07 – Semantic Search API Integration

### Objective
Integrate semantic search into the FastAPI application and make it accessible through an API endpoint.

### Tasks Completed
- Integrated the semantic search function into `app/main.py`.
- Created a new GET endpoint: `/search/semantic`.
- Added query parameter `q` to accept user questions.
- Added `top_k` parameter to control the number of search results.
- Tested the API using FastAPI Swagger documentation.
- Verified successful API responses with HTTP 200 OK.
- Updated project dependencies and prepared the code for GitHub.

### Technologies Used
- Python
- FastAPI
- ChromaDB
- Sentence Transformers
- REST API
- Swagger UI

### API Endpoint

**GET** `/search/semantic?q=What is DPIIT Startup Recognition?&top_k=3`

### Outcome
Successfully integrated semantic search with FastAPI.
## Day 06 – Semantic Search with ChromaDB

### Objective
Implement semantic search to retrieve relevant StartupSetu records based on the meaning of a user's query.

### Tasks Completed
- Implemented document chunking using `app/chunking.py`.
- Split startup records into smaller chunks.
- Added metadata such as record ID, title, category, and chunk index.
- Used Sentence Transformers (`all-MiniLM-L6-v2`) to generate text embeddings.
- Stored document embeddings in a persistent ChromaDB vector database.
- Implemented semantic similarity search using cosine distance.
- Created `app/vectorstore.py` to manage indexing and searching.

### Technologies Used
- Python
- Sentence Transformers
- ChromaDB
- Vector Embeddings
- Semantic Search

### Outcome
Successfully implemented semantic search to retrieve relevant startup-related information based on the meaning of user queries.

---

## Day 07 – Semantic Search API Integration

### Objective
Integrate semantic search into the FastAPI application and make it accessible through an API endpoint.

### Tasks Completed
- Integrated the semantic search function into `app/main.py`.
- Created a new GET endpoint: `/search/semantic`.
- Added query parameter `q` to accept user questions.
- Added `top_k` parameter to control the number of search results.
- Tested the API using FastAPI Swagger documentation.
- Verified successful API responses with HTTP 200 OK.
- Updated project dependencies and prepared the code for GitHub.

### Technologies Used
- Python
- FastAPI
- ChromaDB
- Sentence Transformers
- REST API
- Swagger UI

### API Endpoint

**GET** `/search/semantic?q=What is DPIIT Startup Recognition?&top_k=3`

### Outcome
Successfully integrated semantic search with FastAPI.
## Day 06 – Semantic Search with ChromaDB

### Objective
Implement semantic search to retrieve relevant StartupSetu records based on the meaning of a user's query.

### Tasks Completed
- Implemented document chunking using `app/chunking.py`.
- Split startup records into smaller chunks.
- Added metadata such as record ID, title, category, and chunk index.
- Used Sentence Transformers (`all-MiniLM-L6-v2`) to generate text embeddings.
- Stored document embeddings in a persistent ChromaDB vector database.
- Implemented semantic similarity search using cosine distance.
- Created `app/vectorstore.py` to manage indexing and searching.

### Technologies Used
- Python
- Sentence Transformers
- ChromaDB
- Vector Embeddings
- Semantic Search

### Outcome
Successfully implemented semantic search to retrieve relevant startup-related information based on the meaning of user queries.

---

## Day 07 – Semantic Search API Integration

### Objective
Integrate semantic search into the FastAPI application and make it accessible through an API endpoint.

### Tasks Completed
- Integrated the semantic search function into `app/main.py`.
- Created a new GET endpoint: `/search/semantic`.
- Added query parameter `q` to accept user questions.
- Added `top_k` parameter to control the number of search results.
- Tested the API using FastAPI Swagger documentation.
- Verified successful API responses with HTTP 200 OK.
- Updated project dependencies and prepared the code for GitHub.

### Technologies Used
- Python
- FastAPI
- ChromaDB
- Sentence Transformers
- REST API
- Swagger UI

### API Endpoint

**GET** `/search/semantic?q=What is DPIIT Startup Recognition?&top_k=3`

### Outcome
Successfully integrated semantic search with FastAPI.
## Day 06 – Semantic Search with ChromaDB

### Objective
Implement semantic search to retrieve relevant StartupSetu records based on the meaning of a user's query.

### Tasks Completed
- Implemented document chunking using `app/chunking.py`.
- Split startup records into smaller chunks.
- Added metadata such as record ID, title, category, and chunk index.
- Used Sentence Transformers (`all-MiniLM-L6-v2`) to generate text embeddings.
- Stored document embeddings in a persistent ChromaDB vector database.
- Implemented semantic similarity search using cosine distance.
- Created `app/vectorstore.py` to manage indexing and searching.

### Technologies Used
- Python
- Sentence Transformers
- ChromaDB
- Vector Embeddings
- Semantic Search

### Outcome
Successfully implemented semantic search to retrieve relevant startup-related information based on the meaning of user queries.

---

## Day 07 – Semantic Search API Integration

### Objective
Integrate semantic search into the FastAPI application and make it accessible through an API endpoint.

### Tasks Completed
- Integrated the semantic search function into `app/main.py`.
- Created a new GET endpoint: `/search/semantic`.
- Added query parameter `q` to accept user questions.
- Added `top_k` parameter to control the number of search results.
- Tested the API using FastAPI Swagger documentation.
- Verified successful API responses with HTTP 200 OK.
- Updated project dependencies and prepared the code for GitHub.

### Technologies Used
- Python
- FastAPI
- ChromaDB
- Sentence Transformers
- REST API
- Swagger UI

### API Endpoint

**GET** `/search/semantic?q=What is DPIIT Startup Recognition?&top_k=3`

### Outcome
Successfully integrated semantic search with FastAPI.
## Day 06 – Semantic Search with ChromaDB

### Objective
Implement semantic search to retrieve relevant StartupSetu records based on the meaning of a user's query.

### Tasks Completed
- Implemented document chunking using `app/chunking.py`.
- Split startup records into smaller chunks.
- Added metadata such as record ID, title, category, and chunk index.
- Used Sentence Transformers (`all-MiniLM-L6-v2`) to generate text embeddings.
- Stored document embeddings in a persistent ChromaDB vector database.
- Implemented semantic similarity search using cosine distance.
- Created `app/vectorstore.py` to manage indexing and searching.

### Technologies Used
- Python
- Sentence Transformers
- ChromaDB
- Vector Embeddings
- Semantic Search

### Outcome
Successfully implemented semantic search to retrieve relevant startup-related information based on the meaning of user queries.

---

## Day 07 – Semantic Search API Integration

### Objective
Integrate semantic search into the FastAPI application and make it accessible through an API endpoint.

### Tasks Completed
- Integrated the semantic search function into `app/main.py`.
- Created a new GET endpoint: `/search/semantic`.
- Added query parameter `q` to accept user questions.
- Added `top_k` parameter to control the number of search results.
- Tested the API using FastAPI Swagger documentation.
- Verified successful API responses with HTTP 200 OK.
- Updated project dependencies and prepared the code for GitHub.

### Technologies Used
- Python
- FastAPI
- ChromaDB
- Sentence Transformers
- REST API
- Swagger UI

### API Endpoint

**GET** `/search/semantic?q=What is DPIIT Startup Recognition?&top_k=3`

### Outcome
Successfully integrated semantic search with FastAPI.