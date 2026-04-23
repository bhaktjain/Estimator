#!/usr/bin/env python3
"""Generate Excel from comprehensive_clean_estimate_final.csv using pipeline (Chapter) brand."""
import os
import sys

run_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(run_dir, '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from comprehensive_cleanup import read_csv_items, create_excel_file

csv_path = os.path.join(run_dir, 'comprehensive_clean_estimate_final.csv')
excel_path = os.path.join(run_dir, 'comprehensive_clean_estimate_final.xlsx')

if __name__ == "__main__":
    if not os.path.exists(csv_path):
        print(f"[ERROR] CSV not found: {csv_path}")
        sys.exit(1)
    items = read_csv_items(csv_path)
    print(f"[INFO] Read {len(items)} line items from CSV")
    create_excel_file(items, excel_path)
    print(f"[INFO] Saved pipeline (Chapter) Excel: {excel_path}")
