#!/usr/bin/env python3
"""
Fix calculation errors and ensure all items are properly included
"""
import csv

def fix_estimate():
    """Fix the improved estimate by correcting calculations and ensuring completeness."""
    
    print("🔧 FIXING IMPROVED ESTIMATE...")
    print("=" * 50)
    
    # Read the current CSV
    with open('113_University_Place_Improved_Estimate.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        items = list(reader)
    
    print(f"Found {len(items)} items to fix")
    
    # Fix calculation errors
    fixes_made = 0
    
    for item in items:
        try:
            quantity = float(item['Quantity'])
            unit_cost_str = item['UnitCost']
            unit_cost = float(unit_cost_str.replace('$', '').replace(' per SF', '').replace(' per UNIT', '').replace(' per LF', ''))
            markup = float(item['Markup'])
            
            # Calculate correct total
            correct_total = quantity * unit_cost * (1 + markup)
            current_total = float(item['Total'])
            
            # If difference is more than $1, fix it
            if abs(correct_total - current_total) > 1:
                old_total = item['Total']
                item['Total'] = f"{correct_total:.2f}"
                print(f"Fixed: {item['ItemName']}")
                print(f"  Old: ${old_total} → New: ${item['Total']}")
                print(f"  Calc: {quantity} × ${unit_cost:.2f} × {1 + markup:.2f} = ${correct_total:.2f}")
                print()
                fixes_made += 1
                
        except (ValueError, KeyError) as e:
            print(f"⚠️  Error processing item: {e}")
            continue
    
    print(f"Fixed {fixes_made} calculation errors")
    
    # Ensure all key items from takeoff are included
    print("\n🔍 CHECKING FOR MISSING ITEMS...")
    
    # Key items that should be present
    required_items = {
        'Carpet Tile': {'quantity': 8625, 'unit': 'SF', 'category': 'Flooring'},
        'Engineered Wood': {'quantity': 4875, 'unit': 'SF', 'category': 'Flooring'},
        'Pantry Tile': {'quantity': 225, 'unit': 'SF', 'category': 'Flooring'},
        'Restroom Tile': {'quantity': 825, 'unit': 'SF', 'category': 'Flooring'},
        'VCT/SDT': {'quantity': 300, 'unit': 'SF', 'category': 'Flooring'},
        'Mosaic Tile': {'quantity': 150, 'unit': 'SF', 'category': 'Flooring'},
        'Metal Studs': {'quantity': 700, 'unit': 'LF', 'category': 'Walls & Ceilings'},
        'GWB': {'quantity': 12600, 'unit': 'SF', 'category': 'Walls & Ceilings'},
        'ACT Ceiling': {'quantity': 8625, 'unit': 'SF', 'category': 'Walls & Ceilings'},
        'Wall Paint': {'quantity': 16800, 'unit': 'SF', 'category': 'Wall Finishes'},
        'Solid Doors': {'quantity': 20, 'unit': 'EA', 'category': 'Doors & Hardware'},
        'Glass Doors': {'quantity': 24, 'unit': 'EA', 'category': 'Doors & Hardware'},
        'Round Flushmounts': {'quantity': 80, 'unit': 'EA', 'category': 'Lighting & Electrical'},
        'Recessed Downlights': {'quantity': 60, 'unit': 'EA', 'category': 'Lighting & Electrical'},
        'Water Closets': {'quantity': 7, 'unit': 'EA', 'category': 'Plumbing Fixtures'},
        'Lavatories': {'quantity': 8, 'unit': 'EA', 'category': 'Plumbing Fixtures'},
        'Countertops': {'quantity': 85, 'unit': 'SF', 'category': 'Countertops'}
    }
    
    # Check which items are present
    found_items = set()
    for item in items:
        item_name_lower = item['ItemName'].lower()
        for required_name in required_items.keys():
            if required_name.lower() in item_name_lower:
                found_items.add(required_name)
                break
    
    missing_items = set(required_items.keys()) - found_items
    if missing_items:
        print(f"❌ Missing items: {missing_items}")
    else:
        print("✅ All required items found!")
    
    # Write corrected CSV
    output_filename = '113_University_Place_Corrected_Estimate.csv'
    with open(output_filename, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['Category', 'Room', 'ItemName', 'Description', 'Quantity', 'UnitCost', 'Markup', 'MarkupType', 'Total', 'Confidence']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(items)
    
    print(f"\n✅ Corrected estimate saved to: {output_filename}")
    
    # Calculate final totals
    total = sum(float(item['Total']) for item in items)
    general_conditions = total * 0.10
    final_total = total + general_conditions
    
    print(f"\n📊 FINAL TOTALS:")
    print(f"Base Cost: ${total:,.2f}")
    print(f"General Conditions (10%): ${general_conditions:,.2f}")
    print(f"Final Total: ${final_total:,.2f}")
    
    return output_filename

if __name__ == "__main__":
    fixed_file = fix_estimate()
    print(f"\n🎯 Next step: Run create_excel_estimate.py with {fixed_file}")

