# Estimate from Revised Bid Set + Documents

## Project (from bid set)
- **Address:** 2001 SW 13th St, Miami, FL 33145 (Troiano Residence)
- **Scope:** Convert existing carport to enclosed garage; widen two exterior doorways in Building A; interior renovation of Building B; new landscaping and water features; 425 SF A/C area increase.
- **Buildings:** Building A (existing 3-story CMU), Building B (existing 2-story CMU – partial demo, renovation).
- **Site:** New pool, new jacuzzi, concrete walkways, driveway, planting beds, fencing.

## Documents you provided
| File | Status |
|------|--------|
| **2026.02.25-REVISED BID SET.pdf** | ✅ Used as main plan (75 pages) |
| 2025.12.18 BOUNDARY SURVEY.pdf | In DOCUMENTS folder |
| AC-4.pdf, AHRICertificate.pdf | In DOCUMENTS folder |
| BLD-01 SPECIAL INSPECTOR FORM.pdf | In DOCUMENTS folder |
| ETR-01 SOIL REPORT.pdf | In DOCUMENTS folder |
| ETR-02 ENERGY CALCS.pdf | In DOCUMENTS folder |
| ETR-03 DRAINAGE REPORT.pdf | In DOCUMENTS folder |
| ETR-04 STRUCTURAL CALCS.pdf | In DOCUMENTS folder |
| ETR-05 PERCOLATION.pdf | In DOCUMENTS folder |
| **Dropbox link** | Could not access from here (fetch failed). Download any files you need from that link and add to DOCUMENTS or run folder. |

## How to generate the estimate

1. **Set your OpenAI API key**
   ```bash
   export OPENAI_API_KEY=sk-your-key
   ```

2. **Run the pipeline**
   ```bash
   cd "/Users/bhakt/Desktop/custom gpt"
   bash run_bid_set_estimate.sh
   ```

   This will:
   - Use `estimate_from_bid_set_scope.txt` as the scope instruction
   - Use **2026.02.25-REVISED BID SET.pdf** as the plan (sent to the model with master pricing)
   - Create a new run folder under `chunked_outputs/`
   - Run comprehensive cleanup and produce `comprehensive_clean_estimate_final.xlsx` and `.csv`

3. **If you have more from Dropbox:** Save those files locally and either add them to the DOCUMENTS folder or reference them in `estimate_from_bid_set_scope.txt` and re-run.

## Files created for this estimate
- `estimate_from_bid_set_scope.txt` – Scope instruction for the estimator (bid set + supporting docs).
- `run_bid_set_estimate.sh` – Script to run the pipeline with the bid set.
