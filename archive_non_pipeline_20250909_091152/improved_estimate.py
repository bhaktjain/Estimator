#!/usr/bin/env python3
"""
Generate improved estimate for 113 University Place including all missing items
"""
import csv
import json

def create_improved_estimate():
    """Create comprehensive estimate with all missing items from takeoff."""
    
    items = [
        # DEMOLITION & PROTECTION
        {
            'Category': 'Demolition & Protection',
            'Room': 'General',
            'ItemName': 'Soft Demo & Protection',
            'Description': 'Soft demolition of existing finishes and protection of existing MEP systems and finishes.',
            'Quantity': '15000',
            'UnitCost': '$8.00',
            'Markup': '0.75',
            'MarkupType': '%',
            'Total': '210000.00',
            'Confidence': '90'
        },
        
        # FLOORING - COMPLETE
        {
            'Category': 'Flooring',
            'Room': 'Open Office',
            'ItemName': 'Carpet Tile Installation',
            'Description': 'Install Bentley Outside the Box carpet tiles with cushion backing in open office areas.',
            'Quantity': '8625',
            'UnitCost': '$6.00',
            'Markup': '0.75',
            'MarkupType': '%',
            'Total': '90562.50',
            'Confidence': '95'
        },
        {
            'Category': 'Flooring',
            'Room': 'Corridors/Lounge',
            'ItemName': 'Engineered Wood Flooring',
            'Description': 'Install The Hudson Co. Walnut flat sawn engineered wood flooring in corridors and lounge bands.',
            'Quantity': '4875',
            'UnitCost': '$6.00',
            'Markup': '0.75',
            'MarkupType': '%',
            'Total': '51281.25',
            'Confidence': '95'
        },
        {
            'Category': 'Flooring',
            'Room': 'Pantry',
            'ItemName': 'Porcelain Tile Installation',
            'Description': 'Install Fireclay Quartzite Matte Star porcelain floor tile in the 4F pantry zone.',
            'Quantity': '225',
            'UnitCost': '$12.00',
            'Markup': '0.80',
            'MarkupType': '%',
            'Total': '4860.00',
            'Confidence': '95'
        },
        {
            'Category': 'Flooring',
            'Room': 'Restrooms',
            'ItemName': 'Porcelain Tile Installation',
            'Description': 'Install Tilebar Rizo Silver Beige porcelain floor tile in all restroom floors on 4F & 5F.',
            'Quantity': '825',
            'UnitCost': '$12.00',
            'Markup': '0.80',
            'MarkupType': '%',
            'Total': '17820.00',
            'Confidence': '95'
        },
        {
            'Category': 'Flooring',
            'Room': 'IT/Copy/ESD',
            'ItemName': 'VCT/SDT Installation',
            'Description': 'Install Armstrong VCT/SDT in IT/Copy/ESD small rooms.',
            'Quantity': '300',
            'UnitCost': '$8.00',
            'Markup': '0.75',
            'MarkupType': '%',
            'Total': '4200.00',
            'Confidence': '90'
        },
        {
            'Category': 'Flooring',
            'Room': 'Elevator Lobby',
            'ItemName': 'Mosaic Tile Installation',
            'Description': 'Install B/W brand mosaic tile in small vestibules both floors.',
            'Quantity': '150',
            'UnitCost': '$15.00',
            'Markup': '0.80',
            'MarkupType': '%',
            'Total': '4050.00',
            'Confidence': '90'
        },
        
        # WALLS & CEILINGS - COMPLETE
        {
            'Category': 'Walls & Ceilings',
            'Room': 'Partitions',
            'ItemName': 'Metal Stud Framing',
            'Description': 'Install new metal studs for partitions at 3-5/8" @ 16" o.c., 10\' height.',
            'Quantity': '700',
            'UnitCost': '$77.00',
            'Markup': '0.75',
            'MarkupType': '%',
            'Total': '94325.00',
            'Confidence': '90'
        },
        {
            'Category': 'Walls & Ceilings',
            'Room': 'Partitions',
            'ItemName': 'GWB Installation',
            'Description': 'Install 5/8" Type X GWB on both sides of partitions.',
            'Quantity': '12600',
            'UnitCost': '$4.00',
            'Markup': '0.75',
            'MarkupType': '%',
            'Total': '88200.00',
            'Confidence': '90'
        },
        {
            'Category': 'Walls & Ceilings',
            'Room': 'Partitions',
            'ItemName': 'Track Installation',
            'Description': 'Install 3-5/8" top & bottom track for partitions.',
            'Quantity': '1400',
            'UnitCost': '$3.00',
            'Markup': '0.75',
            'MarkupType': '%',
            'Total': '7350.00',
            'Confidence': '90'
        },
        {
            'Category': 'Walls & Ceilings',
            'Room': 'Partitions',
            'ItemName': 'Acoustic Insulation',
            'Description': 'Install 3-1/2" mineral wool acoustic batt insulation.',
            'Quantity': '6300',
            'UnitCost': '$2.50',
            'Markup': '0.75',
            'MarkupType': '%',
            'Total': '27562.50',
            'Confidence': '90'
        },
        {
            'Category': 'Walls & Ceilings',
            'Room': 'Open Office',
            'ItemName': 'ACT Ceiling System',
            'Description': 'Install 2x2 ACT ceiling system with Turf Pantheon look in open office ceiling zones.',
            'Quantity': '8625',
            'UnitCost': '$9.00',
            'Markup': '0.75',
            'MarkupType': '%',
            'Total': '135468.75',
            'Confidence': '90'
        },
        {
            'Category': 'Walls & Ceilings',
            'Room': 'Meeting Rooms/Wellness/Corridors',
            'ItemName': 'GWB Ceilings',
            'Description': 'Install flat and bulkhead GWB ceilings.',
            'Quantity': '2000',
            'UnitCost': '$4.95',
            'Markup': '0.75',
            'MarkupType': '%',
            'Total': '17325.00',
            'Confidence': '90'
        },
        {
            'Category': 'Walls & Ceilings',
            'Room': 'Open Areas',
            'ItemName': 'Open Ceiling Paint',
            'Description': 'Field paint to 4F ~60% + 5F ~50% of floor plates deck/structure.',
            'Quantity': '8250',
            'UnitCost': '$3.00',
            'Markup': '0.75',
            'MarkupType': '%',
            'Total': '43312.50',
            'Confidence': '90'
        },
        
        # WALL FINISHES - COMPLETE
        {
            'Category': 'Wall Finishes',
            'Room': 'General',
            'ItemName': 'Wall Painting',
            'Description': 'Paint walls with Benjamin Moore Newburyport Blue and field whites.',
            'Quantity': '16800',
            'UnitCost': '$10.30',
            'Markup': '0.75',
            'MarkupType': '%',
            'Total': '302670.00',
            'Confidence': '90'
        },
        {
            'Category': 'Wall Finishes',
            'Room': 'Corridors',
            'ItemName': 'Trim/Door Painting',
            'Description': 'Paint corridor door and trim packages with matching satin finish.',
            'Quantity': '1200',
            'UnitCost': '$10.30',
            'Markup': '0.75',
            'MarkupType': '%',
            'Total': '21645.00',
            'Confidence': '90'
        },
        {
            'Category': 'Wall Finishes',
            'Room': 'Feature Walls',
            'ItemName': 'Specialty Wallpaper Installation',
            'Description': 'Install dark blue Art-Deco patterned specialty wallpaper on feature walls.',
            'Quantity': '800',
            'UnitCost': '$15.00',
            'Markup': '0.75',
            'MarkupType': '%',
            'Total': '21000.00',
            'Confidence': '90'
        },
        {
            'Category': 'Wall Finishes',
            'Room': 'Art Walls/Corridors/Millwork',
            'ItemName': 'Wood-Look Wall Panels',
            'Description': 'Install Momentum "Wood Heights" Black Walnut / Wilsonart "Walnut Heights" panels.',
            'Quantity': '2000',
            'UnitCost': '$18.00',
            'Markup': '0.75',
            'MarkupType': '%',
            'Total': '63000.00',
            'Confidence': '90'
        },
        {
            'Category': 'Wall Finishes',
            'Room': 'General',
            'ItemName': 'Wallcovering Installation',
            'Description': 'Install Designtex Wannabe Rib (Oat/Navy) wallcovering.',
            'Quantity': '3800',
            'UnitCost': '$12.00',
            'Markup': '0.75',
            'MarkupType': '%',
            'Total': '79800.00',
            'Confidence': '90'
        },
        {
            'Category': 'Wall Finishes',
            'Room': 'Office Fronts & Glass Partitions',
            'ItemName': 'Reeded Glass Film Installation',
            'Description': 'Install SOLYX SX-1254 1/2" reeded glass film on office fronts & glass partitions.',
            'Quantity': '1800',
            'UnitCost': '$8.00',
            'Markup': '0.75',
            'MarkupType': '%',
            'Total': '25200.00',
            'Confidence': '90'
        },
        {
            'Category': 'Wall Finishes',
            'Room': 'Carpet Areas',
            'ItemName': 'Rubber Base Installation',
            'Description': 'Install 4" rubber base in carpet areas.',
            'Quantity': '604',
            'UnitCost': '$8.00',
            'Markup': '0.75',
            'MarkupType': '%',
            'Total': '8456.00',
            'Confidence': '90'
        },
        {
            'Category': 'Wall Finishes',
            'Room': 'Wood Flooring Areas',
            'ItemName': 'Wood Base/Shoe Installation',
            'Description': 'Install wood base/shoe stained to match wood flooring.',
            'Quantity': '345',
            'UnitCost': '$12.00',
            'Markup': '0.75',
            'MarkupType': '%',
            'Total': '7245.00',
            'Confidence': '90'
        },
        
        # DOORS & HARDWARE - COMPLETE
        {
            'Category': 'Doors & Hardware',
            'Room': 'General',
            'ItemName': 'Solid-Core Wood Doors',
            'Description': 'Install solid-core wood doors for toilets, IT/Storage, Copy, Wellness, etc.',
            'Quantity': '20',
            'UnitCost': '$550.00',
            'Markup': '0.75',
            'MarkupType': '%',
            'Total': '19250.00',
            'Confidence': '90'
        },
        {
            'Category': 'Doors & Hardware',
            'Room': 'Office Fronts',
            'ItemName': 'Glass Office-Front Doors',
            'Description': 'Install arched motif, single-leaf glass office-front doors.',
            'Quantity': '24',
            'UnitCost': '$825.00',
            'Markup': '0.75',
            'MarkupType': '%',
            'Total': '34650.00',
            'Confidence': '90'
        },
        {
            'Category': 'Doors & Hardware',
            'Room': 'General',
            'ItemName': 'Door Hardware Installation',
            'Description': 'Install Schlage ND Series (satin Grade 1 brass) door hardware.',
            'Quantity': '44',
            'UnitCost': '$150.00',
            'Markup': '0.75',
            'MarkupType': '%',
            'Total': '11550.00',
            'Confidence': '90'
        },
        {
            'Category': 'Doors & Hardware',
            'Room': 'Glass Doors',
            'ItemName': 'Pull Handles Installation',
            'Description': 'Install locking asymmetric pulls + floor deadbolt for glass doors.',
            'Quantity': '24',
            'UnitCost': '$200.00',
            'Markup': '0.75',
            'MarkupType': '%',
            'Total': '8400.00',
            'Confidence': '90'
        },
        
        # LIGHTING & ELECTRICAL - COMPLETE
        {
            'Category': 'Lighting & Electrical',
            'Room': 'Open Office',
            'ItemName': 'Round Flushmounts',
            'Description': 'Install 6–8" LED round flushmounts in open office grid.',
            'Quantity': '80',
            'UnitCost': '$165.00',
            'Markup': '0.75',
            'MarkupType': '%',
            'Total': '23100.00',
            'Confidence': '90'
        },
        {
            'Category': 'Lighting & Electrical',
            'Room': 'Meeting Rooms/Corridors/Restrooms',
            'ItemName': 'Recessed Downlights',
            'Description': 'Install 3" recessed downlights in gypsum areas.',
            'Quantity': '60',
            'UnitCost': '$165.00',
            'Markup': '0.75',
            'MarkupType': '%',
            'Total': '17325.00',
            'Confidence': '90'
        },
        {
            'Category': 'Lighting & Electrical',
            'Room': 'Open Ceiling Bands/Pantry',
            'ItemName': 'Sphere Pendants',
            'Description': 'Install "Novato Globes" sphere pendants.',
            'Quantity': '70',
            'UnitCost': '$250.00',
            'Markup': '0.75',
            'MarkupType': '%',
            'Total': '30625.00',
            'Confidence': '90'
        },
        {
            'Category': 'Lighting & Electrical',
            'Room': 'Pantry/Lounge',
            'ItemName': 'Feature Chandelier',
            'Description': 'Install Arcachon chandelier in pantry/lounge feature area.',
            'Quantity': '1',
            'UnitCost': '$5000.00',
            'Markup': '0.75',
            'MarkupType': '%',
            'Total': '8750.00',
            'Confidence': '90'
        },
        {
            'Category': 'Lighting & Electrical',
            'Room': 'Art Walls/Lounge',
            'ItemName': 'Track Lighting',
            'Description': 'Install MPL L225SR track lighting with dimmable LED heads.',
            'Quantity': '48',
            'UnitCost': '$45.00',
            'Markup': '0.75',
            'MarkupType': '%',
            'Total': '3780.00',
            'Confidence': '90'
        },
        {
            'Category': 'Lighting & Electrical',
            'Room': 'Shelf/Arch Areas',
            'ItemName': 'Linear LED Strips',
            'Description': 'Install linear LED strips for shelf/arch lighting.',
            'Quantity': '250',
            'UnitCost': '$25.00',
            'Markup': '0.75',
            'MarkupType': '%',
            'Total': '10937.50',
            'Confidence': '90'
        },
        {
            'Category': 'Lighting & Electrical',
            'Room': 'General',
            'ItemName': 'Wall Sconces',
            'Description': 'Install Kohler/RBW/Boyd/Lumens wall sconces.',
            'Quantity': '30',
            'UnitCost': '$300.00',
            'Markup': '0.75',
            'MarkupType': '%',
            'Total': '15750.00',
            'Confidence': '90'
        },
        {
            'Category': 'Lighting & Electrical',
            'Room': 'General',
            'ItemName': 'General Power Outlets',
            'Description': 'Install duplex receptacles throughout.',
            'Quantity': '250',
            'UnitCost': '$85.00',
            'Markup': '0.75',
            'MarkupType': '%',
            'Total': '37187.50',
            'Confidence': '90'
        },
        {
            'Category': 'Lighting & Electrical',
            'Room': 'Pantry/Coffee/IT',
            'ItemName': 'Dedicated Circuits',
            'Description': 'Install dedicated circuits for appliances/IT equipment.',
            'Quantity': '15',
            'UnitCost': '$400.00',
            'Markup': '0.75',
            'MarkupType': '%',
            'Total': '10500.00',
            'Confidence': '90'
        },
        
        # PLUMBING FIXTURES - COMPLETE
        {
            'Category': 'Plumbing Fixtures',
            'Room': 'Restrooms',
            'ItemName': 'Water Closets',
            'Description': 'Install Sloan CX (floor) / ST-2469 (wall) water closets.',
            'Quantity': '7',
            'UnitCost': '$550.00',
            'Markup': '0.75',
            'MarkupType': '%',
            'Total': '6737.50',
            'Confidence': '90'
        },
        {
            'Category': 'Plumbing Fixtures',
            'Room': 'Restrooms',
            'ItemName': 'Urinals',
            'Description': 'Install Sloan SU-7019 urinals.',
            'Quantity': '1',
            'UnitCost': '$400.00',
            'Markup': '0.75',
            'MarkupType': '%',
            'Total': '700.00',
            'Confidence': '90'
        },
        {
            'Category': 'Plumbing Fixtures',
            'Room': 'Restrooms',
            'ItemName': 'Restroom Lavatories',
            'Description': 'Install Kohler Compass / Rejuvenation Atlanta restroom lavatories.',
            'Quantity': '8',
            'UnitCost': '$550.00',
            'Markup': '0.75',
            'MarkupType': '%',
            'Total': '7700.00',
            'Confidence': '90'
        },
        {
            'Category': 'Plumbing Fixtures',
            'Room': 'Restrooms',
            'ItemName': 'Restroom Faucets',
            'Description': 'Install Sloan EAF-200 deck-mounted, hard-wired faucets.',
            'Quantity': '8',
            'UnitCost': '$200.00',
            'Markup': '0.75',
            'MarkupType': '%',
            'Total': '2800.00',
            'Confidence': '90'
        },
        {
            'Category': 'Plumbing Fixtures',
            'Room': 'Restrooms',
            'ItemName': 'Paper Towel Dispensers',
            'Description': 'Install Bobrick B-38034.MBLK paper towel dispensers.',
            'Quantity': '4',
            'UnitCost': '$150.00',
            'Markup': '0.75',
            'MarkupType': '%',
            'Total': '1050.00',
            'Confidence': '90'
        },
        {
            'Category': 'Plumbing Fixtures',
            'Room': 'Restrooms',
            'ItemName': 'Toilet Roll Holders',
            'Description': 'Install Bobrick B-540.MBLK toilet roll holders.',
            'Quantity': '4',
            'UnitCost': '$100.00',
            'Markup': '0.75',
            'MarkupType': '%',
            'Total': '700.00',
            'Confidence': '90'
        },
        {
            'Category': 'Plumbing Fixtures',
            'Room': 'ADA Restrooms',
            'ItemName': 'ADA Grab Bars',
            'Description': 'Install 42"/36" sets of ADA grab bars.',
            'Quantity': '6',
            'UnitCost': '$200.00',
            'Markup': '0.75',
            'MarkupType': '%',
            'Total': '2100.00',
            'Confidence': '90'
        },
        
        # CUSTOM MILLWORK - COMPLETE
        {
            'Category': 'Custom Millwork',
            'Room': 'Pantry',
            'ItemName': 'Pantry Island Millwork',
            'Description': 'Install custom walnut millwork for pantry island with integrated lighting.',
            'Quantity': '10',
            'UnitCost': '$800.00',
            'Markup': '0.75',
            'MarkupType': '%',
            'Total': '14000.00',
            'Confidence': '90'
        },
        {
            'Category': 'Custom Millwork',
            'Room': 'Pantry/Coffee',
            'ItemName': 'Pantry Arches & Shelves',
            'Description': 'Install custom walnut millwork for pantry arches and lounge shelves.',
            'Quantity': '25',
            'UnitCost': '$600.00',
            'Markup': '0.75',
            'MarkupType': '%',
            'Total': '26250.00',
            'Confidence': '90'
        },
        {
            'Category': 'Custom Millwork',
            'Room': 'Lounge/AV',
            'ItemName': 'Lounge Built-ins',
            'Description': 'Install walnut look millwork with LED lighting for lounge & meeting built-ins.',
            'Quantity': '20',
            'UnitCost': '$500.00',
            'Markup': '0.75',
            'MarkupType': '%',
            'Total': '17500.00',
            'Confidence': '90'
        },
        {
            'Category': 'Custom Millwork',
            'Room': 'General',
            'ItemName': 'Arch Trim',
            'Description': 'Install bronze/brass arch trim on glass/arches.',
            'Quantity': '30',
            'UnitCost': '$150.00',
            'Markup': '0.75',
            'MarkupType': '%',
            'Total': '7875.00',
            'Confidence': '90'
        },
        
        # COUNTERTOPS - COMPLETE
        {
            'Category': 'Countertops',
            'Room': 'Pantry/Coffee/Copy',
            'ItemName': 'Breccia Vino Marble Countertops',
            'Description': 'Install Breccia Vino marble slab countertops in pantry, coffee, and copy areas.',
            'Quantity': '85',
            'UnitCost': '$97.00',
            'Markup': '0.75',
            'MarkupType': '%',
            'Total': '14376.25',
            'Confidence': '95'
        },
        
        # SPECIALTY FINISHES
        {
            'Category': 'Specialty Finishes',
            'Room': 'Backs of Arches/Pantry/Coffee',
            'ItemName': 'Antique Mirror Installation',
            'Description': 'Install antique mirror on backs of arches/pantry/coffee architecture.',
            'Quantity': '80',
            'UnitCost': '$25.00',
            'Markup': '0.75',
            'MarkupType': '%',
            'Total': '3500.00',
            'Confidence': '90'
        },
        {
            'Category': 'Specialty Finishes',
            'Room': 'Pantry Arches',
            'ItemName': 'Metal Mesh Installation',
            'Description': 'Install Gage GW906 metal mesh in pantry arches.',
            'Quantity': '60',
            'UnitCost': '$35.00',
            'Markup': '0.75',
            'MarkupType': '%',
            'Total': '3675.00',
            'Confidence': '90'
        },
        
        # COMMERCIAL CLEANING
        {
            'Category': 'Commercial Cleaning',
            'Room': 'General',
            'ItemName': 'Post-Construction Cleaning',
            'Description': 'Comprehensive cleaning of all renovated areas post-construction.',
            'Quantity': '15000',
            'UnitCost': '$0.55',
            'Markup': '0.75',
            'MarkupType': '%',
            'Total': '14343.75',
            'Confidence': '85'
        }
    ]
    
    return items

def write_csv(items, filename):
    """Write items to CSV file."""
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['Category', 'Room', 'ItemName', 'Description', 'Quantity', 'UnitCost', 'Markup', 'MarkupType', 'Total', 'Confidence']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(items)
    
    print(f"✅ Written {len(items)} items to {filename}")
    
    # Calculate totals by category
    categories = {}
    for item in items:
        cat = item['Category']
        if cat not in categories:
            categories[cat] = 0
        categories[cat] += float(item['Total'])
    
    print("\n📊 Category Totals:")
    print("=" * 60)
    for cat, total in sorted(categories.items()):
        print(f"{cat:25} | ${total:>12,.2f}")
    
    grand_total = sum(categories.values())
    print("=" * 60)
    print(f"{'GRAND TOTAL':25} | ${grand_total:>12,.2f}")
    
    # Add 10% general conditions
    general_conditions = grand_total * 0.10
    final_total = grand_total + general_conditions
    print(f"{'General Conditions (10%)':25} | ${general_conditions:>12,.2f}")
    print(f"{'FINAL TOTAL':25} | ${final_total:>12,.2f}")
    
    return grand_total

def main():
    """Main function to create improved estimate."""
    print("🏗️  Creating Improved 113 University Place Estimate...")
    print("=" * 60)
    
    # Create improved estimate
    items = create_improved_estimate()
    
    # Write to CSV
    csv_filename = '113_University_Place_Improved_Estimate.csv'
    total = write_csv(items, csv_filename)
    
    print(f"\n🎯 Estimate Summary:")
    print(f"Total Items: {len(items)}")
    print(f"Base Cost: ${total:,.2f}")
    print(f"General Conditions (10%): ${total * 0.10:,.2f}")
    print(f"Final Total: ${total * 1.10:,.2f}")
    
    print(f"\n📁 Files created:")
    print(f"✅ {csv_filename}")

if __name__ == "__main__":
    main()

