# Demo Script

## 1. Introduction
This project is a multi-source web research agent designed for a technical assessment. The goal is to answer a research question using more than one search provider and to ground the answer in retrieved evidence instead of a single search result passed directly to an LLM.

## 2. Problem
A naive pipeline often performs one search, passes the first few results into a model, and produces an answer with little verification. That approach is brittle, can miss key evidence, and tends to hallucinate unsupported details.

## 3. Architecture
The project is split into clear modules: query planning, provider abstraction, normalization, deduplication, ranking, fetching, evidence extraction, verification, conflict detection, synthesis, and citations. This modular design keeps the system understandable and makes adding a third search provider easy.

## 4. Live Demo
I will ask the system: "What are the main advantages and limitations of retrieval-augmented generation compared with fine-tuning for enterprise AI applications?" The planner creates focused queries, each provider searches independently, and the system merges and deduplicates results before ranking them.

## 5. Evidence and Citations
The agent fetches a small number of promising sources, extracts relevant passages, and verifies whether the key claims are supported. Each final answer includes citations tied to source IDs and URLs so the evidence trail is visible.

## 6. Reliability
The design includes timeouts, retries, provider failure handling, and graceful degradation. If one provider is slow or returns an error, the other source can still produce useful evidence.

## 7. Failure Case
I can simulate a provider outage during testing to show the resilience of the system. In that case, the pipeline continues with the remaining provider and reports the failure clearly instead of crashing.

## 8. Engineering Decisions
I chose a lightweight custom architecture instead of LangChain so the logic stays inspectable. Pydantic gives strong typing, while a modular file layout makes the system easy to explain in an interview.

## 9. Trade-offs
This project intentionally avoids huge infrastructure. It is small, testable, and fast to explain, but it does not attempt full-scale retrieval benchmarking or a production-grade evaluation framework.

## 10. Limitations
The model does not guarantee perfect extraction or perfect conflict resolution. Search results are limited by provider coverage and API constraints, and the final answer is bounded by the evidence retrieved.

## 11. Future Improvements
Possible next steps include caching, asynchronous fetching, better claim extraction, stronger evaluation datasets, and observability for long-running research runs.
