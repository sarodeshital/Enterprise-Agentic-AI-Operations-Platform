"""Command-line entry point for the enterprise agentic AI platform."""

import argparse

from app.graph import run_agent


def main() -> None:
    parser = argparse.ArgumentParser(description="Enterprise Agentic AI CLI")
    parser.add_argument("message", help="Question or action request for the agent")
    args = parser.parse_args()

    result = run_agent(args.message)
    print(result.get("answer", ""))

    citations = result.get("citations", [])
    if citations:
        print("\nCitations:")
        for item in citations:
            print(f"- {item['source']} ({item['chunk_id']})")


if __name__ == "__main__":
    main()
