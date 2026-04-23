# Vector Database – Estimation Engine

## Status: Not used

This **Renovation AI Estimator** pipeline does **not** use Pinecone, Weaviate, or any vector database.

## How “RAG” works here

- **Transcript:** Split into text chunks by token count (see `process_transcript.py`; chunk size ~1500 tokens per transcript chunk).
- **Polycam:** One PDF (measurement report) per run; attached in full or as a single chunk to the model.
- **Groups:** `run_chunked_estimation.py` groups transcript chunks so each API call stays under `--max_tokens` (default 10,000).
- **No embeddings:** No embedding model or vector index; the “retrieval” step is fixed chunking + attaching the pricing PDF and Polycam PDF to each request.

## If you need “index config” for integration

| Concept | In this system |
|--------|-----------------|
| **Index** | List of transcript chunk files (e.g. `chunk_1.txt`, `chunk_2.txt`) plus one Polycam PDF path per run. |
| **Embedding model** | None. |
| **Dimensions** | N/A. |
| **Metadata filters** | None. |
| **Service** | None (no vector DB). |

## Embedding generation script

N/A. To replicate retrieval behavior, use the same chunking logic in `run_chunked_estimation.py` and `process_transcript.py` (by token count, no embeddings).
