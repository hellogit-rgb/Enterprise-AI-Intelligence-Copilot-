# Architecture

## High-level flow

1. User submits a chat question in the React frontend.
2. The Node.js backend authenticates and routes request traffic.
3. The Python AI service performs intent classification and tool routing.
4. The orchestrator selects either a document search or SQL query path.
5. Retrieval and verification layers validate evidence before final answer generation.
6. The client receives a source-backed answer with citations and confidence score.

## Current implementation status

This repository is in Phase 1: app foundation and service scaffolding.

- frontend: working React shell for the enterprise dashboard and chat UI
- backend: Express health and chat endpoints
- ai-service: FastAPI health and route selection endpoints
- next focus: hybrid retrieval, SQL validation, RBAC, evaluation dataset
