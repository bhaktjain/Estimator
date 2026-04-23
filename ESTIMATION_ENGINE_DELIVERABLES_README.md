# Estimation Engine – Deliverables for Integration (Eran)

This README maps **Eran’s 8 requested deliverables** to assets in this repo. Use it to upload the right files to the shared AI Estimator folder (e.g. OneDrive) and to email him.

---

## 1. Source Code (full codebase – fork, do not modify production)

**What to pack:** Full repo or a zip of the following (no changes to production).

| Asset | Location |
|-------|----------|
| **Pipeline & prompts** | `run_chunked_estimation.py` (orchestration, chunking, token limits, prompt assembly) |
| **Scope extraction / estimation prompt** | `estimation_prompt.txt` (main GPT prompt: scope, pricing, quantities, confidence) |
| **Dedup & cleanup** | `comprehensive_cleanup.py` (aggregate chunk outputs, dedup, section order, Excel creation) |
| **Transcript chunking** | `process_transcript.py` (creates transcript chunks) |
| **Pricing lookup / validation** | `comprehensive_cleanup.py` (reads `master_pricing_data.csv`, validates codes) |
| **Quantity / confidence** | In `estimation_prompt.txt` (confidence 95/90/85/80); calculations in prompt + cleanup |
| **RAG-style config** | Chunk-based: `--max_tokens` (default 10000), transcript chunk size 1500 tokens; see `run_chunked_estimation.py` |
| **Requirements** | `requirements.txt` (root) |

**Include:** All of the above files plus any scripts under `chunked_outputs/` that are part of the pipeline (e.g. `create_final_excel.py`). Optional: `archive_non_pipeline_20250909_091152/` for legacy/API variants.

---

## 2. Master Pricing Sheet

**Single source of truth:** `master_pricing_data.csv` (root).

- **Columns:** Item Code, Description, Size/Type, Unit, Labor, Material, Category, Subcategory, Notes, Margin, Minimum  
- **Markup rules:** Margin column = 0.75 (most) or 0.80 (tile/bath). Cost = Labor × (1 + Margin) + Material; use max(Minimum, that) per unit.  
- **Countertop formula:** See `estimation_prompt.txt` (e.g. $1,500 install + $97/SF × SF + $2,000 material) × 1.75.  
- **Conditional pricing:** Size/Type bands (e.g. 0–60 SF, 60–80 SF) and Notes in CSV.

Also reference: `Master Pricing Sheet - Q1 - 2025 (2).pdf` if you use a PDF version; include it in the folder if that’s the “production” reference.

---

## 3. Vector Database Export

**Status:** This pipeline does **not** use Pinecone, Weaviate, or any vector DB.

- **Current “RAG”:** Chunked transcript (text) + full Polycam PDF (or chunks) sent to GPT per group; no embeddings or vector index.  
- **What to deliver:** A short **README** (e.g. `VECTOR_DB_README.md`) stating: “No vector DB. RAG is chunk-based: transcript split by token limit (see run_chunked_estimation.py), Polycam PDF attached per request. Embedding generation script: N/A. Index: N/A.”  
- **If Eran still wants “index config”:** Provide chunk config: `max_tokens` (10000), transcript chunk size (1500), and that “index” = list of transcript chunk files + one Polycam PDF per run.

---

## 4. Environment Configuration

**Create and upload:** `.env.example` (redacted).

- **Variables used in code:** `OPENAI_API_KEY` (required), `OPENAI_MODEL`, `OPENAI_EMBEDDING_MODEL` (if any), `MAX_TOKENS`, `TEMPERATURE`, `PORT`, `FLASK_ENV`.  
- **Chunking:** In code, not env: `--max_tokens` default 10000, transcript `--max_tokens` 1500.  
- **Redact:** All API keys (use `OPENAI_API_KEY=<REDACTED>`).  
- **Keep:** Model names (e.g. gpt-4o), non-secret values. See `env.example` in this repo (created below).

---

## 5. Sample Polycam Outputs

**What to pack:** 3–5 complete Polycam “export packages” (PDF measurement report + 3D model files if you have them).

- **Where they live:** Under `chunked_outputs/run_*/polycam_chunks/` (e.g. `polycam.pdf`).  
- **Sizes:** Prefer runs that correspond to studio, 1BR, 2BR+ (label in a small `polycam_samples_index.csv`: run id, unit type, notes).  
- **Format:** One folder per sample: `polycam.pdf` + any .obj/.glb or other 3D exports you normally use.

---

## 6. GPT Prompt Library

**Single main prompt:** `estimation_prompt.txt`.

- **Contents:** Scope extraction, room-by-room rules, markup (75%/80%, countertop formula), Polycam measurement use, confidence scoring, output JSON schema.  
- **Versioning:** If you have git history or dated copies, note “current production = estimation_prompt.txt as of [date].”  
- **Other prompts:** In `run_chunked_estimation.py` (anti-refusal, process/legal chunk note). Extract those into a `PROMPT_LIBRARY.md` or second file listing: name, purpose, location, and 1–2 line description.

---

## 7. Integration Docs / API References

**APIs used:** OpenAI (Chat Completions / Files API) only.

- **Docs:** https://platform.openai.com/docs (reference only; no internal API spec).  
- **Internal “API”:** The pipeline is CLI-driven (`run_chunked_estimation.py` + `comprehensive_cleanup.py`). No REST API in this repo unless you include `archive_non_pipeline_*` (FastAPI/Flask). If you include archive, add one line per file: “Legacy FastAPI/Flask app – not current production pipeline.”

---

## 8. Delivery

- **Upload:** All of the above into the **shared AI Estimator folder** (e.g. OneDrive).  
- **Email Eran:** “Deliverables are in the shared AI Estimator folder. See ESTIMATION_ENGINE_DELIVERABLES_README.md for the map. OneDrive link: [paste link].”

---

## OneDrive: How to share the folder with Eran

1. **Create a folder** (e.g. “AI Estimator – Estimation Engine Deliverables”) in your OneDrive.  
2. **Upload** the files and folders as listed above (source code zip or copy, CSV, prompts, .env.example, Polycam samples, READMEs).  
3. **Share the folder:** Right‑click folder → Share → “Share with Eran” (email) or “Copy link” → set to “Anyone with the link” or “Only people in your org” as appropriate → send link to Eran.  
4. **Optional:** Send the same link by email with the short note above.

You cannot “connect” Cursor or this repo to OneDrive automatically; you upload the files (or a zip) manually and then share the OneDrive link.
