# AI Productivity Platform

<p align="center">
  <img src="/FastAPI_production.PNG" alt="AI Productivity Platform Banner" width="100%">
</p>

<p align="center">

![Python](https://img.shields.io/badge/Python-3.13-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-blue.svg)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.x-red.svg)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED.svg)
![Celery](https://img.shields.io/badge/Celery-Asynchronous-37814A.svg)
![RabbitMQ](https://img.shields.io/badge/RabbitMQ-Message%20Broker-FF6600.svg)
![AWS S3](https://img.shields.io/badge/AWS-S3-orange.svg)
![ChromaDB](https://img.shields.io/badge/Vector-Database-7B68EE.svg)
![SentenceTransformers](https://img.shields.io/badge/Embeddings-all--MiniLM--L6--v2-success.svg)
![Groq](https://img.shields.io/badge/LLM-Groq-black.svg)
![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)

</p>

---

# Overview

AI Productivity Platform is a production-oriented backend platform that transforms transcripts into searchable knowledge using Retrieval-Augmented Generation (RAG) and supports persistent session-based AI conversations. Users can create conversation sessions for individual transcripts, interact with an AI assistant, and persist chat history for future conversational memory enhancements.

Current Version:

**Version 2.4**

---

# Key Features

## Authentication

- JWT Authentication
- User Registration & Login
- Protected APIs

## Todo Management

- Create Todo
- Update Todo
- Delete Todo
- Transcript association

## Transcript Management

- Upload transcript files
- AWS S3 storage
- Metadata persistence
- Background processing

Supported formats

- TXT
- PDF
- DOCX

## Asynchronous ETL Pipeline

- Celery Workers
- RabbitMQ Queue
- Text Extraction
- Text Cleaning
- Recursive Chunking
- Embedding Generation
- Metadata Preparation
- ChromaDB Storage

## Semantic Search

- Dense Vector Retrieval
- Metadata Filtering
- Cross Encoder Reranking
- Context Builder
- Prompt Builder
- Groq LLM Integration

## Session-based Conversations

- Create conversation sessions
- Multiple sessions per transcript
- Persistent chat history
- AI chat endpoint
- Delete sessions and chat history

---

# System Architecture

```
                                      Client
                                         │
                                         ▼
                                 FastAPI REST API
                                         │
             ┌───────────────────────────┼───────────────────────────┐
             │                           │                           │
             ▼                           ▼                           ▼
     Upload & ETL Pipeline        Semantic Search            Session-based Chat
             │                           │                           │
             ▼                           ▼                           ▼
          AWS S3                 Retrieval Service             Chat Service
             │                           │                  ┌────────┴────────┐
             ▼                           │                  ▼                 ▼
      RabbitMQ Queue                     │          Session Service   ChatMessage Service
             │                           │                  │                 │
             ▼                           ▼                  │                 │
       Celery Worker             Query Embedding            │        Load / Save Messages
             │                           │                  │                 │
             ▼                           ▼                  │                 │
      Text Extraction            ChromaDB Search            │                 │
             │                           │                  │                 │
             ▼                           ▼                  └────────┬────────┘
       Text Cleaning         Cross Encoder Reranking                 │
             │                           │                           │
             ▼                           ▼                           │
   Recursive Chunking           Context Builder                      │
             │                           │                           │
             ▼                           ▼                           │
    Embedding Service            Prompt Builder ◄────────────────────┘
             │                           │
             ▼                           ▼
      ChromaDB Storage                 Groq LLM
                                         │
                                         ▼
                                AI Generated Answer
```

---

# ETL Workflow

The transcript processing pipeline executes asynchronously after every successful upload.

```
Client

    │

Upload Transcript

    │

AWS S3 Storage

    │

Save Transcript Metadata

    │

Status = UPLOADED

    │

RabbitMQ

    │

Celery Worker

    │

Status = PROCESSING

    │

Download Transcript

    │

Extract Text

    │

Clean Text

    │

Recursive Chunking

    │

Generate Embeddings

    │

Prepare Metadata

    │

Store in ChromaDB

    │

Status = READY
```

---

# Semantic Search Workflow

The semantic search pipeline retrieves the most relevant transcript chunks before generating an answer.

```
User Question

      │

Generate Query Embedding

      │

Similarity Search

      │

Retrieve Top 20 Chunks

      │

Cross Encoder Reranking

      │

Select Top 5 Chunks

      │

Context Builder

      │

Prompt Builder

      │

Groq LLM

      │

Generated Answer
```

---

# RAG Pipeline

The Retrieval-Augmented Generation workflow combines semantic retrieval with LLM reasoning.

```
Question

     │

EmbeddingService

     │

VectorStoreService

     │

CrossEncoderService

     │

ContextBuilder

     │

PromptBuilder

     │

LLMService

     │

Groq

     │

Answer
```

---

# Project Structure

```
app
├── api
├── auth
├── core
├── db
├── models
├── repositories
├── schemas
├── services
│   ├── builder
│   │   ├── context_builder.py
│   │   └── prompt_builder.py
│   │
│   ├── embeddings
│   │   └── embedding_service.py
│   │
│   ├── extraction
│   │   └── text_extractor.py
│   │
│   ├── cleaning
│   │   └── text_cleaner.py
│   │
│   ├── chunking
│   │   └── text_chunker.py
│   │
│   ├── llm
│   │   └── llm_service.py
│   │
│   ├── reranking
│   │   └── cross_encoder_service.py
│   │
│   ├── retrieval
│   │   └── retrieval_service.py
│   │
│   ├── session
│   │   ├── session_service.py
│   │   └── chatmessage_service.py
│   │
│   ├── vector_store
│   │   └── vectorstore_service.py
│   │
│   ├── transcript_service.py
│   ├── todo_service.py
│   └── user_service.py
│
├── workers
├── utils
└── main.py
```

---

# Core Components

## TextExtractor

Responsible only for extracting text from uploaded documents.

Current support

- TXT
- PDF
- DOCX

Designed for easy extension to OCR, images, and additional document formats.

---

## TextCleaner

Normalizes extracted text before chunking.

Current operations

- Lowercase conversion
- HTML removal
- URL removal
- Emoji removal
- Special character cleanup
- Whitespace normalization

---

## TextChunker

Splits cleaned documents into overlapping chunks using

```
RecursiveCharacterTextSplitter
```

This strategy preserves contextual information while remaining flexible for future chunking approaches.

---

## EmbeddingService

Generates dense vector embeddings.

Current model

```
sentence-transformers/all-MiniLM-L6-v2
```

The embedding provider is configurable through environment variables.

---

## VectorStoreService

Responsible for

- Metadata preparation
- Vector storage
- Semantic retrieval

Current vector database

```
ChromaDB PersistentClient
```

---

## CrossEncoderService

Improves retrieval quality by reranking vector search results.

Current model

```
cross-encoder/ms-marco-MiniLM-L-6-v2
```

---

## ContextBuilder

Builds structured transcript context for the LLM.

Responsibilities

- Sort retrieved chunks
- Prepare formatted context
- Ready for neighboring chunk expansion

---

## PromptBuilder

Constructs structured prompts for chat-based LLMs.

Responsibilities

- System Prompt
- User Prompt
- Transcript Context
- User Query

---

## LLMService

Responsible for all interactions with external language models.

Current provider

```
Groq
```

Designed to support multiple providers in the future without modifying retrieval logic.

## Conversational AI

- Create chat sessions
- Store chat messages
- Session-based AI conversations
- Multiple conversations per transcript

---

# Technologies

| Category | Technology |
|-----------|------------|
| Language | Python 3.13 |
| API | FastAPI |
| ORM | SQLAlchemy 2.x |
| Database | PostgreSQL |
| Object Storage | AWS S3 |
| Queue | RabbitMQ |
| Background Tasks | Celery |
| Vector Database | ChromaDB |
| Embeddings | Sentence Transformers |
| Reranking | Cross Encoder |
| LLM | Groq |
| Containers | Docker & Docker Compose |

---

# Current Capabilities

## User Management

- Registration
- Authentication
- JWT Authorization

## Todo Management

- CRUD Operations

## Transcript Processing

- Upload transcripts
- Store in AWS S3
- Background ETL
- Automatic embeddings
- Vector indexing

## Semantic Retrieval

- Dense Vector Search
- Metadata filtering
- Cross Encoder reranking

## Retrieval-Augmented Generation

- Context creation
- Prompt generation
- AI-generated answers from transcript knowledge

---

# API Overview

## Authentication

```
POST /auth/register
POST /auth/login
```

## Todo

```
GET    /todos
POST   /todos
PUT    /todos/{id}
DELETE /todos/{id}
```

## Transcript

```
POST /transcripts/upload
GET  /transcripts
```

## Semantic Search

```
POST /transcripts/{transcript_id}/search
```

## Conversational AI

```
POST /transcripts/{transcript_id}/sessions
GET /transcripts/{transcript_id}/sessions
GET /sessions/{session_id}
DELETE /sessions/{session_id}

POST /sessions/{session_id}/chat
GET /sessions/{session_id}/messages
```

---

## Roadmap

### Version 2.5

- Conversation memory
- Conversation summaries
- Last-N message retrieval
- Memory-aware prompt building
- Long-context conversations

---

# Running the Project

Clone the repository

```bash
git clone <repository-url>
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run Docker

```bash
docker compose up --build
```

Start FastAPI

```bash
uvicorn app.main:app --reload
```

---

# Environment Variables

Example

```env
DATABASE_URL=

SECRET_KEY=

AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_BUCKET_NAME=

RABBITMQ_URL=

EMBEDDING_PROVIDER=huggingface
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

RERANK_MODEL=cross-encoder/ms-marco-MiniLM-L-6-v2

CHROMA_DB_PATH=./chroma_db
CHROMA_COLLECTION_NAME=transcripts

LLM_PROVIDER=groq
LLM_MODEL=llama-3.3-70b-versatile
GROQ_API_KEY=
```

---

# Logging

Structured logging is enabled throughout the platform.

Logging includes

- API requests
- ETL processing
- Background workers
- Embedding generation
- Vector storage
- Retrieval
- LLM requests
- Error tracking

---

# Design Principles

- Modular Architecture
- Single Responsibility Principle
- Service-Oriented Design
- Replaceable Components
- Configurable AI Providers
- Production-Oriented ETL
- Asynchronous Processing
- Retrieval-Augmented Generation

---

#  License

This project is licensed under the **Apache License 2.0**.

See the [LICENSE](LICENSE)