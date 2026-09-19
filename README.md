# Enterprise AI Intelligence Copilot

An agentic enterprise AI platform for querying unstructured documents and structured business data with evidence-backed responses.

## Overview

This project combines:

- React frontend for enterprise chat and dashboards
- Node.js backend for authentication, APIs, and app services
- Python AI service for agent routing, retrieval, verification, and evaluation
- Hybrid retrieval patterns with semantic and keyword search
- SQL tool validation and role-aware access controls

## Project structure

- `frontend/` – React UI
- `backend/` – Express API
- `ai-service/` – Python AI service
- `docs/` – project documentation
- `evaluation/` – evaluation assets and results
- `infrastructure/` – Terraform and deployment configuration

## Getting started

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Backend

```bash
cd backend
npm install
npm run dev
```

### AI service

```bash
cd ai-service
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## Current status

This repository is now scaffolded with the foundational frontend and service layers needed for the first phase of the project. The next steps are to add:

1. a proper document ingestion flow,
2. hybrid retrieval and reranking,
3. SQL validation and tool routing,
4. evaluation and observability.

## Key features in the initial build

- enterprise dashboard mockup
- chat experience UI
- backend health + chat endpoints
- AI service route planning and retrieval mock endpoints
- project structure aligned to the final architecture

## Architecture summary

```text
React UI -> Node API -> Python AI Service -> Agent Orchestrator -> Retrieval + SQL + Verification
```

## License

MIT
