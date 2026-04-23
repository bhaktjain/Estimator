#!/usr/bin/env python3
"""Create properly formatted Excel for 366 Broadway using comprehensive_cleanup format."""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from comprehensive_cleanup import read_csv_items, create_excel_file

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, 'estimate_366_broadway_UPDATED.csv')
    excel_path = os.path.join(base_dir, '366_Broadway_Gambhir_Estimate_Final_UPDATED.xlsx')
    
    print(f"Reading CSV: {csv_path}")
    items = read_csv_items(csv_path)
    print(f"Found {len(items)} items")
    
    print(f"Creating Excel: {excel_path}")
    create_excel_file(items, excel_path)
    print("Done!")
