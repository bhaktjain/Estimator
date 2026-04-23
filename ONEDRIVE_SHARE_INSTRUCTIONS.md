# How to Share the Estimation Engine Deliverables via OneDrive

Eran asked for deliverables to be uploaded to a **shared AI Estimator folder** and to **connect via OneDrive**. Here’s how to do it from your machine (no Cursor/repo auto-sync to OneDrive).

---

## Step 1: Create the folder in OneDrive

1. Open **OneDrive** (browser at onedrive.com or the OneDrive app on your Mac).
2. Create a new folder, e.g. **`AI Estimator – Estimation Engine Deliverables`**.
3. Optionally create subfolders:
   - `01_source_code`
   - `02_master_pricing`
   - `03_vector_db_docs`
   - `04_env_config`
   - `05_sample_polycam`
   - `06_prompt_library`
   - `07_integration_docs`

(You can also put everything in one flat folder and use the README to navigate.)

---

## Step 2: Upload the files (from this repo)

From your project root (`custom gpt`):

| Deliverable | What to upload |
|-------------|----------------|
| **1. Source code** | Zip or copy: `run_chunked_estimation.py`, `comprehensive_cleanup.py`, `process_transcript.py`, `estimation_prompt.txt`, `requirements.txt`, and any other pipeline scripts you use. Optionally include `archive_non_pipeline_*` for legacy. |
| **2. Master pricing** | `master_pricing_data.csv` and, if you use it, `Master Pricing Sheet - Q1 - 2025 (2).pdf`. |
| **3. Vector DB** | `VECTOR_DB_README.md` (states no vector DB; chunk-based RAG only). |
| **4. Env config** | `env.example` (redacted; variable names and non-secret values). |
| **5. Sample Polycam** | 3–5 run folders from `chunked_outputs/run_*/` (each with `polycam_chunks/polycam.pdf` and any 3D files). Label which are studio / 1BR / 2BR+ if possible. |
| **6. Prompt library** | `estimation_prompt.txt` + a short `PROMPT_LIBRARY.md` listing prompts (see main deliverables README). |
| **7. Integration docs** | Link to https://platform.openai.com/docs and a one-liner that the pipeline uses OpenAI only. |
| **Index for Eran** | `ESTIMATION_ENGINE_DELIVERABLES_README.md` (so he knows what each deliverable is and where it is). |

---

## Step 3: Get a shareable OneDrive link

1. In OneDrive, **right‑click** the folder **`AI Estimator – Estimation Engine Deliverables`**.
2. Click **Share**.
3. Choose one:
   - **Share with people:** Enter Eran’s email → set permission (e.g. “Can edit” or “Can view”) → Send. He’ll get an email with access.
   - **Get link:** Click **Copy link**, set “Anyone with the link” or “Only people in [your org]” as required, then paste the link in an email to Eran.

---

## Step 4: Email Eran

You can send something like:

**Subject:** Estimation Engine deliverables – OneDrive

Hi Eran,

The Estimation Engine integration deliverables are in our shared AI Estimator folder on OneDrive.

**Link:** [paste the OneDrive folder link here]

**In the folder you’ll find:**
1. Source code (pipeline + prompts + cleanup; fork, production unchanged)
2. Master pricing sheet (CSV + optional PDF)
3. Vector DB note (this pipeline doesn’t use a vector DB; RAG is chunk-based)
4. Environment config (`.env.example` with variable names, keys redacted)
5. Sample Polycam outputs (3–5 runs with PDFs; labeled by unit size where possible)
6. GPT prompt library (estimation_prompt.txt + index)
7. Integration docs (OpenAI API reference)

The file **ESTIMATION_ENGINE_DELIVERABLES_README.md** in the folder maps each of your 8 deliverables to the exact files and locations.

Happy to jump on a quick call if anything is unclear.

Best,  
Bhakt

---

## “Connect to OneDrive” – what you can’t do from here

- **Cursor/this repo** cannot “log in” to OneDrive or push files automatically. You have to upload the files (or a zip) yourself.
- **OneDrive sync app:** If you install the OneDrive app and put your repo (or a copy) inside a synced folder, then the folder will sync to the cloud. You’d then share that folder with Eran as above. Your project is currently under `Desktop/custom gpt`, so unless that’s inside OneDrive, you still need to copy/zip the deliverables into a OneDrive folder and share the link.

So: **“Send connect to OneDrive”** = upload the deliverables into a OneDrive folder and send Eran the **share link** (and optional email) as above.
