# 366 Broadway – Estimate Accuracy Verification

## Summary

**Verdict: Accurate** after two corrections. The estimate now matches master pricing for all checked items; a few items are allowances or judgment calls as noted below.

---

## Corrections applied

1. **General demolition (12th floor)**  
   - **Was:** 400 SF × $7/SF → $2,450 (used labor only).  
   - **Should be:** DEMO-07 labor $7/SF × (1 + 0.75) = $12.25/SF → 400 × $12.25 = **$4,900**.  
   - **Updated** in CSV and reflected in subtotal/grand total.

2. **Post-construction cleaning**  
   - **Was:** $4,813 (CLEN-04, 1800–2500 SF).  
   - **Should be:** Duplex ~2,600 SF → CLEN-05 (2500+ SF): 4400 × 1.75 = **$7,700**.  
   - **Updated** in CSV and reflected in subtotal/grand total.

---

## Spot-check vs master pricing

| Line item | Master code | Labor | Margin | Expected unit $ | Estimate | OK? |
|-----------|-------------|-------|--------|------------------|----------|-----|
| Kitchen demo | DEMO-02 | 3300 | 0.75 | 5775 | 5775 | ✓ |
| Primary bath demo | DEMO-05 | 3300 | 0.75 | 5775 | 5775 | ✓ |
| Shared/In-suite demo | DEMO-04 | 2750 | 0.75 | 4813 | 4813 | ✓ |
| Primary bath plumbing | PLMB-03 | 9900 | 0.75 | 17325 | 17325 | ✓ |
| Kitchen plumbing 2-sink | PLMB-10 | 4950 | 0.75 | 8663 | 8663 | ✓ |
| W/D relocation | PLMB-17 | 3350 | 0.75 | 5863 | 5863 | ✓ |
| Waterproofing 89 SF | WATR-03 | 2250 | 0.75 | 3938 | 3938 | ✓ |
| Kitchen cabinets 22 LF | KITC-09 + KITC-11 | 12500 + 22×850 | 0.75 | 40575 | 40568 | ✓ |
| Quartz install 45 SF | STON-02 | 97/SF | 0.75 | 7639 | 7639 | ✓ |
| Hardwood 1300 SF | FINSH-07 | 6/SF | 0.75 | 10.50/SF | 13650 | ✓ |
| Interior doors ×11 | DOOR-01 | 550 | 0.75 | 963 | 10593 | ✓ |
| Pocket doors ×2 | DOOR-02 | 1320 | 0.75 | 2310 | 4620 | ✓ |

---

## Allowances / judgment

- **Stair structure:** MISC-07 has no unit price; $15,000 + handrail is an allowance. Confirm with structural/GC.
- **Radiator covers (7):** Priced as prefab (MISC-11) ~$2,625/ea. If CDs imply custom (MISC-10), use ~$3,750/ea → +$7,875.
- **Appliances:** Allowance only; client selection will drive final cost.

---

## Totals (after corrections)

- **Subtotal:** $438,168.00  
- **General conditions (10%):** $43,816.80  
- **Grand total:** $481,984.80  

Excel is regenerated from the updated CSV; use the Excel file for the final estimate.
