#!/usr/bin/env python3
"""
Add missing materials to the final estimate with proper labor + material pricing
"""
import csv

def add_missing_materials():
    """Add all missing materials with proper pricing."""
    
    print("🔧 ADDING MISSING MATERIALS WITH LABOR + MATERIAL PRICING")
    print("=" * 70)
    
    # Read existing estimate
    existing_items = []
    with open('113_University_Place_FINAL_Complete_Estimate.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        existing_items = list(reader)
    
    print(f"📖 Loaded {len(existing_items)} existing items")
    
    # Missing materials that need to be added
    missing_items = [
        # MICROWAVE & FOOT RAIL (CRITICAL MISSING)
        {
            'Category': 'Appliances',
            'Room': 'Pantry',
            'ItemName': 'Trade Diversified 24" Microwave Drawer',
            'Description': 'Install Trade Diversified 24" microwave drawer with Wilsonart Wallaby integration',
            'Quantity': '1',
            'UnitCost': '$450.00',  # Labor + Material
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '765.00',
            'Confidence': '95'
        },
        {
            'Category': 'Millwork',
            'Room': 'Pantry',
            'ItemName': 'Pegasus Foot Rail - Brass/Bronze',
            'Description': 'Install Pegasus foot rail with brass/bronze finish for pantry island (10 LF)',
            'Quantity': '10',
            'UnitCost': '$85.00',  # Labor + Material
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '1445.00',
            'Confidence': '95'
        },
        
        # LINEAR LED LIGHTING (MISSING)
        {
            'Category': 'Lighting & Electrical',
            'Room': 'General',
            'ItemName': 'Linear LED Strips - Shelf/Arch Lighting',
            'Description': 'Install linear LED strips for shelf/arch lighting throughout (250 LF)',
            'Quantity': '250',
            'UnitCost': '$45.00',  # Labor + Material
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '19125.00',
            'Confidence': '95'
        },
        {
            'Category': 'Lighting & Electrical',
            'Room': 'General',
            'ItemName': 'PICASSO IT LED - 4.15W/FT with Vacancy Dimming',
            'Description': 'Install PICASSO IT LED 4.15W/FT with vacancy dimming sensors and 0-10V control',
            'Quantity': '250',
            'UnitCost': '$55.00',  # Labor + Material
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '23375.00',
            'Confidence': '95'
        },
        
        # CABINET HARDWARE (MISSING)
        {
            'Category': 'Millwork',
            'Room': 'General',
            'ItemName': 'Soft-Close Hinges - All Cabinets',
            'Description': 'Install soft-close hinges for all cabinet doors throughout (200 EA)',
            'Quantity': '200',
            'UnitCost': '$25.00',  # Labor + Material
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '8500.00',
            'Confidence': '95'
        },
        {
            'Category': 'Millwork',
            'Room': 'General',
            'ItemName': 'Drawer Slides - 3" Integrated Full Extension',
            'Description': 'Install 3" integrated full extension drawer slides for all drawers (80 EA)',
            'Quantity': '80',
            'UnitCost': '$35.00',  # Labor + Material
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '4760.00',
            'Confidence': '95'
        },
        {
            'Category': 'Millwork',
            'Room': 'General',
            'ItemName': 'Crown Molding Installation',
            'Description': 'Install crown molding around perimeter for indirect lighting reveal (500 LF)',
            'Quantity': '500',
            'UnitCost': '$17.00',  # Labor + Material
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '14450.00',
            'Confidence': '95'
        },
        
        # SHELF & DRAWER COMPONENTS (MISSING)
        {
            'Category': 'Millwork',
            'Room': 'General',
            'ItemName': 'Duty Shelf Clips - PL-Finish Brass Railing',
            'Description': 'Install duty shelf clips with PL-finish and brass railing (200 EA)',
            'Quantity': '200',
            'UnitCost': '$15.00',  # Labor + Material
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '5100.00',
            'Confidence': '95'
        },
        {
            'Category': 'Millwork',
            'Room': 'General',
            'ItemName': 'Drawer Support Systems',
            'Description': 'Install drawer support systems and finger pull hardware (80 EA)',
            'Quantity': '80',
            'UnitCost': '$20.00',  # Labor + Material
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '2720.00',
            'Confidence': '95'
        },
        
        # LIGHTING CONTROLS & SENSORS (MISSING)
        {
            'Category': 'Lighting & Electrical',
            'Room': 'General',
            'ItemName': 'Vacancy Dimming Sensors - 0-10V Control',
            'Description': 'Install vacancy dimming sensors with 0-10V control throughout (50 EA)',
            'Quantity': '50',
            'UnitCost': '$120.00',  # Labor + Material
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '10200.00',
            'Confidence': '95'
        },
        {
            'Category': 'Lighting & Electrical',
            'Room': 'General',
            'ItemName': 'Occupancy Sensors - Auto Lighting Control',
            'Description': 'Install occupancy sensors for automatic lighting control with 15-min auto-off (30 EA)',
            'Quantity': '30',
            'UnitCost': '$95.00',  # Labor + Material
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '4845.00',
            'Confidence': '95'
        },
        
        # SPECIALTY LIGHTING FIXTURES (MISSING)
        {
            'Category': 'Lighting & Electrical',
            'Room': 'General',
            'ItemName': 'SPI Lighting - LED 39W Vacancy 0-10V',
            'Description': 'Install SPI Lighting LED 39W fixtures with vacancy and 0-10V dimming (20 EA)',
            'Quantity': '20',
            'UnitCost': '$175.00',  # Labor + Material
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '5950.00',
            'Confidence': '95'
        },
        {
            'Category': 'Lighting & Electrical',
            'Room': 'General',
            'ItemName': 'BEGA LED 11.5W Sensors Unv Dimming',
            'Description': 'Install BEGA LED 11.5W fixtures with sensors and unv dimming (15 EA)',
            'Quantity': '15',
            'UnitCost': '$165.00',  # Labor + Material
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '4207.50',
            'Confidence': '95'
        },
        {
            'Category': 'Lighting & Electrical',
            'Room': 'General',
            'ItemName': 'BOYD LED 20W Sensors 0-10V - Knurled End Caps',
            'Description': 'Install BOYD LED 20W fixtures with sensors, 0-10V control, knurled end caps (25 EA)',
            'Quantity': '25',
            'UnitCost': '$155.00',  # Labor + Material
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '6587.50',
            'Confidence': '95'
        },
        {
            'Category': 'Lighting & Electrical',
            'Room': 'General',
            'ItemName': 'BOYD Lucia Sconce 10878 - 42" Length',
            'Description': 'Install BOYD Lucia Sconce 10878, 42" length with sensors and dimming (10 EA)',
            'Quantity': '10',
            'UnitCost': '$185.00',  # Labor + Material
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '3145.00',
            'Confidence': '95'
        },
        
        # DOOR HINGES (MISSING)
        {
            'Category': 'Doors & Hardware',
            'Room': 'General',
            'ItemName': 'Stanley US4 Butt Hinges - All Doors',
            'Description': 'Install Stanley US4 butt hinges for all doors (4 per door, 44 doors)',
            'Quantity': '176',
            'UnitCost': '$12.00',  # Labor + Material
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '3590.40',
            'Confidence': '95'
        },
        {
            'Category': 'Doors & Hardware',
            'Room': 'General',
            'ItemName': 'FALKBUILT Black Hinges - Glass Doors',
            'Description': 'Install FALKBUILT black hinges for glass office front doors (24 sets)',
            'Quantity': '24',
            'UnitCost': '$45.00',  # Labor + Material
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '1836.00',
            'Confidence': '95'
        },
        
        # ADDITIONAL TRIM & FINISHES (MISSING)
        {
            'Category': 'Wall Finishes',
            'Room': 'General',
            'ItemName': 'Window Casings and Trim',
            'Description': 'Install window casings and trim throughout (200 LF)',
            'Quantity': '200',
            'UnitCost': '$19.00',  # Labor + Material
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '6460.00',
            'Confidence': '95'
        },
        {
            'Category': 'Wall Finishes',
            'Room': 'General',
            'ItemName': 'Door Casings and Trim',
            'Description': 'Install door casings and trim throughout (300 LF)',
            'Quantity': '300',
            'UnitCost': '$19.00',  # Labor + Material
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '9690.00',
            'Confidence': '95'
        },
        {
            'Category': 'Wall Finishes',
            'Room': 'General',
            'ItemName': 'Quarter Round and Shoe Molding',
            'Description': 'Install quarter round and shoe molding for all transitions (400 LF)',
            'Quantity': '400',
            'UnitCost': '$19.00',  # Labor + Material
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '12920.00',
            'Confidence': '95'
        },
        
        # ELECTRICAL COMPONENTS (MISSING)
        {
            'Category': 'Lighting & Electrical',
            'Room': 'General',
            'ItemName': 'Raceways for Lighting Controls',
            'Description': 'Install raceways and conduit for lighting control systems (500 LF)',
            'Quantity': '500',
            'UnitCost': '$25.00',  # Labor + Material
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '21250.00',
            'Confidence': '95'
        },
        {
            'Category': 'Lighting & Electrical',
            'Room': 'General',
            'ItemName': 'Control Panels for Lighting Systems',
            'Description': 'Install control panels and wiring for 0-10V lighting control systems (5 EA)',
            'Quantity': '5',
            'UnitCost': '$550.00',  # Labor + Material
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '4675.00',
            'Confidence': '95'
        },
        
        # SPECIALTY FINISHES (MISSING)
        {
            'Category': 'Wall Finishes',
            'Room': 'General',
            'ItemName': 'Brushed Moderne Brass Finishes',
            'Description': 'Install brushed moderne brass finishes for specialty areas (100 SF)',
            'Quantity': '100',
            'UnitCost': '$45.00',  # Labor + Material
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '7650.00',
            'Confidence': '95'
        },
        {
            'Category': 'Wall Finishes',
            'Room': 'General',
            'ItemName': 'Unlacquered Bronze Finishes',
            'Description': 'Install unlacquered bronze finishes for specialty areas (80 SF)',
            'Quantity': '80',
            'UnitCost': '$55.00',  # Labor + Material
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '7480.00',
            'Confidence': '95'
        },
        {
            'Category': 'Wall Finishes',
            'Room': 'General',
            'ItemName': 'Earthen Bronze Finishes',
            'Description': 'Install earthen bronze finishes for specialty areas (60 SF)',
            'Quantity': '60',
            'UnitCost': '$50.00',  # Labor + Material
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '5100.00',
            'Confidence': '95'
        }
    ]
    
    print(f"🔧 Adding {len(missing_items)} missing materials")
    
    # Combine existing and missing items
    all_items = existing_items + missing_items
    
    # Write complete estimate CSV
    output_filename = '113_University_Place_COMPLETE_ALL_MATERIALS.csv'
    with open(output_filename, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['Category', 'Room', 'ItemName', 'Description', 'Quantity', 'UnitCost', 'Markup', 'MarkupType', 'Total', 'Confidence']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_items)
    
    print(f"\n✅ COMPLETE estimate with ALL materials saved to: {output_filename}")
    
    # Calculate final totals
    total = sum(float(item['Total']) for item in all_items)
    general_conditions = total * 0.10
    final_total = total + general_conditions
    
    print(f"\n📊 COMPLETE ESTIMATE TOTALS:")
    print(f"Base Cost: ${total:,.2f}")
    print(f"General Conditions (10%): ${general_conditions:,.2f}")
    print(f"Final Total: ${final_total:,.2f}")
    
    print(f"\n📋 TOTAL ITEMS: {len(all_items)}")
    print(f"  Original: {len(existing_items)}")
    print(f"  Added: {len(missing_items)}")
    
    # Show key missing materials now included
    print(f"\n🎯 MISSING MATERIALS NOW INCLUDED:")
    print(f"  ✅ Trade Diversified 24\" Microwave Drawer")
    print(f"  ✅ Pegasus Foot Rail - Brass/Bronze")
    print(f"  ✅ Linear LED Strips - 250 LF")
    print(f"  ✅ PICASSO IT LED with Vacancy Dimming")
    print(f"  ✅ Soft-Close Hinges - 200 EA")
    print(f"  ✅ Drawer Slides - 80 EA")
    print(f"  ✅ Crown Molding - 500 LF")
    print(f"  ✅ Duty Shelf Clips - 200 EA")
    print(f"  ✅ Vacancy Dimming Sensors - 50 EA")
    print(f"  ✅ SPI, BEGA, BOYD Specialty Lighting")
    print(f"  ✅ Stanley US4 Butt Hinges - 176 EA")
    print(f"  ✅ All Trim, Casings, and Specialty Finishes")
    
    return output_filename

if __name__ == "__main__":
    complete_file = add_missing_materials()
    print(f"\n🎯 Next step: Create Excel file from {complete_file}")

