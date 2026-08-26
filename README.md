# 🦷 AI Dental Analyzer

**AI Dental Analyzer** is an AI-powered dental assistance system that analyzes dental images along with patient symptoms and tooth-specific information to provide a **preliminary educational assessment**.

> ⚠️ **Medical Disclaimer:** This application is for educational and preliminary assessment purposes only. It is not a replacement for professional dental diagnosis or treatment.

## 🚀 Overview

The system combines **multimodal AI, RAG, vector search, web search, and an AI-driven backend** to provide contextual dental information.

### 🔑 Key Features

* 🖼️ Upload/capture dental images
* 📋 Collect patient symptoms and medical information
* 🦷 Select affected teeth using the **FDI tooth numbering system**
* 🤖 Analyze images using **Google Gemini multimodal AI**
* 🔎 Retrieve relevant dental knowledge using **RAG**
* 🧠 Generate embeddings using **Sentence Transformers**
* 🗄️ Store and search vectors using **PostgreSQL + pgvector**
* 🌐 Use **Tavily Search API** for web-based information when RAG results are insufficient
* ⚡ FastAPI backend for APIs and application logic
* ⚛️ React frontend for the user interface
* 🔗 LangChain for LLM, prompt, retrieval, and tool integration
* 🔄 LangGraph for managing multi-step AI workflows and decision-based execution
* 💾 Supabase/PostgreSQL for application data
* 📊 Analytics dashboard
* 🔐 Google OAuth authentication

## 🧠 AI & RAG Architecture

The application follows a retrieval-first architecture:

```text
User
 │
 ▼
React Frontend
 │
 ▼
FastAPI Backend
 │
 ├── Patient & Image Data
 │
 ├── LangChain
 │     ├── Prompt Management
 │     ├── Retriever
 │     └── LLM Integration
 │
 ▼
LangGraph Workflow
 │
 ├── Build Retrieval Query
 │
 ├── Generate Embedding
 │
 ▼
Sentence Transformer
 │
 ▼
PostgreSQL + pgvector
 │
 ├── Relevant Knowledge Found
 │         │
 │         ▼
 │      RAG Context
 │
 └── Insufficient Results
           │
           ▼
      Tavily Search API
           │
           ▼
      Web Supporting Context
           │
           ▼
     Gemini Multimodal AI
           │
           ▼
   Preliminary Assessment
```

### 🔎 RAG

The dental knowledge base is converted into vector embeddings using a **Sentence Transformer embedding model** and stored in **PostgreSQL with pgvector**.

When a user submits symptoms and dental information:

1. A retrieval query is created.
2. The query is converted into an embedding.
3. PostgreSQL/pgvector performs similarity search.
4. Relevant dental knowledge is retrieved.
5. Retrieved context is passed to the LLM.

### 🌐 Tavily Web Search

When the retrieved knowledge does not meet the configured similarity threshold, the system uses the **Tavily Search API** to find additional supporting information from the web.

Tavily results are treated as supporting context and not as a definitive diagnosis.

## 🔗 LangChain & LangGraph

**LangChain** is used where LLM orchestration is required, including prompt construction, retrieval integration, model interaction, and connecting AI tools/components.

**LangGraph** is used to structure the application's multi-step AI workflow. It allows the system to move through steps such as retrieval, checking retrieval quality, triggering Tavily when necessary, and finally generating the assessment.

## 🛠️ Technology Stack

| Technology                | Purpose                                        |
| ------------------------- | ---------------------------------------------- |
| **React**                 | Frontend UI                                    |
| **FastAPI**               | Backend API and application logic              |
| **Python**                | Core backend language                          |
| **Google Gemini**         | Multimodal dental image + text analysis        |
| **LangChain**             | LLM and retrieval orchestration                |
| **LangGraph**             | Multi-step AI workflow orchestration           |
| **Sentence Transformers** | Text embedding generation                      |
| **PostgreSQL + pgvector** | Vector database and similarity search          |
| **Tavily Search API**     | Web search / fallback retrieval                |
| **Supabase**              | Database infrastructure/authentication support |
| **Pandas**                | Analytics and data processing                  |
| **Google OAuth**          | Authentication                                 |
| **Git/GitHub**            | Version control                                |

## 📁 Project Structure

```text
AI-Dental/
│
├── frontend/                # React frontend
│
├── backend/                # FastAPI backend
│
├── knowledge/               # Dental knowledge base
│
├── rag/                     # RAG and vector retrieval
│
├── agents/                  # LangChain/LangGraph workflows
│
├── database/                # PostgreSQL/Supabase operations
│
├── tests/                   # Test files
│
├── requirements.txt
├── .env
└── README.md
```

## ⚙️ Environment Variables

```env
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=your_gemini_model

TAVILY_API_KEY=your_tavily_api_key

DATABASE_URL=your_postgresql_database_url

SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key

RAG_THRESHOLD=0.60
```

Never commit `.env` or other credentials to GitHub.

## ▶️ Running the Project

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## 🔄 User Workflow

```text
Login
  ↓
Upload/Capture Dental Image
  ↓
Enter Symptoms
  ↓
Select Affected Tooth
  ↓
FastAPI Backend
  ↓
LangGraph Workflow
  ↓
RAG Search using Sentence Transformers + PostgreSQL/pgvector
  ↓
Enough Context?
 ┌───────────────┴───────────────┐
 │                               │
Yes                             No
 │                               │
 ▼                               ▼
RAG Context                Tavily Search API
 │                               │
 └───────────────┬───────────────┘
                 ▼
          Gemini Multimodal AI
                 ↓
       Preliminary Assessment
                 ↓
        Store Assessment
```

## ⚠️ Medical Safety

The system provides **preliminary AI-assisted information only**.

Dental photographs cannot reliably determine every underlying condition, and AI-generated information can be incorrect. Professional dental examination and appropriate clinical tests may be required for diagnosis and treatment.

## 👩‍💻 Project

**AI Dental Analyzer — Venus John**

An AI-assisted dental image analysis platform combining **React, FastAPI, Gemini, LangChain, LangGraph, RAG, Sentence Transformers, PostgreSQL/pgvector, Tavily Search API, and Supabase**.
