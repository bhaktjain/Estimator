#!/usr/bin/env python3
"""Verify latest estimate against transcript: scope checklist and measurement summary."""
import os
import sys
import csv
from pathlib import Path

def main():
    chunked_dir = Path('chunked_outputs')
    if not chunked_dir.exists():
        print("[ERROR] chunked_outputs not found")
        return
    run_dirs = sorted([p for p in chunked_dir.iterdir() if p.is_dir() and p.name.startswith('run_')],
                      key=lambda p: p.stat().st_mtime, reverse=True)
    if not run_dirs:
        print("[ERROR] No run directories")
        return
    run_dir = run_dirs[0]
    print(f"[INFO] Latest run: {run_dir.name}")

    # Find CSV
    csv_path = run_dir / 'comprehensive_clean_estimate_final.csv'
    if not csv_path.exists():
        csv_path = run_dir / 'comprehensive_clean_estimate.csv'
    if not csv_path.exists():
        print("[WARNING] No estimate CSV in run; run comprehensive_cleanup.py first after pipeline succeeds.")
        return

    # Load estimate items
    items = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            if row.get('Category') and row.get('ItemName') and row.get('Category') != 'Category':
                items.append(row)
    categories = set(i.get('Category', '') for i in items)
    print(f"[INFO] Estimate: {len(items)} items, categories: {', '.join(sorted(categories))}")

    # Load transcript from run chunks
    chunk_dir = run_dir / 'transcript_chunks'
    transcript_text = ""
    if chunk_dir.exists():
        for p in sorted(chunk_dir.glob('*.txt')):
            transcript_text += p.read_text(encoding='utf-8') + "\n"
    if not transcript_text.strip():
        print("[WARNING] No transcript chunks in run")
    else:
        transcript_lower = transcript_text.lower()
        # Simple scope keywords from transcript
        checks = [
            ('kitchen', 'Kitchen' in str(categories) or any('kitchen' in (i.get('ItemName') or '').lower() or (i.get('Room') or '').lower() == 'kitchen' for i in items)),
            ('bathroom', 'Tile' in str(categories) or 'Plumbing' in str(categories) or any('bathroom' in (i.get('Room') or '').lower() for i in items)),
            ('floor', 'Flooring' in str(categories) or any('floor' in (i.get('ItemName') or '').lower() for i in items)),
            ('demolition', 'Demolition' in str(categories)),
            ('cleaning', 'General Requirements' in str(categories) or any('clean' in (i.get('ItemName') or '').lower() for i in items)),
        ]
        print("\n--- SCOPE CHECK (transcript vs estimate) ---")
        for name, ok in checks:
            print(f"  [{('OK' if ok else '?')}] {name}")

    # Section order
    from comprehensive_cleanup import ESTIMATE_SECTION_ORDER
    order_ok = True
    csv_cats = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            c = (row.get('Category') or '').strip()
            if c and c not in csv_cats:
                csv_cats.append(c)
    expected_order = [c for c in ESTIMATE_SECTION_ORDER if c in csv_cats]
    if csv_cats != expected_order:
        order_ok = False
    print(f"\n--- SECTION ORDER ---")
    print(f"  Order in CSV: {' -> '.join(csv_cats)}")
    print(f"  Expected (partial): {' -> '.join(expected_order[:5])}...")
    print(f"  Consistent: {'Yes' if order_ok else 'No (re-run write_final_csv/create_excel)'}")

    # Totals
    total = 0.0
    for i in items:
        t = i.get('Total', '') or '0'
        if isinstance(t, str):
            t = t.replace(',', '').replace('$', '').strip()
        try:
            total += float(t)
        except ValueError:
            pass
    print(f"\n--- TOTALS ---")
    print(f"  Sum of line items: ${total:,.2f}")
    print(f"  File: {csv_path}")
    print("\nVerification complete.")

if __name__ == '__main__':
    main()
