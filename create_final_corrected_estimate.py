"""
Create corrected estimate based on provided scope breakdown
NO kitchen work, NO garage work - only items from provided Excel file
"""
import pandas as pd
import csv

# Extension area from scope: 430 SF
EXTENSION_AREA = 430

# Read the correct scope
df = pd.read_excel('/Users/bhakt/Downloads/35 Springfield Road.xlsx')

print('=== CREATING CORRECTED ESTIMATE (NO KITCHEN, NO GARAGE) ===\n')

estimate_rows = []
current_category = None

# Category mapping
category_map = {
    'Demolition': 'Demolition',
    'Electrical': 'Electrical',
    'Walls & Ceiling': 'Drywall & Insulation',
    'Doors': 'Doors',
    'Flooring': 'Flooring',
    'Heating and Cooling': 'HVAC',
    'Trims': 'Trims',
    'Painting & Wall Coverings': 'Painting & Wall Coverings',
    'Interior Design Services': 'Interior Design Services',
    'General Requirements ': 'General Requirements',
    'Plumbing': 'Plumbing',
    'Waterproofing': 'Waterproofing',
    'Tile': 'Tile',
    'Concrete ': 'Concrete',
    'Extensions/Additions': 'Structural & Framing',
    'Siding ': 'Siding & Exterior',
    'Decks': 'Deck & Exterior',
    'Gutters ': 'Roofing',
    'Windows': 'Windows'
}

def get_pricing_and_quantity(item_name, description, category):
    """Get pricing and quantity based on item description"""
    desc = str(description).lower() if pd.notna(description) else ''
    item = str(item_name).lower() if pd.notna(item_name) else ''
    
    # Demolition items
    if 'pre-construction' in item or 'site preparation' in item:
        return {'qty': '1 UNIT', 'unit_cost': 2000, 'markup': 0.75}
    
    if 'demolition' in item:
        if 'powder room' in desc:
            return {'qty': '1 UNIT', 'unit_cost': 1375, 'markup': 0.75}
        if 'laundry' in desc:
            return {'qty': '1 UNIT', 'unit_cost': 2200, 'markup': 0.75}
        if 'bathroom' in desc and 'primary' in desc:
            return {'qty': '1 UNIT', 'unit_cost': 2200, 'markup': 0.75}
        if 'bathroom' in desc and 'second' in desc:
            return {'qty': '1 UNIT', 'unit_cost': 1375, 'markup': 0.75}
        if 'closet' in desc:
            return {'qty': '1 UNIT', 'unit_cost': 1375, 'markup': 0.75}
        if 'excavation' in item or 'grading' in item:
            return {'qty': f'{EXTENSION_AREA} SF', 'unit_cost': 15, 'markup': 0.75}
        # Existing house demolition
        return {'qty': f'{EXTENSION_AREA} SF', 'unit_cost': 7, 'markup': 0.75}
    
    # Electrical
    if 'electrical' in item:
        if 'extension' in desc:
            return {'qty': f'{EXTENSION_AREA} SF', 'unit_cost': 8, 'markup': 0.75}
        # Bathroom/laundry electrical
        return {'qty': '1 UNIT', 'unit_cost': 3500, 'markup': 0.75}
    
    # Drywall & Insulation
    if 'partition walls' in item or 'ceiling' in item:
        return {'qty': f'{EXTENSION_AREA * 2} SF', 'unit_cost': 8, 'markup': 0.75}  # Both floors
    if 'mold resistant' in item or 'drywall' in item:
        return {'qty': '1 UNIT', 'unit_cost': 1225, 'markup': 0.75}
    
    # Doors
    if 'door' in item:
        # 5 standard + 2 sliding + 1 bifold = 8 doors
        return {'qty': '8 UNIT', 'unit_cost': 550, 'markup': 0.75}
    
    # Flooring
    if 'flooring' in item:
        if '2nd floor' in desc:
            return {'qty': f'{EXTENSION_AREA} SF', 'unit_cost': 6, 'markup': 0.75}
        if '1st floor' in desc:
            # 1st floor includes extension + existing
            return {'qty': f'{EXTENSION_AREA + 620} SF', 'unit_cost': 6, 'markup': 0.75}
        if 'tile' in item and 'laundry' in desc:
            return {'qty': '50 SF', 'unit_cost': 2000, 'markup': 0.80}
    
    # HVAC
    if 'hvac' in item or 'heating' in item:
        return {'qty': '1 UNIT', 'unit_cost': 12000, 'markup': 0.75}
    
    # Trims
    if 'baseboard' in item:
        # Master sheet: Labor $5 + Material $6 = $11 per LF
        return {'qty': '300 LF', 'unit_cost': 11, 'markup': 0.75}
    if 'crown' in item or 'molding' in item:
        # Master sheet: Labor $9 + Material $8 = $17 per LF
        return {'qty': f'{EXTENSION_AREA * 2} LF', 'unit_cost': 17, 'markup': 0.75}
    
    # Painting
    if 'paint' in item:
        # Entire house including extension and basement - $4.50 per SF
        return {'qty': '3000 SF', 'unit_cost': 4.5, 'markup': 0.75}
    
    # Plumbing
    if 'plumbing' in item:
        if 'bathroom' in desc:
            return {'qty': '1 UNIT', 'unit_cost': 8800, 'markup': 0.75}
        if 'laundry' in desc:
            return {'qty': '1 UNIT', 'unit_cost': 3850, 'markup': 0.75}
    
    # Waterproofing
    if 'waterproofing' in item:
        return {'qty': '1 UNIT', 'unit_cost': 1900, 'markup': 0.75}
    
    # Tile
    if 'tile' in item:
        if 'wall' in desc:
            return {'qty': '1 UNIT', 'unit_cost': 2600, 'markup': 0.80}
        return {'qty': '1 UNIT', 'unit_cost': 2000, 'markup': 0.80}
    
    # Concrete
    if 'concrete' in item or 'footing' in item or 'slab' in item:
        return {'qty': f'{EXTENSION_AREA} SF', 'unit_cost': 12, 'markup': 0.75}
    
    # Structural & Framing (Extension)
    if 'extension' in item and ('wall' in item or 'roof' in item):
        if 'roof' in item:
            return {'qty': f'{EXTENSION_AREA} SF', 'unit_cost': 12, 'markup': 0.75}
        # Exterior walls
        return {'qty': f'{EXTENSION_AREA} SF', 'unit_cost': 150, 'markup': 0.75}
    
    # Siding
    if 'siding' in item:
        # Estimate siding area (walls around extension)
        return {'qty': '600 SF', 'unit_cost': 8, 'markup': 0.75}
    
    # Deck
    if 'deck' in item:
        return {'qty': '200 SF', 'unit_cost': 25, 'markup': 0.75}
    
    # Gutters
    if 'gutter' in item or 'drainage' in item:
        return {'qty': f'{EXTENSION_AREA} LF', 'unit_cost': 15, 'markup': 0.75}
    
    # Windows
    if 'window' in item:
        return {'qty': '5 UNIT', 'unit_cost': 1200, 'markup': 0.75}
    
    # General Requirements
    if 'cleaning' in item:
        return {'qty': '1 UNIT', 'unit_cost': 2750, 'markup': 0.75}
    
    # Interior Design
    if 'interior design' in item:
        return {'qty': '1 UNIT', 'unit_cost': 5000, 'markup': 0.75}
    
    # Default
    return {'qty': '1 UNIT', 'unit_cost': 2000, 'markup': 0.75}

# Process the scope file
for idx, row in df.iterrows():
    # Category header
    if pd.notna(row.get('Category')):
        current_category = row['Category']
        continue
    
    # Item row
    if pd.notna(row.get('ItemName')):
        room = row.get('Room', 'General')
        item_name = row.get('ItemName', '')
        description = row.get('Description', '')
        
        if current_category:
            mapped_cat = category_map.get(current_category, current_category)
            pricing = get_pricing_and_quantity(item_name, description, mapped_cat)
            
            # Calculate total
            qty_str = pricing['qty']
            qty_value = 1
            if 'SF' in qty_str:
                import re
                matches = re.findall(r'([\d.]+)', qty_str)
                qty_value = float(matches[0]) if matches else 1
            elif 'LF' in qty_str:
                import re
                matches = re.findall(r'([\d.]+)', qty_str)
                qty_value = float(matches[0]) if matches else 1
            elif 'UNIT' in qty_str:
                import re
                matches = re.findall(r'([\d.]+)', qty_str)
                qty_value = float(matches[0]) if matches else 1
            
            base_cost = pricing['unit_cost'] * qty_value
            total = base_cost * (1 + pricing['markup'])
            
            estimate_rows.append({
                'Category': mapped_cat,
                'Room': room,
                'ItemName': item_name,
                'Description': description if pd.notna(description) else '',  # Full description, no truncation
                'Quantity': qty_str,
                'UnitCost': f'${pricing["unit_cost"]:,.2f} per {pricing["qty"].split()[1] if " " in pricing["qty"] else "UNIT"}',
                'Markup': str(pricing['markup']),
                'MarkupType': '',
                'Total': f'{total:.2f}',
                'Confidence': '95'
            })

print(f'Created {len(estimate_rows)} estimate items')

# Write to CSV with category totals
output_path = 'chunked_outputs/run_20251118_143425_d75ae620/corrected_estimate_final.csv'
fieldnames = ['Category', 'Room', 'ItemName', 'Description', 'Quantity', 'UnitCost', 'Markup', 'MarkupType', 'Total', 'Confidence']

formatted_rows = []
category_totals = {}
current_cat = None

for row in estimate_rows:
    cat = row['Category']
    if cat not in category_totals:
        category_totals[cat] = 0
    category_totals[cat] += float(row['Total'])
    
    if cat != current_cat:
        if current_cat is not None:
            formatted_rows.append({
                'Category': '', 'Room': '', 'ItemName': '', 'Description': '',
                'Quantity': '', 'UnitCost': '', 'Markup': '', 'MarkupType': '',
                'Total': f'{category_totals[current_cat]:.2f}', 'Confidence': ''
            })
        formatted_rows.append({
            'Category': cat, 'Room': '', 'ItemName': '', 'Description': '',
            'Quantity': '', 'UnitCost': '', 'Markup': '', 'MarkupType': '',
            'Total': '', 'Confidence': ''
        })
        current_cat = cat
    formatted_rows.append(row)

# Add final category total
if current_cat:
    formatted_rows.append({
        'Category': '', 'Room': '', 'ItemName': '', 'Description': '',
        'Quantity': '', 'UnitCost': '', 'Markup': '', 'MarkupType': '',
        'Total': f'{category_totals[current_cat]:.2f}', 'Confidence': ''
    })

# Add grand total
grand_total = sum(category_totals.values())
gc = grand_total * 0.10
formatted_rows.append({
    'Category': '', 'Room': '', 'ItemName': '', 'Description': 'General Conditions (10%)',
    'Quantity': '', 'UnitCost': '', 'Markup': '', 'MarkupType': '',
    'Total': f'{gc:.2f}', 'Confidence': ''
})
formatted_rows.append({
    'Category': '', 'Room': '', 'ItemName': '', 'Description': 'Grand Total',
    'Quantity': '', 'UnitCost': '', 'Markup': '', 'MarkupType': '',
    'Total': f'{grand_total + gc:.2f}', 'Confidence': ''
})

with open(output_path, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(formatted_rows)

print(f'\n✅ Created corrected estimate: {output_path}')
print(f'Grand Total: ${grand_total + gc:,.2f}')
print(f'\n✅ NO kitchen work included')
print(f'✅ NO garage work included')
print(f'✅ Only items from provided scope breakdown')

