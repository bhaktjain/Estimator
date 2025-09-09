#!/usr/bin/env python3
"""
Final comprehensive verification of the verified and corrected estimate
"""
import csv

def final_comprehensive_verification():
    """Final verification of internal pricing and scope coverage."""
    
    print("🔍 FINAL COMPREHENSIVE VERIFICATION")
    print("=" * 60)
    
    # Read the verified estimate
    with open('113_University_Place_ChatGPT_Verified_Corrected.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        items = list(reader)
    
    print(f"📊 Total items in estimate: {len(items)}")
    
    # Define internal pricing rates from master sheet
    internal_rates = {
        # Demolition
        'DEMO-12': {'rate': 11.00, 'description': 'Full gut HYBRID'},
        
        # Framing
        'FRAM-01': {'rate': 77.00, 'description': 'Metal framing 8-10 ft high'},
        'FRAM-02': {'rate': 9.00, 'description': 'Dropped ceiling SF'},
        'FRAM-04': {'rate': 55.00, 'description': 'Frame new soffit'},
        
        # Drywall
        'CARP-10': {'rate': 4.00, 'description': '5/8" drywall wall board'},
        'CARP-11': {'rate': 4.95, 'description': '5/8" drywall ceiling board'},
        
        # Finishes
        'FINSH-02': {'rate': 4.00, 'description': 'Ceiling painting'},
        'FINSH-04': {'rate': 18.00, 'description': 'Tile installation'},
        'FINSH-05': {'rate': 10.30, 'description': 'Benjamin Moore paint'},
        'FINSH-06': {'rate': 6.00, 'description': 'Engineered flooring'},
        
        # Electrical
        'ELEC-02': {'rate': 175.00, 'description': 'Light fixture'},
        'ELEC-05': {'rate': 165.00, 'description': 'Light fixture'},
        'ELEC-06': {'rate': 55.00, 'description': 'Outlet'},
        'ELEC-12': {'rate': 440.00, 'description': 'Outlet new location'},
        
        # Plumbing
        'PLMB-13': {'rate': 750.00, 'description': 'New sink installation'},
        'PLMB-14': {'rate': 650.00, 'description': 'New toilet installation'},
        
        # Doors
        'DOOR-01': {'rate': 550.00, 'description': 'Standard door'},
        'DOOR-03': {'rate': 825.00, 'description': 'Double door'},
        
        # Kitchen/Millwork
        'KITC-10': {'rate': 800.00, 'description': 'Kitchen cabinets standard'},
        
        # Stone
        'STON-02': {'rate': 97.00, 'description': 'Kitchen countertop fabricate/install'},
        
        # Bathroom rates (derived from pricing sheet)
        'BATH-02': {'rate': 19.00, 'description': 'Bathroom waterproofing 0-60 SF'}
    }
    
    # Analyze each item
    internal_pricing_count = 0
    estimated_pricing_count = 0
    
    print("\n📋 ITEM ANALYSIS:")
    print("-" * 80)
    
    for item in items:
        item_name = item['ItemName']
        unit_cost = float(item['UnitCost'].replace('$', ''))
        
        # Check if this matches internal pricing
        found_internal = False
        for code, details in internal_rates.items():
            if abs(unit_cost - details['rate']) < 0.01:  # Exact match
                print(f"✅ {item_name:35} | ${unit_cost:>8.2f} | {code:>8} | {details['description']}")
                internal_pricing_count += 1
                found_internal = True
                break
        
        if not found_internal:
            print(f"⚠️  {item_name:35} | ${unit_cost:>8.2f} | {'ESTIMATED':>8} | Market rate")
            estimated_pricing_count += 1
    
    print(f"\n📊 PRICING SOURCE SUMMARY:")
    print(f"✅ Internal pricing: {internal_pricing_count} items")
    print(f"⚠️  Estimated pricing: {estimated_pricing_count} items")
    print(f"📈 Internal pricing coverage: {(internal_pricing_count/len(items)*100):.1f}%")
    
    # Scope coverage analysis
    print(f"\n🔍 SCOPE COVERAGE ANALYSIS:")
    print("-" * 80)
    
    # Key scope items from takeoff
    takeoff_scope = {
        'Flooring': {
            'Carpet Tile': {'quantity': 8625, 'unit': 'SF', 'found': False},
            'Engineered Wood': {'quantity': 4875, 'unit': 'SF', 'found': False},
            'Pantry Tile': {'quantity': 225, 'unit': 'SF', 'found': False},
            'Restroom Tile': {'quantity': 825, 'unit': 'SF', 'found': False},
            'VCT/SDT': {'quantity': 300, 'unit': 'SF', 'found': False},
            'Mosaic Tile': {'quantity': 150, 'unit': 'SF', 'found': False}
        },
        'Walls & Ceilings': {
            'Metal Studs': {'quantity': 700, 'unit': 'LF', 'found': False},
            'GWB': {'quantity': 12600, 'unit': 'SF', 'found': False},
            'Track': {'quantity': 1400, 'unit': 'LF', 'found': False},
            'Insulation': {'quantity': 6300, 'unit': 'SF', 'found': False},
            'ACT Ceiling': {'quantity': 8625, 'unit': 'SF', 'found': False},
            'GWB Ceilings': {'quantity': 2000, 'unit': 'SF', 'found': False},
            'Open Ceiling Paint': {'quantity': 8250, 'unit': 'SF', 'found': False}
        },
        'Wall Finishes': {
            'Wall Paint': {'quantity': 16800, 'unit': 'SF', 'found': False},
            'Trim/Door Paint': {'quantity': 1200, 'unit': 'SF', 'found': False},
            'Wallpaper': {'quantity': 800, 'unit': 'SF', 'found': False},
            'Wood Panels': {'quantity': 2000, 'unit': 'SF', 'found': False},
            'Wallcovering': {'quantity': 3800, 'unit': 'SF', 'found': False},
            'Reeded Glass': {'quantity': 1800, 'unit': 'SF', 'found': False},
            'Rubber Base': {'quantity': 604, 'unit': 'LF', 'found': False},
            'Wood Base': {'quantity': 345, 'unit': 'LF', 'found': False}
        },
        'Doors & Hardware': {
            'Solid Doors': {'quantity': 20, 'unit': 'EA', 'found': False},
            'Glass Doors': {'quantity': 24, 'unit': 'EA', 'found': False},
            'Hardware': {'quantity': 44, 'unit': 'Sets', 'found': False},
            'Pull Handles': {'quantity': 24, 'unit': 'Sets', 'found': False}
        },
        'Lighting & Electrical': {
            'Round Flushmounts': {'quantity': 80, 'unit': 'EA', 'found': False},
            'Recessed Downlights': {'quantity': 60, 'unit': 'EA', 'found': False},
            'Wall Sconces': {'quantity': 30, 'unit': 'EA', 'found': False},
            'Power Outlets': {'quantity': 250, 'unit': 'EA', 'found': False},
            'Dedicated Circuits': {'quantity': 15, 'unit': 'EA', 'found': False}
        },
        'Plumbing': {
            'Water Closets': {'quantity': 7, 'unit': 'EA', 'found': False},
            'Urinals': {'quantity': 1, 'unit': 'EA', 'found': False},
            'Lavatories': {'quantity': 8, 'unit': 'EA', 'found': False},
            'Faucets': {'quantity': 8, 'unit': 'EA', 'found': False},
            'Paper Towel': {'quantity': 4, 'unit': 'EA', 'found': False},
            'Toilet Roll': {'quantity': 4, 'unit': 'EA', 'found': False},
            'ADA Grab Bars': {'quantity': 6, 'unit': 'EA', 'found': False}
        },
        'Millwork': {
            'Pantry Island': {'quantity': 10, 'unit': 'LF', 'found': False},
            'Pantry Arches': {'quantity': 25, 'unit': 'LF', 'found': False},
            'Lounge Built-ins': {'quantity': 20, 'unit': 'LF', 'found': False},
            'Arch Trim': {'quantity': 30, 'unit': 'LF', 'found': False}
        },
        'Specialty': {
            'Countertops': {'quantity': 85, 'unit': 'SF', 'found': False},
            'Antique Mirror': {'quantity': 80, 'unit': 'SF', 'found': False},
            'Metal Mesh': {'quantity': 60, 'unit': 'SF', 'found': False}
        }
    }
    
    # Check each item against takeoff scope
    for item in items:
        item_name = item['ItemName']
        quantity = float(item['Quantity'])
        
        for category, scope_items in takeoff_scope.items():
            for scope_name, scope_details in scope_items.items():
                if scope_name.lower() in item_name.lower():
                    scope_details['found'] = True
                    # Check if quantity matches
                    if abs(quantity - scope_details['quantity']) <= 1:
                        print(f"✅ {scope_name:25} | {quantity:>8} {scope_details['unit']} | {category}")
                    else:
                        print(f"⚠️  {scope_name:25} | {quantity:>8} {scope_details['unit']} | {category} | QTY MISMATCH")
                    break
    
    # Report missing items
    print(f"\n❌ MISSING SCOPE ITEMS:")
    print("-" * 80)
    missing_count = 0
    for category, scope_items in takeoff_scope.items():
        for scope_name, scope_details in scope_items.items():
            if not scope_details['found']:
                print(f"❌ {scope_name:25} | {scope_details['quantity']:>8} {scope_details['unit']} | {category}")
                missing_count += 1
    
    total_scope_items = sum(len(scope_items) for scope_items in takeoff_scope.values())
    found_scope_items = total_scope_items - missing_count
    
    print(f"\n📊 SCOPE COVERAGE SUMMARY:")
    print(f"✅ Found: {found_scope_items} items")
    print(f"❌ Missing: {missing_count} items")
    print(f"📈 Coverage: {(found_scope_items/total_scope_items*100):.1f}%")
    
    # Final summary
    print(f"\n🎯 FINAL VERIFICATION SUMMARY:")
    print("=" * 80)
    print(f"💰 PRICING:")
    print(f"   • Internal pricing coverage: {(internal_pricing_count/(internal_pricing_count+estimated_pricing_count)*100):.1f}%")
    print(f"   • Items using internal rates: {internal_pricing_count}")
    print(f"   • Items using estimated rates: {estimated_pricing_count}")
    
    print(f"\n📋 SCOPE:")
    print(f"   • Scope coverage: {(found_scope_items/(found_scope_items+missing_count)*100):.1f}%")
    print(f"   • Items covered: {found_scope_items}")
    print(f"   • Items missing: {missing_count}")
    
    if internal_pricing_count/(internal_pricing_count+estimated_pricing_count) >= 0.9:
        print(f"\n✅ PRICING: EXCELLENT - Using maximum internal pricing")
    elif internal_pricing_count/(internal_pricing_count+estimated_pricing_count) >= 0.8:
        print(f"\n⚠️  PRICING: VERY GOOD - Using mostly internal pricing")
    else:
        print(f"\n❌ PRICING: NEEDS IMPROVEMENT - Too many estimated rates")
    
    if found_scope_items/(found_scope_items+missing_count) >= 0.95:
        print(f"✅ SCOPE: EXCELLENT - Comprehensive coverage")
    elif found_scope_items/(found_scope_items+missing_count) >= 0.9:
        print(f"⚠️  SCOPE: VERY GOOD - Good coverage")
    else:
        print(f"❌ SCOPE: NEEDS IMPROVEMENT - Missing many items")

if __name__ == "__main__":
    final_comprehensive_verification()

