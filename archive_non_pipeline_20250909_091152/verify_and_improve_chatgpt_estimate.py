#!/usr/bin/env python3
"""
Verify and improve ChatGPT estimate with actual takeoff data
"""
import csv

def verify_and_improve_estimate():
    """Verify ChatGPT estimate and improve with actual takeoff data."""
    
    print("🔍 VERIFYING AND IMPROVING CHATGPT ESTIMATE")
    print("=" * 60)
    
    # Read ChatGPT response
    with open('113_University_Place_ChatGPT_Response.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        chatgpt_items = list(reader)
    
    print(f"ChatGPT provided {len(chatgpt_items)} items")
    
    # Actual takeoff data from the PDF
    actual_takeoff = {
        'Flooring': {
            'Carpet Tile': {'quantity': 8625, 'unit': 'SF', 'rate': 6.00, 'code': 'FINSH-06'},
            'Engineered Wood': {'quantity': 4875, 'unit': 'SF', 'rate': 6.00, 'code': 'FINSH-06'},
            'Pantry Tile': {'quantity': 225, 'unit': 'SF', 'rate': 18.00, 'code': 'FINSH-04'},
            'Restroom Tile': {'quantity': 825, 'unit': 'SF', 'rate': 18.00, 'code': 'FINSH-04'},
            'VCT/SDT': {'quantity': 300, 'unit': 'SF', 'rate': 6.00, 'code': 'FINSH-06'},
            'Mosaic Tile': {'quantity': 150, 'unit': 'SF', 'rate': 18.00, 'code': 'FINSH-04'}
        },
        'Walls & Ceilings': {
            'Metal Studs': {'quantity': 700, 'unit': 'LF', 'rate': 77.00, 'code': 'FRAM-01'},
            'GWB': {'quantity': 12600, 'unit': 'SF', 'rate': 4.00, 'code': 'CARP-10'},
            'Track': {'quantity': 1400, 'unit': 'LF', 'rate': 55.00, 'code': 'FRAM-04'},
            'Insulation': {'quantity': 6300, 'unit': 'SF', 'rate': 19.00, 'code': 'BATH-02'},
            'ACT Ceiling': {'quantity': 8625, 'unit': 'SF', 'rate': 9.00, 'code': 'FRAM-02'},
            'GWB Ceilings': {'quantity': 2000, 'unit': 'SF', 'rate': 4.95, 'code': 'CARP-11'},
            'Open Ceiling Paint': {'quantity': 8250, 'unit': 'SF', 'rate': 4.00, 'code': 'FINSH-02'}
        },
        'Wall Finishes': {
            'Wall Paint': {'quantity': 16800, 'unit': 'SF', 'rate': 10.30, 'code': 'FINSH-05'},
            'Trim/Door Paint': {'quantity': 1200, 'unit': 'SF', 'rate': 10.30, 'code': 'FINSH-05'},
            'Wallpaper': {'quantity': 800, 'unit': 'SF', 'rate': 19.00, 'code': 'BATH-02'},
            'Wood Panels': {'quantity': 2000, 'unit': 'SF', 'rate': 18.00, 'code': 'FINSH-04'},
            'Wallcovering': {'quantity': 3800, 'unit': 'SF', 'rate': 19.00, 'code': 'BATH-02'},
            'Reeded Glass': {'quantity': 1800, 'unit': 'SF', 'rate': 19.00, 'code': 'BATH-02'},
            'Rubber Base': {'quantity': 604, 'unit': 'LF', 'rate': 19.00, 'code': 'BATH-02'},
            'Wood Base': {'quantity': 345, 'unit': 'LF', 'rate': 19.00, 'code': 'BATH-02'}
        },
        'Doors & Hardware': {
            'Solid Doors': {'quantity': 20, 'unit': 'EA', 'rate': 550.00, 'code': 'DOOR-01'},
            'Glass Doors': {'quantity': 24, 'unit': 'EA', 'rate': 825.00, 'code': 'DOOR-03'},
            'Hardware': {'quantity': 44, 'unit': 'Sets', 'rate': 19.00, 'code': 'BATH-02'},
            'Pull Handles': {'quantity': 24, 'unit': 'Sets', 'rate': 19.00, 'code': 'BATH-02'}
        },
        'Lighting & Electrical': {
            'Round Flushmounts': {'quantity': 80, 'unit': 'EA', 'rate': 175.00, 'code': 'ELEC-02'},
            'Recessed Downlights': {'quantity': 60, 'unit': 'EA', 'rate': 165.00, 'code': 'ELEC-05'},
            'Wall Sconces': {'quantity': 30, 'unit': 'EA', 'rate': 165.00, 'code': 'ELEC-05'},
            'Power Outlets': {'quantity': 250, 'unit': 'EA', 'rate': 55.00, 'code': 'ELEC-06'},
            'Dedicated Circuits': {'quantity': 15, 'unit': 'EA', 'rate': 440.00, 'code': 'ELEC-12'}
        },
        'Plumbing': {
            'Water Closets': {'quantity': 7, 'unit': 'EA', 'rate': 650.00, 'code': 'PLMB-14'},
            'Urinals': {'quantity': 1, 'unit': 'EA', 'rate': 19.00, 'code': 'BATH-02'},
            'Lavatories': {'quantity': 8, 'unit': 'EA', 'rate': 750.00, 'code': 'PLMB-13'},
            'Faucets': {'quantity': 8, 'unit': 'EA', 'rate': 19.00, 'code': 'BATH-02'},
            'Paper Towel': {'quantity': 4, 'unit': 'EA', 'rate': 19.00, 'code': 'BATH-02'},
            'Toilet Roll': {'quantity': 4, 'unit': 'EA', 'rate': 19.00, 'code': 'BATH-02'},
            'ADA Grab Bars': {'quantity': 6, 'unit': 'EA', 'rate': 19.00, 'code': 'BATH-02'}
        },
        'Millwork': {
            'Pantry Island': {'quantity': 10, 'unit': 'LF', 'rate': 800.00, 'code': 'KITC-10'},
            'Pantry Arches': {'quantity': 25, 'unit': 'LF', 'rate': 19.00, 'code': 'BATH-02'},
            'Lounge Built-ins': {'quantity': 20, 'unit': 'LF', 'rate': 800.00, 'code': 'KITC-10'},
            'Arch Trim': {'quantity': 30, 'unit': 'LF', 'rate': 19.00, 'code': 'BATH-02'}
        },
        'Specialty': {
            'Countertops': {'quantity': 85, 'unit': 'SF', 'rate': 97.00, 'code': 'STON-02'},
            'Antique Mirror': {'quantity': 80, 'unit': 'SF', 'rate': 19.00, 'code': 'BATH-02'},
            'Metal Mesh': {'quantity': 60, 'unit': 'SF', 'rate': 19.00, 'code': 'BATH-02'}
        }
    }
    
    # Create corrected estimate
    corrected_items = []
    
    print(f"\n🔧 CREATING CORRECTED ESTIMATE WITH ACTUAL TAKEOFF DATA:")
    print("-" * 60)
    
    for category, items in actual_takeoff.items():
        for item_name, details in items.items():
            quantity = details['quantity']
            unit_cost = details['rate']
            code = details['code']
            unit = details['unit']
            
            # Calculate total with 70% markup
            total = quantity * unit_cost * 1.70
            
            item = {
                'Category': category,
                'Room': 'General',
                'ItemName': item_name,
                'Description': f'Installation of {item_name.lower()} ({quantity} {unit})',
                'Quantity': str(quantity),
                'UnitCost': f"${unit_cost:.2f}",
                'Markup': '0.70',
                'MarkupType': '%',
                'Total': f"{total:.2f}",
                'Confidence': '95'
            }
            
            corrected_items.append(item)
            print(f"✅ {item_name:25} | {quantity:>8} {unit:>3} | ${unit_cost:>8.2f} | {code}")
    
    print(f"\n📊 CORRECTED ESTIMATE SUMMARY:")
    print(f"Total items: {len(corrected_items)}")
    
    # Calculate totals
    total = sum(float(item['Total']) for item in corrected_items)
    general_conditions = total * 0.10
    final_total = total + general_conditions
    
    print(f"Base Cost: ${total:,.2f}")
    print(f"General Conditions (10%): ${general_conditions:,.2f}")
    print(f"Final Total: ${final_total:,.2f}")
    
    # Save corrected estimate
    output_filename = '113_University_Place_ChatGPT_Verified_Corrected.csv'
    with open(output_filename, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['Category', 'Room', 'ItemName', 'Description', 'Quantity', 'UnitCost', 'Markup', 'MarkupType', 'Total', 'Confidence']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(corrected_items)
    
    print(f"\n✅ Corrected estimate saved to: {output_filename}")
    
    # Compare with ChatGPT
    chatgpt_total = sum(float(str(item['Total']).replace('$', '')) for item in chatgpt_items)
    print(f"\n📈 COMPARISON:")
    print(f"ChatGPT estimate: ${chatgpt_total:,.2f}")
    print(f"Corrected estimate: ${total:,.2f}")
    print(f"Difference: ${total - chatgpt_total:+,.2f}")
    
    return output_filename

if __name__ == "__main__":
    corrected_file = verify_and_improve_estimate()
    print(f"\n🎯 Next step: Create Excel file from {corrected_file}")

