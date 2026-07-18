# Adaptive RAG

## Overview

Adaptive RAG is an AI-powered document question-answering platform that dynamically selects the best retrieval strategy based on the user's query.

Unlike traditional Retrieval-Augmented Generation (RAG) systems that follow a fixed pipeline, Adaptive RAG uses **LangGraph** to orchestrate multiple decision-making nodes. Depending on the query, the system can retrieve documents, rewrite the query, perform web search, and generate responses using the most appropriate workflow.

Users can upload PDF or TXT documents, ask natural language questions, and receive context-aware responses with source attribution while maintaining persistent conversation history across multiple sessions.

---

# Features

- Upload and index PDF and TXT documents
- Adaptive LangGraph workflow for intelligent routing
- Semantic search using vector embeddings
- Automatic query rewriting for improved retrieval
- Document relevance grading
- Web search fallback using Tavily when documents lack sufficient context
- Persistent multi-session chat history using MongoDB
- Source attribution for generated answers
- Interactive Streamlit interface
- REST API built with FastAPI

---

# Tech Stack

| Category | Technology |
|----------|------------|
| Backend | FastAPI |
| AI Orchestration | LangGraph |
| LLM | Groq (Llama 3.3 70B) |
| Embeddings | HuggingFace (BAAI/bge-small-en-v1.5) |
| Vector Database | Qdrant |
| Database | MongoDB Atlas |
| Web Search | Tavily |
| Frontend | Streamlit |

---

# Workflow

## 1. Document Upload

Users upload PDF or TXT documents through the Streamlit interface.

The ingestion pipeline:

- Loads the document
- Splits the document into semantic chunks
- Generates embeddings
- Stores vectors in Qdrant
- Associates every chunk with a session ID

---

## 2. User Query

A user submits a question.

The query is first classified into one of two categories:

- General knowledge question
- Document-specific question

General questions are answered directly using the LLM.

---

## 3. Semantic Retrieval

For document-related questions:

- Relevant chunks are retrieved from Qdrant
- Retrieval is filtered using the user's session ID
- Only the user's uploaded documents are searched

---

## 4. Document Relevance Grading

The retrieved context is evaluated by the LLM.

**If relevant:**

- Generate the final answer.

**Otherwise:**

- Rewrite the query.

---

## 5. Query Rewriting

The system reformulates ambiguous or poorly phrased questions to improve retrieval quality.

Example:

```text
Original:
Explain this.

↓

Rewritten:
Explain the authentication mechanism described in the uploaded document.
```

---

## 6. Web Search

If relevant information is still unavailable:

- Invoke Tavily Search
- Retrieve external information
- Combine web results with document context

---

## 7. Response Generation

The final answer is generated using:

- Retrieved document context
- Web search results (when required)
- Conversation history stored in MongoDB

Responses also include source attribution whenever document chunks are used.

---

# LangGraph Workflow

The application is implemented as a graph instead of a sequential pipeline.

The workflow consists of the following nodes:

- Query Classification
- Semantic Retrieval
- Document Relevance Grading
- Query Rewriting
- Web Search
- Answer Generation

This adaptive architecture dynamically selects the best execution path based on the user's query.

---

# Installation

## Clone the Repository

```bash
git clone <repository-url>
cd adaptive-rag
```

## Create a Virtual Environment

```bash
python -m venv venv
```

### macOS / Linux

```bash
source venv/bin/activate
```

### Windows

```bash
venv\Scripts\activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file in the project root.

```env
GROQ_API_KEY=your_key

QDRANT_URL=your_url
QDRANT_API_KEY=your_key

MONGODB_URI=your_uri

TAVILY_API_KEY=your_key

EMBEDDING_MODEL=BAAI/bge-small-en-v1.5
```

---

# Running the Backend

```bash
uvicorn src.main:app --reload
```

API Documentation:

```text
http://localhost:8000/docs
```

---

# Running the Frontend

```bash
streamlit run streamlit_app/home.py
```

---

# Future Improvements

- Multi-document reasoning
- Hybrid keyword + semantic retrieval
- Support for DOCX and Markdown documents
- Streaming token generation
- User authentication and access control
- Citation highlighting within documents
- Evaluation pipeline for retrieval quality

---

# Key Learnings

This project provided hands-on experience with:

- Building adaptive AI workflows using LangGraph
- Retrieval-Augmented Generation (RAG)
- Semantic search using vector databases
- Prompt engineering and query optimization
- LLM orchestration and decision-making
- Session-aware conversational AI
- FastAPI backend development
- Streamlit frontend development
- Vector search with Qdrant
- Persistent conversation history using MongoDB

---

# Why Adaptive RAG?

### Traditional RAG

```text
Retrieve
    │
    ▼
Generate
```

### Adaptive RAG

```text
Classify Query
      │
      ▼
Retrieve Documents
      │
      ▼
Grade Relevance
      │
      ▼
Rewrite Query (if needed)
      │
      ▼
Web Search (if needed)
      │
      ▼
Generate Response
```

Instead of following a fixed retrieval pipeline, Adaptive RAG dynamically selects the most appropriate strategy based on the user's query. This results in more accurate, context-aware, and reliable responses.
