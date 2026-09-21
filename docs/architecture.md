# Architecture Notes

## Agent flow

```text
START
  |
Router
  +---- general ------> Final
  |
  +---- retrieval ----> Retrieval -> Policy -> Reviewer -> Final
  |
  +---- action --------> Action -> Reviewer -> Final
```

## RAG

Documents are split into overlapping chunks, embedded, and stored in pgvector.
At query time the same embedding model is used to retrieve semantically similar chunks.
The retrieved text is explicitly passed to the policy agent.

## Agentic behavior

The important design choice is that the model does not directly control the whole application.
The graph controls transitions. Each node has a bounded responsibility.

## MCP

The MCP server standardizes access to external capabilities. The host/agent can discover
tools rather than relying on one-off tool wrappers. Write tools should be protected by
identity, authorization, validation and audit logging.

## Reliability

Recommended production controls:
- timeout every external call
- retry only idempotent operations
- circuit-break model/provider outages
- cache safe reads
- persist thread state
- use request IDs
- record tool calls
- add human approval to high-impact actions
