#!/usr/bin/env python3
import csv
import sys
import os

# Add the current directory to Python path to import comprehensive_cleanup functions
sys.path.append('.')

from comprehensive_cleanup import create_excel_file, read_csv_items

def main():
    """Create Excel file directly from our estimate CSV."""
    
    csv_file = '113_University_Place_Maximum_Internal_Pricing.csv'
    
    if not os.path.exists(csv_file):
        print(f"Error: {csv_file} not found!")
        return
    
    # Read the CSV items
    print(f"Reading items from {csv_file}...")
    items = read_csv_items(csv_file)
    print(f"Found {len(items)} items")
    
    # Create the Excel file
    output_excel = '113_University_Place_Maximum_Internal_Pricing.xlsx'
    print(f"Creating Excel file: {output_excel}")
    
    try:
        create_excel_file(items, output_excel)
        print(f"✅ Successfully created: {output_excel}")
        
        # Calculate total
        total = sum(float(item.get('Total', '0').replace('$', '').replace(',', '')) for item in items)
        print(f"💰 Total Estimated Cost: ${total:,.2f}")
        
    except Exception as e:
        print(f"❌ Error creating Excel file: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
