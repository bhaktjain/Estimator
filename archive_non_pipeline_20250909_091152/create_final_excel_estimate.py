#!/usr/bin/env python3
"""
Create final Excel estimate from verified and corrected CSV
"""
import sys
import os

# Add the current directory to Python path to import comprehensive_cleanup
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from comprehensive_cleanup import create_excel_file, read_csv_items

def create_final_excel():
    """Create final Excel estimate from verified CSV."""
    
    print("📊 CREATING FINAL EXCEL ESTIMATE")
    print("=" * 50)
    
    input_csv = '113_University_Place_ChatGPT_Verified_Corrected.csv'
    output_excel = '113_University_Place_Final_Verified_Estimate.xlsx'
    
    if not os.path.exists(input_csv):
        print(f"❌ Input CSV file not found: {input_csv}")
        return
    
    try:
        # Read CSV items
        print(f"📖 Reading CSV: {input_csv}")
        items = read_csv_items(input_csv)
        print(f"✅ Loaded {len(items)} items")
        
        # Create Excel file
        print(f"📝 Creating Excel: {output_excel}")
        create_excel_file(items, output_excel)
        print(f"✅ Excel file created: {output_excel}")
        
        # Show summary
        total = sum(float(item['Total']) for item in items)
        general_conditions = total * 0.10
        final_total = total + general_conditions
        
        print(f"\n📊 FINAL ESTIMATE SUMMARY:")
        print(f"Total items: {len(items)}")
        print(f"Base Cost: ${total:,.2f}")
        print(f"General Conditions (10%): ${general_conditions:,.2f}")
        print(f"Final Total: ${final_total:,.2f}")
        
        return output_excel
        
    except Exception as e:
        print(f"❌ Error creating Excel: {e}")
        return None

if __name__ == "__main__":
    excel_file = create_final_excel()
    if excel_file:
        print(f"\n🎯 Final Excel estimate ready: {excel_file}")

