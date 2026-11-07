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