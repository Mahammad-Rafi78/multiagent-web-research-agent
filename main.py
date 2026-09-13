from __future__ import annotations

import sys

from app.agent import ResearchAgent


def main() -> None:
    if len(sys.argv) > 1:
        question = " ".join(sys.argv[1:])
    else:
        question = input("Research question: ").strip()

    if not question:
        raise SystemExit("A research question is required.")

    agent = ResearchAgent()
    result = agent.run(question)
    print("\n--------------------------------------------------")
    print("RESEARCH ANSWER")
    print("--------------------------------------------------")
    print(result.answer)
    print("\n--------------------------------------------------")
    print("SUPPORTING CLAIMS")
    print("--------------------------------------------------")
    for index, claim in enumerate(result.supporting_claims, start=1):
        print(f"{index}. {claim}")
    print("\n--------------------------------------------------")
    print("REFERENCES")
    print("--------------------------------------------------")
    for ref in result.references:
        print(f"[{ref['id']}] {ref['title']}\n{ref['url']}")
    print("\n--------------------------------------------------")
    print("CONFLICTS")
    print("--------------------------------------------------")
    if result.conflicts:
        for conflict in result.conflicts:
            print(conflict.details)
    else:
        print("None detected")
    print("\n--------------------------------------------------")
    print("UNCERTAINTY / MISSING EVIDENCE")
    print("--------------------------------------------------")
    print(result.uncertainty)
    if result.missing_evidence:
        for item in result.missing_evidence:
            print(f"- {item}")
    print("\n--------------------------------------------------")
    print("RESEARCH RUN")
    print("--------------------------------------------------")
    stats = result.research_run or {}
    print(f"Providers queried: {len(stats.get('providers_attempted', []))}")
    print(f"Queries generated: {len(stats.get('queries', []))}")
    print(f"Raw results: {stats.get('raw_result_count', 0)}")
    print(f"Duplicates removed: {max(0, stats.get('raw_result_count', 0) - stats.get('deduplicated_result_count', 0))}")
    print(f"Sources selected: {stats.get('sources_selected', 0)}")
    print(f"Sources fetched: {stats.get('sources_fetched', 0)}")
    print(f"Sources unavailable: {stats.get('sources_unavailable', 0)}")
    print("Provider status:")
    for item in stats.get("provider_status", []):
        print(f"{item['provider']}: {item['status']}")


if __name__ == "__main__":
    main()
