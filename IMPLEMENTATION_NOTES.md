# Implementation Notes

## Approach
The project implements a lightweight retrieval pipeline that combines focused query planning, multi-source search, normalization, deduplication, ranking, fetching, evidence extraction, and LLM-grounded synthesis. The goal is to answer a question with explicit evidence and transparent uncertainty, not to pretend the model knows the answer without sources.

## Architecture
The system is modular, with separate components for planning, provider access, normalization, deduplication, ranking, fetching, verification, conflict detection, and final synthesis. This makes the intern assessment easier to explain and easier to test.

## Personally Implemented Components
The project includes:
- a modular Python package under `app/`
- provider implementations for Tavily and Brave
- orchestration and CLI entry points
- Pydantic models
- deduplication and ranking utilities
- fetch and evidence extraction stages
- conflict detection and synthesis logic
- pytest coverage for core behaviors

## Key Decisions
- A custom lightweight architecture was chosen instead of LangChain to keep logic explicit.
- Search providers are abstracted behind a common interface to ease extension.
- URL normalization and deduplication protect against duplicate results from the same source.
- The synthesis layer is explicitly evidence-bound and rejects invalid citations.

## Technology Choices
- Python 3.11+ for a straightforward deployment environment
- Pydantic for typed models and validation
- httpx for resilient HTTP access
- BeautifulSoup for document text extraction
- python-dotenv for local configuration
- pytest for test automation
- OpenAI API for final answer synthesis
- Tavily and Brave as independent retrieval providers

## Trade-offs
The system is intentionally minimal and interview-friendly rather than a full production search engine. It does not include a full ranking benchmark or a huge evaluation pipeline, but it demonstrates the core engineering patterns well.

## Testing
The repository includes pytest checks for configuration, planner fallback behavior, normalization, deduplication, ranking, fetch recovery, conflict handling, citation validation, and an end-to-end mocked pipeline.

## Failure Handling
Provider errors, rate limits, timeouts, and fetch failures are handled as recoverable events. The system logs them and continues with the other provider when possible.

## Limitations
- Search quality depends on external provider coverage.
- The extraction stage is simple and may miss some high-value passages.
- The system does not guarantee fully exhaustive retrieval for broad or ambiguous questions.
- The LLM output must still be interpreted carefully as evidence-grounded synthesis, not as absolute truth.

## Future Improvements
- Add caching and async fetching
- Support more providers and better source weighting
- Add stronger claim extraction and evaluation datasets
- Improve observability and persistent research history
