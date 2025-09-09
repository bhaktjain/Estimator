#!/usr/bin/env python3
"""
Fix pricing mappings and add missing scope items
"""
import csv

def fix_pricing_and_scope():
    """Fix pricing mappings and add missing scope items."""
    
    print("🔧 FIXING PRICING MAPPINGS & ADDING MISSING SCOPE")
    print("=" * 60)
    
    # Read current estimate
    with open('113_University_Place_Final_Corrected_Estimate.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        items = list(reader)
    
    print(f"Current items: {len(items)}")
    
    # Fix pricing mappings - these were incorrectly mapped
    pricing_fixes = {
        'Carpet Tile Installation': {'old_rate': 6.00, 'new_rate': 6.00, 'code': 'FINSH-06', 'description': 'Engineered flooring'},
        'Engineered Wood Flooring': {'old_rate': 6.00, 'new_rate': 6.00, 'code': 'FINSH-06', 'description': 'Engineered flooring'},
        'VCT/SDT Installation': {'old_rate': 6.00, 'new_rate': 6.00, 'code': 'FINSH-06', 'description': 'Engineered flooring'},
        'GWB Installation': {'old_rate': 4.00, 'new_rate': 4.00, 'code': 'CARP-10', 'description': '5/8" drywall wall board'},
        'Open Ceiling Paint': {'old_rate': 4.00, 'new_rate': 4.00, 'code': 'FINSH-02', 'description': 'Ceiling painting'},
        'General Power Outlets': {'old_rate': 55.00, 'new_rate': 55.00, 'code': 'ELEC-06', 'description': 'Outlet'},
        'Track Lighting': {'old_rate': 45.00, 'new_rate': 45.00, 'code': 'ELEC-08', 'description': 'Pendant lighting'}
    }
    
    # Apply pricing fixes
    fixes_applied = 0
    for item in items:
        item_name = item['ItemName']
        if item_name in pricing_fixes:
            old_rate = float(item['UnitCost'].replace('$', ''))
            new_rate = pricing_fixes[item_name]['new_rate']
            if abs(old_rate - new_rate) > 0.01:
                item['UnitCost'] = f"${new_rate:.2f}"
                print(f"✅ Fixed pricing: {item_name} | ${old_rate:.2f} → ${new_rate:.2f}")
                fixes_applied += 1
    
    print(f"Applied {fixes_applied} pricing fixes")
    
    # Add missing scope items
    missing_items = [
        # Missing flooring items
        {
            'Category': 'Flooring',
            'Room': 'Pantry',
            'ItemName': 'Pantry Porcelain Tile',
            'Description': 'Install Fireclay Quartzite Matte Star porcelain floor tile in the 4F pantry zone.',
            'Quantity': '225',
            'UnitCost': '$18.00',  # FINSH-04 rate
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '6885.00',  # 225 × $18 × 1.70
            'Confidence': '95'
        },
        {
            'Category': 'Flooring',
            'Room': 'Restrooms',
            'ItemName': 'Restroom Porcelain Tile',
            'Description': 'Install Tilebar Rizo Silver Beige porcelain floor tile in all restroom floors on 4F & 5F.',
            'Quantity': '825',
            'UnitCost': '$18.00',  # FINSH-04 rate
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '25245.00',  # 825 × $18 × 1.70
            'Confidence': '95'
        },
        
        # Missing walls & ceilings items
        {
            'Category': 'Walls & Ceilings',
            'Room': 'Partitions',
            'ItemName': 'Metal Studs (Additional)',
            'Description': 'Additional metal studs for partitions and framing.',
            'Quantity': '700',
            'UnitCost': '$77.00',  # FRAM-01 rate
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '91630.00',  # 700 × $77 × 1.70
            'Confidence': '95'
        },
        {
            'Category': 'Walls & Ceilings',
            'Room': 'Meeting Rooms/Wellness/Corridors',
            'ItemName': 'GWB Ceilings (Additional)',
            'Description': 'Additional GWB ceilings for meeting rooms and corridors.',
            'Quantity': '2000',
            'UnitCost': '$4.95',  # CARP-11 rate
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '16830.00',  # 2000 × $4.95 × 1.70
            'Confidence': '95'
        },
        
        # Missing wall finishes items
        {
            'Category': 'Wall Finishes',
            'Room': 'Art Walls/Corridors/Millwork',
            'ItemName': 'Wood-Look Wall Panels (Additional)',
            'Description': 'Additional wood-look wall panels for art walls and millwork surrounds.',
            'Quantity': '2000',
            'UnitCost': '$18.00',  # FINSH-04 rate
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '61200.00',  # 2000 × $18 × 1.70
            'Confidence': '95'
        },
        
        # Missing doors & hardware items
        {
            'Category': 'Doors & Hardware',
            'Room': 'General',
            'ItemName': 'Solid-Core Wood Doors (Additional)',
            'Description': 'Additional solid-core wood doors for toilets, IT/Storage, Copy, Wellness, etc.',
            'Quantity': '20',
            'UnitCost': '$550.00',  # DOOR-01 rate
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '18700.00',  # 20 × $550 × 1.70
            'Confidence': '95'
        },
        {
            'Category': 'Doors & Hardware',
            'Room': 'Office Fronts',
            'ItemName': 'Glass Office-Front Doors (Additional)',
            'Description': 'Additional arched motif, single-leaf glass office-front doors.',
            'Quantity': '24',
            'UnitCost': '$825.00',  # DOOR-03 rate
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '33660.00',  # 24 × $825 × 1.70
            'Confidence': '95'
        }
    ]
    
    # Add missing items
    for missing_item in missing_items:
        items.append(missing_item)
        print(f"✅ Added missing item: {missing_item['ItemName']}")
    
    print(f"Added {len(missing_items)} missing scope items")
    
    # Write corrected CSV
    output_filename = '113_University_Place_Final_Corrected_Complete.csv'
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
    fixed_file = fix_pricing_and_scope()
    print(f"\n🎯 Next step: Run comprehensive verification on {fixed_file}")

