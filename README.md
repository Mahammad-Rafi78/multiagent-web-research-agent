# Multi-Source Web Research Agent

A lightweight Python research agent that answers a question using more than one search provider and grounds the final answer in retrieved evidence instead of a single-search-result chain.

## Problem Understanding
A basic search -> LLM -> answer pipeline is not reliable enough for serious research. It often over-relies on a single provider, ignores duplicates and conflicting evidence, and can invent facts if the model is not constrained by retrieved sources. This project addresses those issues by combining multiple retrieval sources, normalizing and deduplicating results, ranking sources, fetching excerpts, verifying claims, and synthesizing a final answer with explicit uncertainty.

## Objectives
- Use at least two independent search providers
- Normalize and merge results from multiple sources
- Deduplicate overlapping results while preserving provenance
- Rank sources using explainable heuristics
- Fetch and inspect the most relevant pages
- Extract evidence and verify claims
- Detect conflicts and surface uncertainty
- Produce a concise final answer with citations and references
- Handle API failures, rate limits, and timeouts gracefully

## Features
- Query decomposition planner with fallback behavior
- Abstract search-provider interface for future extension
- Tavily and Brave implementations
- Normalization, deduplication, and ranking stages
- Webpage fetching and evidence extraction
- Claim verification and conflict detection
- LLM synthesis grounded only in supplied evidence
- Citation validation and resilient CLI execution
- Mock-friendly pytest suite

## Architecture

```text
User question
    |
    v
Query planner
    |
    +--> Tavily search provider
    |
    +--> Brave search provider
    |
    v
Normalization -> Deduplication -> Ranking
    |
    v
Fetch relevant pages -> Extract evidence -> Verify claims -> Detect conflicts
    |
    v
LLM synthesis with citations and uncertainty reporting
```

## End-to-End Flow
1. The user supplies a research question.
2. The planner generates a few focused search queries.
3. Both configured providers are queried.
4. Results are normalized, merged, and deduplicated.
5. Ranked sources are fetched for evidence extraction.
6. Relevant passages are pulled and claims are validated.
7. Conflicts and missing evidence are reported.
8. The final answer is synthesized with citations and explicit uncertainty.

## Project Structure

```text
multisource-web-research-agent/
├── app/
│   ├── __init__.py
│   ├── agent.py
│   ├── citations.py
│   ├── config.py
│   ├── conflicts.py
│   ├── deduplicator.py
│   ├── evidence.py
│   ├── fetcher.py
│   ├── logging_config.py
│   ├── models.py
│   ├── normalizer.py
│   ├── planner.py
│   ├── ranker.py
│   ├── search.py
│   ├── synthesizer.py
│   └── verifier.py
├── providers/
│   ├── __init__.py
│   ├── base.py
│   ├── brave.py
│   └── tavily.py
├── tests/
│   ├── __init__.py
│   ├── test_agent.py
│   ├── test_citations.py
│   ├── test_conflicts.py
│   ├── test_config.py
│   ├── test_deduplicator.py
│   ├── test_fetcher.py
│   ├── test_models.py
│   ├── test_normalizer.py
│   ├── test_planner.py
│   ├── test_ranker.py
│   └── test_verifier.py
├── .env.example
├── .gitignore
├── DEMO_SCRIPT.md
├── IMPLEMENTATION_NOTES.md
├── LICENSE
├── README.md
├── main.py
├── requirements.txt
└── .venv/
```

## Technology Choices
- Python 3.11: modern type hints and stable runtime support
- Pydantic: strongly typed models and validation
- httpx: HTTP client with timeout and retry-friendly behavior
- BeautifulSoup: readable text extraction from HTML pages
- python-dotenv: environment-variable configuration
- tenacity: bounded retry behavior
- pytest: fast automated checks
- OpenAI, Gemini, Groq, and OpenRouter: selectable final synthesis providers
- Tavily and Brave Search: two independent search sources

## Setup

### Create a virtual environment

Windows:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

## Environment Variables
Create a local `.env` file based on `.env.example` and fill in your API keys.

The minimum configuration for a live, evidence-grounded answer is:

```env
OPENAI_API_KEY=your_openai_key
# Or use one of these alternatives:
# GEMINI_API_KEY=your_gemini_key
# GROQ_API_KEY=your_groq_key
# OPENROUTER_API_KEY=your_openrouter_key
TAVILY_API_KEY=your_tavily_key
```

`OPENAI_API_KEY` is used to generate the final answer. `TAVILY_API_KEY` and
`BRAVE_API_KEY` are used for web retrieval; configure both for multi-provider
search, or configure Tavily alone for a simpler local run. Obtain keys from
the providers' official dashboards, and never paste a secret into source code
or commit it to Git.

Set `LLM_PROVIDER` to `openai`, `gemini`, `groq`, or `openrouter` to choose a
specific model provider. The default `auto` mode uses the first configured
provider in that order. Use the matching model variables to override defaults.

```env
OPENAI_API_KEY=
TAVILY_API_KEY=
BRAVE_API_KEY=
OPENAI_MODEL=gpt-4o-mini
REQUEST_TIMEOUT=20
MAX_RETRIES=3
MAX_SEARCH_RESULTS=8
MAX_SOURCES_TO_FETCH=5
MAX_EVIDENCE_ITEMS=6
```

Never commit real API keys. The repository intentionally ignores `.env` in `.gitignore`.

## Execution

CLI mode:

```bash
python main.py "What are the main advantages and limitations of RAG?"
```

Interactive mode:

```bash
python main.py
```

Browser UI:

```bash
python ui_server.py
```

Open `http://127.0.0.1:8000`, enter a question, and select **Run research**.
The UI falls back to a clearly labelled demo response when a live provider or
the LLM is unavailable.

## Deploy on Render

This repository includes `Dockerfile` and `render.yaml` deployment settings.
To deploy, push the project to GitHub, create a new Render Blueprint, and
select the repository. In the service environment settings, enter fresh
values for `GEMINI_API_KEY` and `TAVILY_API_KEY` without committing them.
Render will build the container, use the injected `PORT`, and check `/health`.

The same `Dockerfile` can be deployed to any container host that supports
Docker. Configure the provider keys as runtime environment variables and keep
`/health` as the health-check URL.

## Example Input

```text
What are the main advantages and limitations of retrieval-augmented generation compared with fine-tuning for enterprise AI applications?
```

## Example Output

```text
RESEARCH ANSWER
...
SUPPORTING CLAIMS
1. Retrieval-augmented generation reduces the need to retrain models for each new knowledge update.
REFERENCES
[S1] Example source title
https://example.com/source
CONFLICTS
None detected
UNCERTAINTY / MISSING EVIDENCE
Evidence is limited to the retrieved sources; the answer may omit edge cases.
```

## Query Planning
The planner tries to decompose the question into a small, high-signal set of precise queries. For simple questions it may generate 1-2 queries; for more complex prompts, it can generate several focused searches without exploding the search budget.

## Multi-Source Retrieval
Using two independent providers reduces dependence on any single search ecosystem and improves evidence diversity. Even if one provider fails or returns poor results, the pipeline can still answer from the other provider.

## Normalization
All provider responses are normalized into the same result schema. This includes whitespace cleanup, title normalization, snippet sanitization, and URL canonicalization. The URL normalization removes tracking parameters such as UTM values and strips fragments when appropriate.

## Deduplication
Duplicate sources are collapsed by their normalized URL. This preserves provenance while avoiding duplicate evidence. If the same article is returned by both Tavily and Brave, the system keeps one source record and records both providers as having discovered it.

## Source Ranking
The ranking stage uses an explainable scoring approach based on relevance, authority, freshness, and evidence quality. The design deliberately avoids claiming that a rank is objectively perfect; it is simply a structured heuristic to prioritize the best available evidence.

## Web Fetching
The fetcher uses httpx with timeouts and follows redirects carefully. It extracts readable text from pages and handles common failures such as 404s, 403s, 429s, timeouts, and invalid HTML without crashing the full pipeline.

## Evidence Extraction
Relevant passages are drawn from fetched sources and tied back to the original source, title, URL, and provider. This keeps the evidence traceable and prevents the LLM from inventing unsupported facts.

## Verification
The verifier marks claims as supported, partially supported, conflicting, unsupported, or insufficient evidence. This is intentionally conservative and avoids claiming support without direct evidence.

## Conflict Handling
When sources disagree, the system records the conflict and warns the synthesis stage. It does not silently choose one side unless the evidence clearly supports it.

## Hallucination Mitigation
The synthesis prompt explicitly instructs the model to answer only from the supplied evidence, cite only real source IDs, and clearly note uncertainty or missing evidence. Retrieved webpage text is treated as data, not as instructions.

## Prompt Injection Considerations
Webpages may contain instructions that appear to override system behavior. The system treats retrieved content as untrusted data, not as operational instructions. It never exposes secrets or internal prompts to the webpage environment.

## Reliability
The system implements:
- request timeouts
- bounded retries with exponential backoff
- rate-limit awareness
- provider failure handling
- graceful degradation when a provider is unavailable
- structured logging without leaking credentials

## API Limits
Exact API limits depend on the current provider plan and documentation. This project does not assume fixed quotas; instead it handles failures gracefully and treats quota-related errors as recoverable conditions.

## Security
- API keys are stored in environment variables
- `.env` is excluded from version control
- logs avoid printing credentials
- fetched webpage content is treated as untrusted input

## Testing
The project includes mocked pytest tests covering models, planner fallback behavior, normalization, deduplication, ranking, fetch behavior, verification, conflicts, citation validation, and integration-style execution.

## Known Limitations
- Search results depend on provider coverage and keyword quality
- Web extraction is simple and may miss some nuanced passages
- The system is not a full production retrieval engine
- Final answer quality remains dependent on the evidence retrieved and the model used

## Future Improvements
- Add caching and asynchronous fetching
- Support more providers and better source weighting
- Add stronger claim extraction and evaluation benchmarks
- Improve observability and persistent research history
- Add a small Streamlit UI for demo use

## Design Trade-offs
The architecture favors clarity and maintainability over maximal complexity. It is intentionally narrow and easy to explain during an interview, while still demonstrating real retrieval, verification, and synthesis behavior.

## Reproducibility
The project is designed to be reproducible with a Python virtual environment, a pinned dependency set, and example environment variables in `.env.example`. The tests use mocked APIs so that regression checks remain stable without real external access.
