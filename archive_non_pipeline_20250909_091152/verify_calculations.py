#!/usr/bin/env python3
"""
Verify calculations in the improved estimate
"""
import csv

def verify_calculations():
    """Verify all calculations in the improved estimate."""
    
    print("🔍 CROSS-CHECKING IMPROVED ESTIMATE CALCULATIONS")
    print("=" * 60)
    
    # Read the CSV file
    with open('113_University_Place_Final_Corrected_Estimate.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        items = list(reader)
    
    print(f"Total items found: {len(items)}")
    print()
    
    # Verify each calculation
    errors = []
    total_verified = 0
    
    for i, item in enumerate(items, 1):
        try:
            quantity = float(item['Quantity'])
            unit_cost = float(item['UnitCost'].replace('$', '').replace(' per SF', '').replace(' per UNIT', '').replace(' per LF', ''))
            markup = float(item['Markup'])
            expected_total = quantity * unit_cost * (1 + markup)
            actual_total = float(item['Total'])
            
            # Allow for small rounding differences
            if abs(expected_total - actual_total) > 1:
                errors.append({
                    'item': item['ItemName'],
                    'expected': expected_total,
                    'actual': actual_total,
                    'difference': expected_total - actual_total
                })
            
            total_verified += actual_total
            
        except (ValueError, KeyError) as e:
            print(f"⚠️  Error processing item {i}: {e}")
            continue
    
    # Print verification results
    if errors:
        print("❌ CALCULATION ERRORS FOUND:")
        print("-" * 40)
        for error in errors:
            print(f"Item: {error['item']}")
            print(f"  Expected: ${error['expected']:,.2f}")
            print(f"  Actual:   ${error['actual']:,.2f}")
            print(f"  Diff:     ${error['difference']:,.2f}")
            print()
    else:
        print("✅ ALL CALCULATIONS VERIFIED CORRECTLY!")
    
    print(f"Total verified amount: ${total_verified:,.2f}")
    
    # Verify category totals
    print("\n📊 VERIFYING CATEGORY TOTALS:")
    print("-" * 40)
    
    categories = {}
    for item in items:
        cat = item['Category']
        if cat not in categories:
            categories[cat] = 0
        categories[cat] += float(item['Total'])
    
    for cat, total in sorted(categories.items()):
        print(f"{cat:25} | ${total:>12,.2f}")
    
    grand_total = sum(categories.values())
    print("-" * 40)
    print(f"{'GRAND TOTAL':25} | ${grand_total:>12,.2f}")
    
    # Add 10% general conditions
    general_conditions = grand_total * 0.10
    final_total = grand_total + general_conditions
    print(f"{'General Conditions (10%)':25} | ${general_conditions:>12,.2f}")
    print(f"{'FINAL TOTAL':25} | ${final_total:>12,.2f}")
    
    # Cross-check with takeoff quantities
    print("\n🔍 CROSS-CHECKING WITH TAKEOFF:")
    print("-" * 40)
    
    # Key quantities to verify
    key_quantities = {
        'Carpet Tile Installation': {'expected': 8625, 'unit': 'SF'},
        'Engineered Wood Flooring': {'expected': 4875, 'unit': 'SF'},
        'Porcelain Tile Installation': {'expected': 225, 'unit': 'SF'},  # Pantry
        'Porcelain Tile Installation': {'expected': 825, 'unit': 'SF'},  # Restrooms
        'VCT/SDT Installation': {'expected': 300, 'unit': 'SF'},
        'Mosaic Tile Installation': {'expected': 150, 'unit': 'SF'},
        'Metal Stud Framing': {'expected': 700, 'unit': 'LF'},
        'GWB Installation': {'expected': 12600, 'unit': 'SF'},
        'ACT Ceiling System': {'expected': 8625, 'unit': 'SF'},
        'Wall Painting': {'expected': 16800, 'unit': 'SF'},
        'Solid-Core Wood Doors': {'expected': 20, 'unit': 'EA'},
        'Glass Office-Front Doors': {'expected': 24, 'unit': 'EA'},
        'Round Flushmounts': {'expected': 80, 'unit': 'EA'},
        'Recessed Downlights': {'expected': 60, 'unit': 'EA'},
        'Water Closets': {'expected': 7, 'unit': 'EA'},
        'Restroom Lavatories': {'expected': 8, 'unit': 'EA'},
        'Breccia Vino Marble Countertops': {'expected': 85, 'unit': 'SF'}
    }
    
    for item_name, expected in key_quantities.items():
        found = False
        for item in items:
            if item_name.lower() in item['ItemName'].lower():
                actual_qty = float(item['Quantity'])
                if abs(actual_qty - expected['expected']) <= 1:  # Allow for rounding
                    print(f"✅ {item_name}: {actual_qty} {expected['unit']} ✓")
                    found = True
                    break
        
        if not found:
            print(f"❌ {item_name}: NOT FOUND or quantity mismatch")
    
    return len(errors) == 0

if __name__ == "__main__":
    success = verify_calculations()
    if success:
        print("\n🎉 VERIFICATION COMPLETE - ALL CALCULATIONS CORRECT!")
    else:
        print("\n⚠️  VERIFICATION COMPLETE - ERRORS FOUND!")
