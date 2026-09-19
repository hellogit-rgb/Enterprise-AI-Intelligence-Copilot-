# Enterprise AI Intelligence Copilot

## Purpose

Enterprise AI Intelligence Copilot is an agentic enterprise knowledge system designed to answer questions across both unstructured documents and structured business data. The platform combines document retrieval, SQL-driven analytics, evidence verification, and confidence-aware workflows to help users query enterprise information through a single conversational interface.

The core purpose is to move beyond a basic chatbot and build a production-style AI system that can:

- answer questions from company contracts, reports, policies, and other documents
- answer analytic questions from sales and business data
- route queries to the correct tool automatically
- validate evidence before presenting an answer
- protect access to sensitive data using role-aware controls
- detect low-confidence situations and trigger review instead of guessing

## Full project description

This project is a flagship AI application for an enterprise environment. It demonstrates the full stack required for serious AI engineering work:

- React frontend for a business-facing interface
- Node.js backend for APIs, auth, and orchestration
- Python AI service for agent logic, retrieval, and verification
- Hybrid retrieval combining semantic search and BM25 keyword search
- SQL tool use for structured business data
- Citation-backed responses tied to retrieved evidence
- Confidence scoring and human review workflows
- Security controls for access, SQL validation, and prompt isolation
- Evaluation framework for measuring retrieval and answer quality
- Cloud-ready architecture for GCP deployment

The application is designed around the following enterprise scenarios:

- "What are Customer A's payment terms?"
- "Compare Customer A's contract terms with the standard company policy."
- "Which five customers generated the highest revenue?"
- "Why did revenue decrease in March?"
- "Which customers have overdue payments and what do the contracts say about late penalties?"

These examples require both document search and structured data reasoning, which is why the system combines search, SQL, and verification layers.

## What we have achieved so far

The project has reached a working foundation and a meaningful first version of the AI architecture.

### Completed work

- Monorepo structure created for frontend, backend, AI service, docs, evaluation, and infrastructure
- React-based enterprise dashboard and chat shell implemented
- Express backend created with health and chat endpoints
- FastAPI AI service created with agent routing, retrieval, and verification routes
- Hybrid semantic + BM25 retrieval implemented using real text chunks
- Metadata-aware chunking system added for document sections and pages
- Query rewriting support for ambiguous follow-up questions like “What about payment?”
- SQL tool abstraction created with safe allowed operations and blocked destructive statements
- Evidence verification logic implemented for claim validation
- Evaluation dataset scaffold added for future testing
- Docker and infrastructure starter files added for deployment readiness
- Project documentation file created to track architecture and implementation status

### Current system capabilities

At this stage, the project already demonstrates:

- enterprise UI shell
- backend API orchestration
- AI routing between document and SQL flows
- hybrid retrieval using vector similarity and keyword matching
- chunked document retrieval with page/section metadata
- safe SQL operation validation
- verification hooks for numeric evidence checks

## What is left to build

The remaining work is still substantial, but it follows a clean build order to avoid building too much at once.

### High-priority remaining work

1. Document upload and ingestion pipeline
   - PDF parsing and text extraction
   - metadata extraction
   - chunk storage with document IDs, section names, pages, and chunk IDs

2. Advanced retrieval and reranking
   - top-k reranking
   - hybrid score tuning
   - improved recall and precision across real enterprise documents

3. SQL execution safety and query governance
   - allowed tables and column restrictions
   - query timeout enforcement
   - maximum row limits and data scan caps
   - read-only role identity

4. Confidence system and low-confidence retry flow
   - retrieval relevance scoring
   - source agreement scoring
   - citation verification score
   - human review trigger when confidence is low

5. Citation verification and answer generation
   - exact evidence mapping to answer claims
   - source-anchored final answer generation
   - unsupported claim re-generation flow

6. Access control and security
   - document authorization checks
   - role-based access control
   - prompt injection defense
   - PII masking and redaction strategy
   - rate limiting and input validation

7. Evaluation and observability
   - structured evaluation dataset with expected answers and sources
   - retrieval metrics such as recall, precision, hit rate, and MRR
   - answer correctness and citation correctness tracking
   - dashboards for latency, cost, and tool success rates

8. Deployment and cloud setup
   - Terraform or IaC for GCP resources
   - Cloud Run deployment configuration
   - BigQuery schema and sample business data
   - GitHub Actions for CI/CD

## Current status summary

This project is no longer just a concept or mock UI. It has a real foundation with working backend, retrieval, and AI routing logic, but it is still in an early-to-mid implementation stage. The architecture is sound and the next steps are all focused on real enterprise readiness rather than cosmetic features.

## Recommended next milestone

The next milestone should be:

- secure SQL layer
- confidence engine
- evidence verification
- evaluation metrics
- ingestion improvements

Once those are in place, the project will be convincingly close to the final enterprise AI copilot architecture described in the original specification.
