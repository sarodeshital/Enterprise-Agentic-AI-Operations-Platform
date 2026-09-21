# Enterprise Agentic AI Platform — Multi-Agent RAG + MCP

Production-oriented reference implementation for an enterprise AI assistant that combines:

- LangGraph stateful multi-agent orchestration
- LangChain model/tool abstractions
- RAG over enterprise documents with PostgreSQL + pgvector
- MCP tool server
- Azure OpenAI as the primary LLM provider
- Provider abstraction for Azure / AWS Bedrock / Google Gemini
- FastAPI REST API + WebSocket streaming
- Redis-backed short-term state/cache
- Event-driven audit events
- Guardrails, citations, tool allowlists, retries and structured outputs
- Docker Compose for local development
- Jenkins CI/CD
- Kubernetes manifests
- Prometheus-style health/metrics endpoint
- Pytest unit tests

> This is a portfolio/learning implementation. Replace secrets, authentication, authorization,
> network policies, model endpoints and compliance controls before production use.

## Business use case

An enterprise employee asks questions such as:

- "What is our travel reimbursement policy?"
- "Find the latest approved security exception procedure."
- "Create a support ticket for the incident described below."
- "Summarize the relevant policy and show the sources."

The system routes work through specialized agents:

1. Router Agent — classifies the request.
2. Retrieval Agent — searches the vector index and returns grounded context.
3. Policy Agent — interprets retrieved policy text.
4. Action Agent — proposes or executes an approved enterprise tool.
5. Reviewer Agent — checks grounding, citations and unsafe/unsupported claims.
6. Final Agent — produces the user-facing answer.

MCP exposes enterprise tools through a standard tool interface.

## Architecture

```text
                       +----------------------+
                       |       Client         |
                       | Web / API / Copilot  |
                       +----------+-----------+
                                  |
                         REST / WebSocket
                                  |
                       +----------v-----------+
                       |       FastAPI        |
                       | Auth boundary / API  |
                       +----------+-----------+
                                  |
                       +----------v-----------+
                       |     LangGraph        |
                       | stateful workflow    |
                       +----------+-----------+
                                  |
            +---------------------+----------------------+
            |                     |                      |
     +------v------+       +------v------+        +------v------+
     | Router      |       | Retrieval   |        | Action      |
     | Agent       |       | Agent       |        | Agent       |
     +------+------+       +------+------+        +------+------+
            |                     |                      |
            |              +------v------+               |
            |              | PostgreSQL  |               |
            |              | + pgvector  |               |
            |              +-------------+               |
            |                                             |
            |                                      +------v------+
            |                                      | MCP Server  |
            |                                      | tools       |
            |                                      +------+------+
            |                                             |
            |                                  +----------+----------+
            |                                  | ticket / policy /  |
            |                                  | employee systems   |
            |                                  +---------------------+
            |
     +------v------+
     | Reviewer    |
     +------+------+
            |
     +------v------+
     | Final LLM   |
     +-------------+

 Observability: structured logs + metrics + audit events
 CI/CD: GitHub -> Jenkins -> tests -> Docker -> registry -> Kubernetes
```

LangGraph is used because it is designed for long-running, stateful agent orchestration,
including persistence, streaming and human-in-the-loop patterns.

## Repository layout

```text
enterprise-agentic-ai-platform/
├── app/
│   ├── api.py
│   ├── config.py
│   ├── graph.py
│   ├── llm.py
│   ├── schemas.py
│   ├── observability.py
│   ├── rag/
│   │   ├── chunking.py
│   │   ├── embeddings.py
│   │   └── store.py
│   ├── agents/
│   │   ├── router.py
│   │   ├── retrieval.py
│   │   ├── policy.py
│   │   ├── action.py
│   │   ├── reviewer.py
│   │   └── final.py
│   └── services/
│       └── tools.py
├── mcp_server/
│   └── server.py
├── scripts/
│   └── ingest.py
├── tests/
│   ├── test_api.py
│   ├── test_graph.py
│   └── test_rag.py
├── docs/
│   ├── architecture.md
│   └── interview.md
├── k8s/
│   ├── deployment.yaml
│   └── service.yaml
├── .github/workflows/
│   └── ci.yml
├── Dockerfile
├── docker-compose.yml
├── Jenkinsfile
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Language focus

The application is **Python-first**. The AI agents, LangGraph orchestration, RAG pipeline, API, MCP integration, ingestion and tests are implemented in Python. Docker, Kubernetes and Jenkins files are deployment infrastructure.

## Quick start

### 1. Clone

```bash
git clone https://github.com/<your-user>/enterprise-agentic-ai-platform.git
cd enterprise-agentic-ai-platform
```

### 2. Create environment

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate

pip install -r requirements.txt
copy .env.example .env
```

### 3. Configure Azure OpenAI

Set these in `.env`:

```env
AZURE_OPENAI_ENDPOINT=https://YOUR-RESOURCE.openai.azure.com/
AZURE_OPENAI_API_KEY=YOUR_KEY
AZURE_OPENAI_API_VERSION=2025-01-01-preview
AZURE_OPENAI_CHAT_DEPLOYMENT=YOUR_CHAT_DEPLOYMENT
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=YOUR_EMBEDDING_DEPLOYMENT
```

The code intentionally keeps model access behind `app/llm.py`, so the graph does not depend
directly on a vendor-specific client.

### 4. Start infrastructure

```bash
docker compose up -d postgres redis
```

### 5. Run API

```bash
uvicorn app.api:app --reload --port 8000
```

Open:

```text
http://localhost:8000/docs
```

Health:

```text
http://localhost:8000/health
```

### 6. Ingest a document

Put `.txt` or `.md` files under `data/` and run:

```bash
python scripts/ingest.py
```

### 7. Query

```bash
curl -X POST http://localhost:8000/v1/chat \
  -H "Content-Type: application/json" \
  -d "{\"message\":\"What is the travel reimbursement policy?\"}"
```

## WebSocket

```text
ws://localhost:8000/v1/ws/{thread_id}
```

Send:

```json
{"message":"Summarize the travel policy and cite the source."}
```

## MCP

Start the MCP server:

```bash
python -m mcp_server.server
```

The sample MCP server exposes:

- `search_policy`
- `create_support_ticket`
- `get_employee_profile`

Keep write/action tools behind authentication and authorization in real deployments.

## Docker

```bash
docker build -t enterprise-agentic-ai:latest .
docker run --env-file .env -p 8000:8000 enterprise-agentic-ai:latest
```

## CI/CD

Jenkins pipeline stages:

1. Checkout
2. Install
3. Lint
4. Unit tests
5. Build image
6. Security scan hook
7. Push image
8. Deploy to Kubernetes

The Jenkinsfile intentionally leaves registry credentials/deployment environment-specific.

## Cloud mapping

Primary reference deployment:

```text
Azure OpenAI / Azure AI platform
        |
Azure Container Apps or AKS
        |
Azure Database for PostgreSQL + pgvector
        |
Azure Cache for Redis
        |
Azure Monitor / Application Insights
```

Equivalent provider mapping:

| Capability | Azure | AWS | GCP |
|---|---|---|---|
| LLM | Azure OpenAI | Bedrock | Gemini |
| Containers | AKS / Container Apps | EKS / ECS | GKE / Cloud Run |
| PostgreSQL | Azure PostgreSQL | RDS PostgreSQL | Cloud SQL |
| Object store | Blob Storage | S3 | Cloud Storage |
| Secrets | Key Vault | Secrets Manager | Secret Manager |
| Monitoring | Azure Monitor | CloudWatch | Cloud Monitoring |

The application layer should remain provider-neutral; only the model/infrastructure adapters
should change.

## Production hardening checklist

- OIDC/JWT authentication
- RBAC and per-tool authorization
- managed identity / workload identity
- Key Vault / Secrets Manager instead of `.env`
- private networking and egress controls
- prompt injection detection
- PII redaction
- tool input validation
- human approval for destructive tools
- rate limiting
- retries with exponential backoff
- circuit breakers
- request/trace IDs
- LLM cost and latency metrics
- retrieval quality evaluation
- golden test set
- model/version pinning
- data retention policy
- audit trail

## What to say in an interview

"I built a production-oriented multi-agent enterprise assistant rather than a single
chatbot. FastAPI exposes REST and WebSocket interfaces. LangGraph manages the stateful
workflow. A router decides whether a request needs retrieval or an action. The retrieval
agent searches pgvector and passes citations to downstream agents. MCP standardizes access
to enterprise tools. A reviewer node checks grounding and tool safety before the final
response. The service is containerized, tested in CI, and deployable to Kubernetes. Azure
OpenAI is the primary model provider, while the LLM adapter keeps the architecture portable."

Be ready to explain:
- why LangGraph instead of a simple chain
- why RAG instead of putting all documents in the prompt
- why MCP instead of hard-coded tool wrappers
- how you prevent prompt injection
- how you control hallucinations
- how you handle retries/timeouts
- how you measure retrieval quality
- how you scale WebSocket and REST workloads
- how you secure secrets and tool execution
- how you reduce LLM latency/cost
