# LLM Agent Swarm Challenge

## Agent Swarm Workflow

![alt text](https://github.com/filipef9/llm-agent-swam-challenge/blob/develop/agent-swarm-api/agent-swarm-graph.png?raw=true)

This project implements a multi-agent Large Language Model (LLM) system using a swarm intelligence
approach. It leverages modern frameworks and tools to provide a scalable and efficient solution
for conversational and Retrieval-Augmented Generation (RAG) tasks.

## Features

* **Multi-Agent System:** Built using the **LangGraph** framework to orchestrate multiple LLM agents.
* **FastAPI Backend:** The agents are exposed through a RESTful API implemented with **FastAPI**.
* **RAG Pipeline:** A Retrieval-Augmented Generation pipeline powered by **LangChain** components.
* **Vector Database:** Utilizes **Qdrant** for efficient vector-based Retrieval-Augmented Generation.
* **Document Loading:** Knowledge base populated from URLs using **Docling** and **DoclingLoader** (via LangChain).
* **EmEmbedding Model:** **Uses sentence-transformers/paraphrase-multilingual-mpnet-base-v2** for generating embeddings.

## Architecture

The project consists of two main components:
1. **Agent API:** The FastAPI-based interface for interacting with the multi-agent LLM system.
2. **RAG Pipeline:** A LangChain-powered pipeline for retrieval-augmented generation, integrated
with Qdrant for vector storage and retrieval.

## Getting Started

### Prerequisites

* Docker and Docker Compose installed.

### Setup

To run the project locally, follow these steps:

1. Copy the `.env.template` file and rename it to `.env`, then fill in the required environment variables:

2. Start the services using Docker Compose:
```bash
docker-compose up -d
```

3. Monitor the service logs to ensure everything starts correctly:
```bash
docker-compose logs -f
```

4. Once the services are up:
   - The **Qdrant vector database** wil be available at `http://localhost:6333`
   - The **API server** will be accessible at `http://localhost:8080`

### Testing the API

You can perform a quick test using the Swagger UI provided by FastAPI, available
at `http://localhost:8080/docs`. Use the interactive interface to send requests
to the `POST /chat` endpoint.

Alternatively, you can test the API using `curl`. Example:
```bash
curl -X POST http://localhost:8080/chat \
-H "Content-Type: application/json" \
-d '{"message": "Quais as principais notícias de São Paulo hoje?", "user_id": "client789"}'
```

## Technologies Used
- **LangGraph**: Framework for orchestrating multi-agent LLM workflows.
- **FastAPI**: High-performance API framework for Python.
- **LangChain**: Components for building the RAG pipeline.
- **Qdrant**: Vector database for efficient similarity search.
- **Docling & DoclingLoader**: Tools for loading and processing documents from URLs.
- **Sentence Transformers**: Embedding model (`paraphrase-multilingual-mpnet-base-v2`) for multilingual text embeddings.