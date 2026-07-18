Adaptive RAG is an AI-powered document question-answering platform that dynamically selects the best retrieval strategy based on the user's query. Instead of relying on a fixed Retrieval-Augmented Generation (RAG) pipeline, the system uses LangGraph to orchestrate multiple decision-making nodes, enabling document retrieval, query rewriting, web search fallback, and answer generation.
Users can upload PDF or TXT documents, ask natural language questions, and receive context-aware responses with source attribution while maintaining persistent conversation history across sessions.

Features
1.Upload and index PDF and TXT documents
2.Adaptive LangGraph workflow for intelligent routing
3.Semantic search using vector embeddings
4.Automatic query rewriting for improved retrieval
5.Document relevance grading
6.Web search fallback using Tavily when documents lack sufficient context
7.Persistent multi-session chat history using MongoDB
8.Source attribution for generated answers
9.Interactive Streamlit interface
10.REST API built with FastAPI
11.Tech Stack
12.Category	Technologies
13.Backend	FastAPI
14.AI Orchestration	LangGraph
15.LLM	Groq (Llama 3.3 70B)
16.Embeddings	HuggingFace (BAAI/bge-small-en-v1.5)
17.Vector Database	Qdrant
18.Database	MongoDB Atlas
19.Web Search	Tavily
20.Frontend	Streamlit



Workflow
1. Document Upload

Users upload PDF or TXT documents through the Streamlit interface.

The ingestion pipeline:

Loads the document
Splits it into semantic chunks
Generates embeddings
Stores vectors in Qdrant
Associates every chunk with a session ID
2. User Query

A user asks a question.

The query is first classified into one of two categories:

General knowledge question
Document-specific question

General questions are answered directly using the LLM.

3. Semantic Retrieval

For document-related questions:

Relevant chunks are retrieved from Qdrant
Retrieval is filtered using the user's session ID
Only the user's uploaded documents are searched
4. Document Grading

The retrieved context is evaluated by the LLM.

If sufficient information exists:

Generate the final answer.

Otherwise:

Rewrite the query.
5. Query Rewriting

The system reformulates ambiguous or poorly phrased questions to improve retrieval quality.

Example:

Original:
Explain this.

↓

Rewritten:
Explain the authentication mechanism described in the uploaded document.
6. Web Search

If relevant information is still unavailable,

the workflow automatically invokes Tavily to retrieve external information.

The web results are combined with the document context before answer generation.

7. Response Generation

The LLM generates a final answer using:

Retrieved document context
Web search results (if required)
Conversation history

The response also includes source attribution whenever document chunks are used.

LangGraph Workflow

The application is implemented as a graph rather than a sequential pipeline.

Nodes include:

Query Classification
Semantic Retrieval
Document Relevance Grading
Query Rewriting
Web Search
Answer Generation

This adaptive architecture allows the workflow to dynamically choose the best execution path based on the query.


Installation

Clone the repository

git clone <repository-url>
cd adaptive-rag

Create a virtual environment

python -m venv venv

Activate it

macOS/Linux

source venv/bin/activate

Windows

venv\Scripts\activate

Install dependencies

pip install -r requirements.txt
Environment Variables

Create a .env file.

GROQ_API_KEY=your_key

QDRANT_URL=your_url
QDRANT_API_KEY=your_key

MONGODB_URI=your_uri

TAVILY_API_KEY=your_key

EMBEDDING_MODEL=BAAI/bge-small-en-v1.5
Running the Backend
uvicorn src.main:app --reload

API documentation

http://localhost:8000/docs
Running the Frontend
streamlit run streamlit_app/home.py
Future Improvements
Multi-document reasoning
Hybrid keyword + semantic retrieval
Support for DOCX and Markdown documents
Streaming token generation
User authentication and access control
Citation highlighting within documents
Evaluation pipeline for retrieval quality
Key Learnings

Through this project, I gained hands-on experience with:

Building adaptive AI workflows using LangGraph
Retrieval-Augmented Generation (RAG) architectures
Semantic search with vector databases
Prompt engineering and query optimization
LLM orchestration and decision-making
Session-aware conversational AI
FastAPI backend development
Streamlit frontend development
Vector search using Qdrant
Persistent chat history using MongoDB
Why Adaptive RAG?

Traditional RAG systems always follow the same sequence:

Retrieve
    ↓
Generate

Adaptive RAG introduces intelligent decision-making:

Classify Query
      ↓
Retrieve Documents
      ↓
Grade Relevance
      ↓
Rewrite Query (if needed)
      ↓
Web Search (if needed)
      ↓
Generate Response

This enables the system to produce more reliable and context-aware responses by selecting the most appropriate retrieval strategy instead of relying on a fixed pipeline.
