# AI Knowledge Platform

An AI-powered document question-answering platform built with **FastAPI, React, Retrieval-Augmented Generation (RAG), Qdrant, LangGraph, and Google Gemini**. Upload documents, ask questions about their content, and retrieve relevant passages with source citations.

## Features

- **Document Upload:** Upload TXT, PDF, and DOCX documents.
- **Document Processing:** Extract text, split content into chunks, and prepare it for retrieval.
- **Semantic Search:** Find relevant document passages using embeddings and Qdrant.
- **Retrieval-Augmented Generation:** Generate answers using retrieved document context.
- **Source Citations:** Return source information alongside retrieval results.
- **AI Agent:** Integrate agent workflows with LangGraph and Google Gemini.
- **Chat API:** Provide chat and streaming-chat endpoints.
- **Voice Features:** API endpoints for speech transcription and text-to-speech.
- **Database Integration:** PostgreSQL and SQLAlchemy.
- **Automated Tests:** Backend tests using pytest.
- **Web Interface:** Frontend built with React and Vite.

> Note: Available features depend on the current configuration of the backend, external services, and AI provider.

## Technology Stack

| Area | Technologies |
|---|---|
| Backend | Python 3.11, FastAPI, Pydantic Settings |
| Database | PostgreSQL, SQLAlchemy, Alembic |
| AI / LLM | Google Gemini, LangChain, LangGraph |
| RAG | Embeddings, document chunking, semantic retrieval |
| Vector Database | Qdrant |
| Background Processing | Redis, Celery |
| Frontend | React, JavaScript, Vite |
| API Communication | REST, Server-Sent Events (SSE) |
| Testing | pytest |
| Version Control | Git, GitHub |

## Architecture

```text
User
 |
 v
React Frontend
 |
 v
FastAPI Backend
 |
 +---- Document Upload and Processing
 |              |
 |              v
 |        Text Extraction
 |              |
 |              v
 |        Chunking and Embeddings
 |              |
 |              v
 |            Qdrant
 |
 +---- User Question
                |
                v
         Semantic Retrieval
                |
                v
         Relevant Context
                |
                v
        LangGraph / Gemini
                |
                v
       Answer and Citations
```

PostgreSQL stores application data. Redis and Celery are intended for background processing where configured.

## Project Structure

```text
ai-knowledge-platform/
├── backend/
│   ├── app/
│   │   ├── agents/
│   │   ├── api/
│   │   │   └── v1/
│   │   ├── core/
│   │   ├── infra/
│   │   ├── models/
│   │   ├── services/
│   │   └── main.py
│   ├── evaluation/
│   └── tests
├── frontend/
│   └── src/
├── requirements.txt
├── requirements-dev.txt
├── .env.example
├── .gitignore
└── README.md
```

The exact files and folders may vary as development continues.

## Prerequisites

Install the following before running the project:

- Python 3.11
- Node.js and npm
- Git
- PostgreSQL, if enabled in your configuration
- A Qdrant instance or local Qdrant storage
- Google Gemini API key

Redis is required if the configured application workflows use Redis or Celery.

## Local Setup

### 1. Clone the repository

```powershell
git clone https://github.com/MashhoodUlHassan/ai-knowledge-platform.git
cd ai-knowledge-platform
```

### 2. Create and activate a Python environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install backend dependencies

```powershell
python -m pip install -r requirements.txt
```

Install development dependencies separately if needed:

```powershell
python -m pip install -r requirements-dev.txt
```

### 4. Configure environment variables

Create a local `.env` file using `.env.example` as a reference.

Configure the values required by your application, such as:

- Google Gemini API key
- Database connection string
- Qdrant connection settings
- Redis settings, if required
- Frontend allowed origins and application configuration

Never commit `.env` files, credentials, or API keys to GitHub.

### 5. Start the backend

From the repository root, open a PowerShell terminal:

```powershell
$env:PYTHONPATH = "backend"
python -m uvicorn app.main:app --reload
```

The local API should be available at:

- API: `http://127.0.0.1:8000`
- Swagger documentation: `http://127.0.0.1:8000/docs`
- Health check: `http://127.0.0.1:8000/api/v1/health`

Keep the backend terminal running.

### 6. Start the frontend

Open another PowerShell terminal:

```powershell
cd frontend
npm install
npm run dev
```

Open the local frontend URL printed by Vite, commonly `http://localhost:5173`.

Ensure the frontend API configuration points to the running backend.

## API Overview

The following endpoints are available in the current application. Refer to Swagger for their exact request schemas and response formats.

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Root endpoint |
| GET | `/api/v1/health` | Health check |
| POST | `/api/v1/documents/upload` | Upload a document |
| POST | `/api/v1/retrieval/search` | Search relevant document passages |
| POST | `/api/v1/agent/ask` | Submit a question to the AI agent |
| POST | `/chat` | Chat API |
| POST | `/chat/stream` | Streaming chat API |
| POST | `/api/v1/voice/transcribe` | Speech transcription |
| POST | `/api/v1/voice/synthesize` | Text-to-speech |

Some endpoints require configured external services or API credentials.

## RAG Workflow

1. Upload a supported document.
2. Extract text from the file.
3. Split the text into chunks.
4. Generate embeddings.
5. Store vectors for semantic retrieval.
6. Search for relevant passages when a question is asked.
7. Pass retrieved context to the configured AI workflow.
8. Return the answer and available source citations.

## Testing

Run backend tests from the repository root:

```powershell
python -m pytest backend -q
```

The test environment must have the required dependencies and services configured. If local Qdrant storage is in use, avoid opening the same storage directory from multiple processes simultaneously.

Build the frontend for production:

```powershell
cd frontend
npm run build
```

## Deployment

The project is intended to be deployed without Docker.

Deployment requires a frontend host, a backend host, environment variables, and appropriately configured database and vector storage services.

Before deployment:

- Configure the production frontend API URL.
- Set the backend's allowed frontend origins.
- Add secrets through the hosting provider's environment settings.
- Configure persistent or managed PostgreSQL and Qdrant storage.
- Verify all required AI provider credentials and service connections.
- Test document upload, retrieval, chat, and citations using the live URLs.

**Deployment status:** Hosting configuration and live production verification are pending.

## Security Notes

- Do not expose API keys in frontend code.
- Do not commit `.env` files or private credentials.
- Use production-specific environment variables.
- Restrict allowed origins to the deployed frontend.
- Protect uploaded documents and database credentials.

## Future Improvements

- Authentication and user-specific document access
- Improved retrieval quality and reranking
- More robust streaming responses
- Better evaluation and observability
- Production monitoring and error handling
- Further voice feature testing
- Deployment automation

## Author

**Muhammad Mashhood Ul Hassan**

BS Computer Science  
Interests: AI / ML, Generative AI, Agentic AI, RAG, and backend development.

GitHub: [MashhoodUlHassan](https://github.com/MashhoodUlHassan)

## License

For educational, portfolio, and demonstration purposes. Add a formal license file if you intend to distribute the project under a specific open-source license.
