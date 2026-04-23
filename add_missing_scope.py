#!/usr/bin/env python3
"""
Add missing scope items to the final estimate CSV
"""

import pandas as pd
import os

def add_missing_scope_items():
    # Read the current final CSV
    csv_path = "chunked_outputs/run_20250922_235037_9d1c32e1/comprehensive_clean_estimate_final.csv"
    df = pd.read_csv(csv_path)
    
    # Remove the grand total rows (last 3 rows)
    df = df[:-3]
    
    # Missing items to add
    missing_items = [
        {
            "Category": "Walls & Ceiling",
            "Room": "Bedroom 1", 
            "ItemName": "Install dropped ceiling",
            "Description": "Install new dropped ceiling in Bedroom 1.",
            "Quantity": "189.5 SF",
            "UnitCost": "$9 per SF",
            "Markup": "0.75",
            "MarkupType": "",
            "Total": "2987.625",
            "Confidence": "90"
        },
        {
            "Category": "Walls & Ceiling",
            "Room": "Bedroom 2",
            "ItemName": "Install dropped ceiling", 
            "Description": "Install new dropped ceiling in Bedroom 2.",
            "Quantity": "110.6 SF",
            "UnitCost": "$9 per SF",
            "Markup": "0.75",
            "MarkupType": "",
            "Total": "1743.45",
            "Confidence": "90"
        },
        {
            "Category": "Electrical",
            "Room": "Bedroom 1",
            "ItemName": "Recessed lighting installation",
            "Description": "Install 4 recessed lights in Bedroom 1.",
            "Quantity": "4 UNIT",
            "UnitCost": "$440 per UNIT", 
            "Markup": "0.75",
            "MarkupType": "",
            "Total": "3080",
            "Confidence": "95"
        },
        {
            "Category": "Electrical",
            "Room": "Bedroom 2",
            "ItemName": "Recessed lighting installation",
            "Description": "Install 4 recessed lights in Bedroom 2.",
            "Quantity": "4 UNIT",
            "UnitCost": "$440 per UNIT",
            "Markup": "0.75", 
            "MarkupType": "",
            "Total": "3080",
            "Confidence": "95"
        },
        {
            "Category": "Electrical",
            "Room": "Bedroom 2",
            "ItemName": "Pendant lighting installation",
            "Description": "Install 1 pendant light in Bedroom 2.",
            "Quantity": "1 UNIT",
            "UnitCost": "$440 per UNIT",
            "Markup": "0.75",
            "MarkupType": "",
            "Total": "770",
            "Confidence": "95"
        }
    ]
    
    # Add missing items
    for item in missing_items:
        new_row = pd.DataFrame([item])
        df = pd.concat([df, new_row], ignore_index=True)
    
    # Recalculate category totals
    category_totals = {}
    for category in df['Category'].unique():
        if pd.notna(category) and category != '':
            category_df = df[df['Category'] == category]
            total = category_df['Total'].astype(float).sum()
            category_totals[category] = total
    
    # Add category total rows
    rows_to_add = []
    for category, total in category_totals.items():
        total_row = {
            "Category": "",
            "Room": "",
            "ItemName": "",
            "Description": "",
            "Quantity": "",
            "UnitCost": "",
            "Markup": "",
            "MarkupType": "",
            "Total": f"{total:.2f}",
            "Confidence": ""
        }
        rows_to_add.append(total_row)
    
    # Add category totals
    for row in rows_to_add:
        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    
    # Calculate grand total
    grand_total = sum(category_totals.values())
    general_conditions = grand_total * 0.10
    final_total = grand_total + general_conditions
    
    # Add grand total rows
    grand_total_rows = [
        {
            "Category": "",
            "Room": "",
            "ItemName": "",
            "Description": "",
            "Quantity": "",
            "UnitCost": "",
            "Markup": "",
            "MarkupType": "",
            "Total": f"{grand_total:.2f}",
            "Confidence": ""
        },
        {
            "Category": "",
            "Room": "",
            "ItemName": "",
            "Description": "General Conditions (10%)",
            "Quantity": "",
            "UnitCost": "",
            "Markup": "",
            "MarkupType": "",
            "Total": f"{general_conditions:.2f}",
            "Confidence": ""
        },
        {
            "Category": "",
            "Room": "",
            "ItemName": "",
            "Description": "Grand Total",
            "Quantity": "",
            "UnitCost": "",
            "Markup": "",
            "MarkupType": "",
            "Total": f"{final_total:.2f}",
            "Confidence": ""
        }
    ]
    
    for row in grand_total_rows:
        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    
    # Write updated CSV
    df.to_csv(csv_path, index=False)
    print(f"✅ Added missing scope items to {csv_path}")
    print(f"📊 Updated grand total: ${final_total:,.2f}")
    
    return df

if __name__ == "__main__":
    add_missing_scope_items()





