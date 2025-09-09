#!/usr/bin/env python3
"""
Replace estimated rates with internal rates where possible
"""
import csv

def replace_estimated_with_internal():
    """Replace estimated rates with internal rates where possible."""
    
    print("🔄 REPLACING ESTIMATED RATES WITH INTERNAL RATES")
    print("=" * 60)
    
    # Read the corrected estimate
    with open('113_University_Place_Final_Corrected_Complete.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        items = list(reader)
    
    print(f"Processing {len(items)} items")
    
    # Define internal rate replacements
    internal_replacements = {
        # Track Installation - use FRAM-04 rate for framing
        'Track Installation': {'new_rate': 55.00, 'code': 'FRAM-04', 'description': 'Frame new soffit'},
        
        # Acoustic Insulation - use insulation rate from pricing sheet
        'Acoustic Insulation': {'new_rate': 4.70, 'code': 'INSUL-01', 'description': 'Batt insulation (1.7 labor + 3.0 material)'},
        
        # Specialty Wallpaper - use wallcovering rate
        'Specialty Wallpaper Installation': {'new_rate': 12.00, 'code': 'FINSH-07', 'description': 'Wallcovering installation'},
        
        # Wallcovering - use internal rate
        'Wallcovering Installation': {'new_rate': 12.00, 'code': 'FINSH-07', 'description': 'Wallcovering installation'},
        
        # Reeded Glass Film - use glazing rate
        'Reeded Glass Film Installation': {'new_rate': 15.00, 'code': 'GLAZ-01', 'description': 'Glass film installation'},
        
        # Rubber Base - use baseboard rate
        'Rubber Base Installation': {'new_rate': 11.00, 'code': 'TRIM-01', 'description': 'Baseboards (5 labor + 6 material)'},
        
        # Wood Base/Shoe - use crown molding rate
        'Wood Base/Shoe Installation': {'new_rate': 17.00, 'code': 'TRIM-02', 'description': 'Crown molding (9 labor + 8 material)'},
        
        # Door Hardware - use hardware rate
        'Door Hardware Installation': {'new_rate': 200.00, 'code': 'HARD-01', 'description': 'Door hardware installation'},
        
        # Pull Handles - use hardware rate
        'Pull Handles Installation': {'new_rate': 200.00, 'code': 'HARD-01', 'description': 'Door hardware installation'},
        
        # Feature Chandelier - use chandelier rate
        'Feature Chandelier': {'new_rate': 165.00, 'code': 'ELEC-05', 'description': 'Light fixture installation'},
        
        # Track Lighting - use track rate
        'Track Lighting': {'new_rate': 165.00, 'code': 'ELEC-08', 'description': 'Pendant lighting'},
        
        # Linear LED Strips - use undercabinet rate
        'Linear LED Strips': {'new_rate': 110.00, 'code': 'ELEC-13', 'description': 'Undercabinet lighting per 15ft'},
        
        # Urinals - use urinal rate
        'Urinals': {'new_rate': 400.00, 'code': 'PLMB-15', 'description': 'Urinal installation'},
        
        # Restroom Faucets - use faucet rate
        'Restroom Faucets': {'new_rate': 200.00, 'code': 'PLMB-16', 'description': 'Faucet installation'},
        
        # Paper Towel Dispensers - use accessory rate
        'Paper Towel Dispensers': {'new_rate': 150.00, 'code': 'PLMB-17', 'description': 'Accessory installation'},
        
        # Toilet Roll Holders - use accessory rate
        'Toilet Roll Holders': {'new_rate': 100.00, 'code': 'PLMB-18', 'description': 'Accessory installation'},
        
        # ADA Grab Bars - use grab bar rate
        'ADA Grab Bars': {'new_rate': 200.00, 'code': 'PLMB-19', 'description': 'Grab bar installation'},
        
        # Lounge Built-ins - use cabinet rate
        'Lounge Built-ins': {'new_rate': 800.00, 'code': 'KITC-10', 'description': 'Kitchen cabinets standard'},
        
        # Arch Trim - use trim rate
        'Arch Trim': {'new_rate': 17.00, 'code': 'TRIM-02', 'description': 'Crown molding (9 labor + 8 material)'},
        
        # Antique Mirror - use mirror rate
        'Antique Mirror Installation': {'new_rate': 25.00, 'code': 'FINSH-08', 'description': 'Mirror installation'},
        
        # Metal Mesh - use mesh rate
        'Metal Mesh Installation': {'new_rate': 35.00, 'code': 'FINSH-09', 'description': 'Metal mesh installation'}
    }
    
    # Apply internal rate replacements
    replacements_made = 0
    for item in items:
        item_name = item['ItemName']
        if item_name in internal_replacements:
            old_rate = float(item['UnitCost'].replace('$', ''))
            new_rate = internal_replacements[item_name]['new_rate']
            code = internal_replacements[item_name]['code']
            description = internal_replacements[item_name]['description']
            
            # Update the item
            item['UnitCost'] = f"${new_rate:.2f}"
            
            # Recalculate total with new rate
            quantity = float(item['Quantity'])
            markup = float(item['Markup'])
            new_total = quantity * new_rate * (1 + markup)
            item['Total'] = f"{new_total:.2f}"
            
            print(f"✅ Replaced: {item_name:35} | ${old_rate:>8.2f} → ${new_rate:>8.2f} | {code}")
            replacements_made += 1
    
    print(f"\nApplied {replacements_made} internal rate replacements")
    
    # Write updated CSV
    output_filename = '113_University_Place_Internal_Pricing_Only.csv'
    with open(output_filename, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['Category', 'Room', 'ItemName', 'Description', 'Quantity', 'UnitCost', 'Markup', 'MarkupType', 'Total', 'Confidence']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(items)
    
    print(f"\n✅ Updated estimate saved to: {output_filename}")
    
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
    updated_file = replace_estimated_with_internal()
    print(f"\n🎯 Next step: Run comprehensive verification on {updated_file}")

