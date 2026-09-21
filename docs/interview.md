# Interview Preparation

## 1. Why LangGraph?

Because the application needs explicit state and controlled transitions between specialized
nodes. A normal prompt chain is simpler, but this workflow needs routing, retrieval,
review, action boundaries and room for persistence/human approval.

## 2. Why RAG?

Enterprise policy changes frequently. RAG lets the system retrieve current approved source
content instead of expecting the model to memorize internal information.

## 3. Why MCP?

MCP provides a standard interface for exposing tools/resources/prompts to compatible AI
hosts. It separates tool integration from the agent's reasoning layer.

## 4. How do you reduce hallucinations?

- retrieve evidence
- require source citations
- instruct the policy agent to stay within evidence
- run a reviewer node
- return an explicit "insufficient evidence" response
- evaluate on a golden question set

## 5. How do you secure tool calls?

Never trust model output as authorization. Authenticate the user, authorize the requested
tool, validate arguments against a schema, apply allowlists, log the action and require
human approval for sensitive operations.

## 6. How do you scale?

Run stateless API replicas behind a load balancer. Store persistent state in a shared
database/checkpointer, use Redis for cache/rate limiting, and isolate long-running jobs
from synchronous request handling.

## 7. What would you monitor?

Latency, token usage/cost, error rate, retrieval hit quality, tool failure rate, model
fallbacks, timeouts, user feedback and unsafe/blocked requests.

## 8. How would you move this to Azure?

Azure OpenAI for models, Azure PostgreSQL for pgvector, Azure Cache for Redis, AKS or
Container Apps for workloads, Key Vault for secrets, managed identity for service access,
and Azure Monitor/Application Insights for telemetry.

## 9. What is the project contribution to the job requirements?

Agentic AI -> LangGraph workflow
RAG -> pgvector retrieval
GenAI -> Azure OpenAI
MCP -> MCP server/tools
Microservices -> FastAPI + MCP service boundary
REST -> /v1/chat
WebSocket -> /v1/ws/{thread_id}
Cloud -> Azure-first deployment mapping
CI/CD -> Jenkinsfile + GitHub Actions
LLM lifecycle -> model adapter, tests, observability
Enterprise -> authorization/audit/guardrail design
