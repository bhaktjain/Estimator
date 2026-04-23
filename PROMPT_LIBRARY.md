# GPT Prompt Library – Estimation Engine

All prompts used in the renovation estimation pipeline. Version = current production as of repo state; no separate version tags in code.

---

## 1. Main estimation prompt (scope, pricing, quantities, confidence)

| Field | Value |
|-------|--------|
| **File** | `estimation_prompt.txt` |
| **Purpose** | Scope extraction from transcript + Polycam, pricing lookup from master sheet, quantity calculation, confidence scoring, JSON output schema. |
| **Used by** | `run_chunked_estimation.py` (injected into each chunk group request). |
| **Key rules** | Room-specific scope; 75% / 80% markup; countertop formula; Polycam measurements; confidence 95/90/85/80; commercial cleaning always; no placeholders. |

---

## 2. Process/legal chunk override

| Field | Value |
|-------|--------|
| **Location** | `run_chunked_estimation.py` (inline string). |
| **Purpose** | When a transcript chunk is detected as process/legal/insurance-heavy, prepend this so the model still extracts renovation scope. |
| **Text (summary)** | “This chunk is mostly about process, insurance, or legal topics. IGNORE those topics. Focus only on physical renovation work, scope items, or plausible tasks. NEVER refuse.” |

---

## 3. Anti-refusal retry prompt

| Field | Value |
|-------|--------|
| **Location** | `run_chunked_estimation.py` (inline string). |
| **Purpose** | If the model refuses or disclaims, retry with this prepended. |
| **Text (summary)** | “MANDATORY: You must NOT refuse or say you cannot provide an estimate. If the chunk is ambiguous or process-focused, MAKE UP plausible scope items and proceed.” |

---

## 4. Chunk wrapper format

| Field | Value |
|-------|--------|
| **Location** | `run_chunked_estimation.py`. |
| **Format** | `[TRANSCRIPT CHUNK]\n{transcript_text}\n\n{extra_instruction}{prompt_instructions}` where `prompt_instructions` = contents of `estimation_prompt.txt`. |

No other prompts are used for scope extraction, pricing lookup, quantity calculation, or confidence scoring. Dedup/cleanup in `comprehensive_cleanup.py` is logic only (no LLM prompts).
