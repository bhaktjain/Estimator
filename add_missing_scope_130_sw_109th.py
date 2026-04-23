#!/usr/bin/env python3
"""Add transcript-verified missing scope to 130 SW 109th estimate and regenerate Excel."""
import os
import sys

run_dir = os.path.join(os.path.dirname(__file__), 'chunked_outputs', 'run_20260211_173807_fde7a68d')
csv_path = os.path.join(run_dir, 'comprehensive_clean_estimate_final.csv')
excel_path = os.path.join(run_dir, 'comprehensive_clean_estimate_final.xlsx')

# Run from project root so comprehensive_cleanup can be imported
os.chdir(os.path.dirname(__file__))
sys.path.insert(0, os.path.dirname(__file__))

from comprehensive_cleanup import read_csv_items, write_final_csv, create_excel_file

def main():
    items = read_csv_items(csv_path)
    print(f"[INFO] Read {len(items)} items from {csv_path}")

    # Remove partial flooring lines so we can add full-apartment scope (avoid double count)
    items = [i for i in items if not (
        i.get('Category') == 'Flooring' and i.get('Room') in ('Kitchen', 'Bedroom 1')
    )]
    print(f"[INFO] After removing partial flooring: {len(items)} items")

    # Add transcript-verified missing items (Chapter markups: 75% default, 80% tile)
    add = [
        {
            'Category': 'Appliances', 'Room': 'Kitchen', 'ItemName': 'Kitchen Appliances',
            'Description': 'Install new appliances and connect plumbing and electrical.',
            'Quantity': '1 UNIT', 'UnitCost': '$1,500 per UNIT', 'Markup': '0.75', 'MarkupType': '', 'Total': '2625', 'Confidence': '85',
        },
        {
            'Category': 'Tile', 'Room': 'Bathroom 2', 'ItemName': 'Bathroom Tile Work',
            'Description': 'Install floor and wall tiles (shower).',
            'Quantity': '100 SF', 'UnitCost': '$15 per SF', 'Markup': '0.80', 'MarkupType': '', 'Total': '2700', 'Confidence': '90',
        },
        {
            'Category': 'Electrical', 'Room': 'Bathroom 2', 'ItemName': 'Bathroom Electrical',
            'Description': 'Install vanity lighting, exhaust fan, and GFCI outlets.',
            'Quantity': '1 UNIT', 'UnitCost': '$800 per UNIT', 'Markup': '0.75', 'MarkupType': '', 'Total': '1400', 'Confidence': '90',
        },
        {
            'Category': 'Walls & Ceiling', 'Room': 'Entire Apartment', 'ItemName': 'Whole Apartment Drywall',
            'Description': 'Drywall walls and ceiling throughout apartment (post-fire rebuild).',
            'Quantity': '2500 SF', 'UnitCost': '$2 per SF', 'Markup': '0.75', 'MarkupType': '', 'Total': '8750', 'Confidence': '90',
        },
        {
            'Category': 'Walls & Ceiling', 'Room': 'Entire Apartment', 'ItemName': 'Insulation',
            'Description': 'Insulation throughout apartment.',
            'Quantity': '1 UNIT', 'UnitCost': '$2,000 per UNIT', 'Markup': '0.75', 'MarkupType': '', 'Total': '3500', 'Confidence': '85',
        },
        {
            'Category': 'Painting & Wall Coverings', 'Room': 'Entire Apartment', 'ItemName': 'Whole Apartment Painting',
            'Description': 'Paint walls and ceiling throughout.',
            'Quantity': '1 UNIT', 'UnitCost': '$2,000 per UNIT', 'Markup': '0.75', 'MarkupType': '', 'Total': '3500', 'Confidence': '90',
        },
        {
            'Category': 'Flooring', 'Room': 'Entire Apartment', 'ItemName': 'Laminate Flooring (full apartment)',
            'Description': 'Install laminate flooring throughout 2,500 SF.',
            'Quantity': '2500 SF', 'UnitCost': '$5 per SF', 'Markup': '0.75', 'MarkupType': '', 'Total': '21875', 'Confidence': '90',
        },
        {
            'Category': 'Flooring', 'Room': 'Stairs', 'ItemName': 'Stairs Laminate',
            'Description': 'Laminate on staircase (same as floor).',
            'Quantity': '50 SF', 'UnitCost': '$5 per SF', 'Markup': '0.75', 'MarkupType': '', 'Total': '437.5', 'Confidence': '85',
        },
        {
            'Category': 'Painting & Wall Coverings', 'Room': 'Stairs', 'ItemName': 'Staircase Paint',
            'Description': 'Paint staircase (struts in good condition).',
            'Quantity': '1 UNIT', 'UnitCost': '$500 per UNIT', 'Markup': '0.75', 'MarkupType': '', 'Total': '875', 'Confidence': '90',
        },
        {
            'Category': 'General Requirements', 'Room': 'Entire Apartment', 'ItemName': 'Window Glass Replacement',
            'Description': 'Replace broken window glass only (same framing; no full window replacement).',
            'Quantity': '2 UNIT', 'UnitCost': '$400 per UNIT', 'Markup': '0.75', 'MarkupType': '', 'Total': '1400', 'Confidence': '90',
        },
    ]

    for it in add:
        items.append(it)
    print(f"[INFO] Added {len(add)} transcript-verified items. Total items: {len(items)}")

    write_final_csv(items, csv_path)
    print(f"[INFO] Wrote {csv_path}")
    create_excel_file(items, excel_path)
    print(f"[INFO] Wrote {excel_path}")
    print("[DONE] Revised estimate includes both Polycam files and transcript-verified scope.")

if __name__ == '__main__':
    main()
