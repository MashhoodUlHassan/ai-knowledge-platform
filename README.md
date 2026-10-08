# AI Knowledge Platform

An AI-powered knowledge platform that combines **Retrieval-Augmented Generation (RAG)**, **vector search**, **LangGraph agents**, and **Google Gemini** to answer questions from uploaded documents with source-aware responses.

## 🚀 Features

- 📄 Document upload and processing
- ✂️ Automatic text parsing and chunking
- 🧠 Embedding generation
- 🔎 Semantic vector search with Qdrant
- 🤖 Retrieval-Augmented Generation (RAG)
- 🕸️ LangGraph-based AI agent workflow
- 💬 Chat API with Server-Sent Events (SSE)
- 🗄️ PostgreSQL database
- ⚡ Redis-based background processing
- 🔐 Environment-based configuration
- 🛡️ Basic query guardrails
- 🧪 Automated backend tests
- 📊 RAGAS evaluation pipeline
- 🐳 Docker deployment support
- 🌐 Frontend interface

## 🏗️ Architecture

```text
                    ┌─────────────────────┐
                    │      Frontend       │
                    │      Web App        │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │      FastAPI        │
                    │       Backend       │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
        ┌───────────┐    ┌───────────┐    ┌───────────┐
        │ PostgreSQL│    │   Qdrant  │    │   Redis   │
        │  Database │    │Vector DB  │    │   Queue   │
        └───────────┘    └───────────┘    └─────┬─────┘
                                                │
                                                ▼
                                         ┌─────────────┐
                                         │   Workers   │
                                         └─────────────┘

                         User Question
                               │
                               ▼
                         Query Validation
                               │
                               ▼
                         Vector Retrieval
                               │
                               ▼
                           Qdrant
                               │
                               ▼
                       Relevant Context
                               │
                               ▼
                         LangGraph Agent
                               │
                               ▼
                         Google Gemini
                               │
                               ▼
                      Grounded AI Answer
                               │
                               ▼
                          Citations
```

## 🛠️ Technology Stack

### Backend

- Python 3.11
- FastAPI
- Pydantic Settings
- SQLAlchemy
- Alembic
- PostgreSQL

### AI / ML

- Google Gemini
- LangChain
- LangGraph
- Retrieval-Augmented Generation (RAG)
- Text Embeddings
- Semantic Search

### Vector Database

- Qdrant

### Background Processing

- Redis
- Celery

### Frontend

- JavaScript
- Vite
- Web-based chat interface
- Server-Sent Events (SSE)

### Testing & Evaluation

- Pytest
- RAGAS

### DevOps

- Docker
- Git
- GitHub

## 📁 Project Structure

```text
ai-knowledge-platform/
│
├── backend/
│   ├── app/
│   │   ├── agents/
│   │   ├── api/
│   │   │   └── v1/
│   │   ├── core/
│   │   ├── infra/
│   │   ├── models/
│   │   ├── services/
│   │   ├── workers/
│   │   └── main.py
│   │
│   ├── evaluation/
│   │   ├── dataset.py
│   │   └── run_evaluation.py
│   │
│   └── test_*.py
│
├── frontend/
│
├── docs/
│   └── eval-report.md
│
├── Dockerfile
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## ⚙️ Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/MashhoodUlHassan/ai-knowledge-platform.git
cd ai-knowledge-platform
```

### 2. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file based on:

```text
.env.example
```

Add the required database, Redis, Qdrant, and Gemini configuration.

> Never commit your `.env` file or API keys to GitHub.

## ▶️ Run the Backend

From the project root:

```powershell
$env:PYTHONPATH="backend"
python -m uvicorn app.main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

## 🌐 Run the Frontend

```powershell
cd frontend
npm install
npm run dev
```

Frontend:

```text
http://localhost:5173
```

## 🧪 Run Tests

From the project root:

```powershell
$env:PYTHONPATH="backend"
python -m pytest -q
```

Current automated test suite covers:

- API health endpoint
- Chat API
- Chat validation
- Retrieval validation
- Guardrails
- Document processing

## 📊 Evaluation

The project includes a RAGAS-based evaluation pipeline.

Evaluation metrics include:

- **Faithfulness**
- **Answer Relevancy**
- **Context Precision**
- **Context Recall**

Evaluation dataset and execution code are located in:

```text
backend/evaluation/
```

Detailed evaluation documentation:

```text
docs/eval-report.md
```

Run evaluation with:

```powershell
$env:PYTHONPATH="backend"
python backend\evaluation\run_evaluation.py
```

> Final numerical RAGAS scores may vary depending on LLM/API availability and model response behavior.

## 🐳 Docker

Build the backend image:

```bash
docker build -t ai-knowledge-platform .
```

Run the container:

```bash
docker run -p 8000:8000 ai-knowledge-platform
```

## 🔌 API Overview

### Health / Root

```http
GET /
```

### Chat

```http
POST /chat
```

Example:

```json
{
  "message": "What is machine learning?"
}
```

### Streaming Chat

```http
POST /chat/stream
```

### Document APIs

```text
/api/v1/documents
```

### Retrieval

```http
POST /api/v1/retrieval/search
```

Example:

```json
{
  "query": "What is artificial intelligence?",
  "top_k": 5
}
```

## 🔄 RAG Pipeline

The platform follows this workflow:

```text
Document Upload
      ↓
Document Parsing
      ↓
Text Chunking
      ↓
Embedding Generation
      ↓
Qdrant Vector Storage
      ↓
User Question
      ↓
Query Embedding
      ↓
Semantic Retrieval
      ↓
Relevant Context
      ↓
LangGraph Agent
      ↓
Google Gemini
      ↓
Grounded Answer
      ↓
Source References
```

## 🛡️ Guardrails

The platform validates incoming queries before processing.

Current guardrails include:

- Empty-query rejection
- Context-grounded answering
- Explicit fallback when information is unavailable
- Source-aware responses

## 📈 Future Improvements

Planned improvements include:

- True token-level streaming
- Authentication and authorization
- Advanced document formats
- Improved citation handling
- Hybrid search
- Reranking
- Conversation memory
- Advanced evaluation datasets
- Better observability and tracing
- Production CI/CD
- Cloud deployment
- Performance optimization
- Improved agent tool selection

## 🎯 Project Goals

This project was designed to demonstrate practical experience with:

- Production-style FastAPI architecture
- RAG system development
- Vector databases
- LLM integration
- Agentic AI
- LangGraph
- Background processing
- Automated testing
- AI evaluation
- Docker
- API design
- Full-stack AI application development

## 👨‍💻 Author

**Muhammad Mashhood Ul Hassan**

BS Computer Science  
AI / ML | Generative AI | Agentic AI | RAG

GitHub: `MashhoodUlHassan`

## 📄 License

This project is intended for educational, portfolio, and demonstration purposes.