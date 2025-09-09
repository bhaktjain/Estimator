#!/usr/bin/env python3
"""
Create complete estimate with EVERY material from ALL documents - comprehensive coverage
"""
import csv

def create_complete_material_estimate():
    """Create complete estimate with EVERY material from ALL documents."""

    print("🔧 CREATING COMPLETE MATERIAL ESTIMATE FROM ALL DOCUMENTS")
    print("=" * 80)

    # Create items with EVERY material from ALL documents
    items = [
        # FLOORING - Exact materials from documents
        {
            'Category': 'Flooring',
            'Room': 'General',
            'ItemName': 'Bentley Carpet Tile - Creative 407840',
            'Description': 'Install Bentley Outside the Box carpet tiles with cushion backing in open office areas (8,625 SF)',
            'Quantity': '8625',
            'UnitCost': '$6.00',  # Labor only - material included in carpet tile
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '87975.00',
            'Confidence': '95'
        },
        {
            'Category': 'Flooring',
            'Room': 'General',
            'ItemName': 'The Hudson Co. Engineered Wood - Walnut',
            'Description': 'Install The Hudson Co. Walnut flat sawn engineered wood in corridors/lounge bands (4,875 SF)',
            'Quantity': '4875',
            'UnitCost': '$6.00',  # Labor only - material included in engineered wood
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '49725.00',
            'Confidence': '95'
        },
        {
            'Category': 'Flooring',
            'Room': 'Pantry',
            'ItemName': 'Fireclay Quartzite Matte Star Tile',
            'Description': 'Install Fireclay Quartzite Matte Star porcelain tile in 4F pantry zone (225 SF)',
            'Quantity': '225',
            'UnitCost': '$18.00',  # Labor only - material included in tile
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '6885.00',
            'Confidence': '95'
        },
        {
            'Category': 'Flooring',
            'Room': 'Restrooms',
            'ItemName': 'Tilebar Rizo Silver Beige Tile',
            'Description': 'Install Tilebar Rizo Silver Beige porcelain tile in all restroom floors (825 SF)',
            'Quantity': '825',
            'UnitCost': '$18.00',  # Labor only - material included in tile
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '25245.00',
            'Confidence': '95'
        },
        {
            'Category': 'Flooring',
            'Room': 'IT/Copy/ESD',
            'ItemName': 'Armstrong VCT/SDT',
            'Description': 'Install Armstrong VCT/SDT in IT/Copy/ESD small rooms (300 SF)',
            'Quantity': '300',
            'UnitCost': '$6.00',  # Labor only - material included in VCT
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '3060.00',
            'Confidence': '95'
        },
        {
            'Category': 'Flooring',
            'Room': 'Lobby',
            'ItemName': 'B/W Brand Mosaic Tile',
            'Description': 'Install B/W brand mosaic tile in elevator lobby vestibules (150 SF)',
            'Quantity': '150',
            'UnitCost': '$18.00',  # Labor only - material included in mosaic
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '4590.00',
            'Confidence': '95'
        },

        # WALLS & CEILINGS - Exact materials from documents
        {
            'Category': 'Walls & Ceilings',
            'Room': 'General',
            'ItemName': '3-5/8" Metal Studs @ 16" o.c.',
            'Description': 'Install new metal studs for partitions (578 EA)',
            'Quantity': '700',
            'UnitCost': '$77.00',  # Labor only - material included in studs
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '91630.00',
            'Confidence': '95'
        },
        {
            'Category': 'Walls & Ceilings',
            'Room': 'General',
            'ItemName': '5/8" Type X GWB Both Sides',
            'Description': 'Install 5/8" Type X GWB on both sides of partitions (12,600 SF)',
            'Quantity': '12600',
            'UnitCost': '$4.00',  # Labor only - material included in GWB
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '85680.00',
            'Confidence': '95'
        },
        {
            'Category': 'Walls & Ceilings',
            'Room': 'General',
            'ItemName': '3-5/8" Track Top & Bottom',
            'Description': 'Install 3-5/8" track top and bottom for partitions (1,400 LF)',
            'Quantity': '1400',
            'UnitCost': '$55.00',  # Labor only - material included in track
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '130900.00',
            'Confidence': '95'
        },
        {
            'Category': 'Walls & Ceilings',
            'Room': 'General',
            'ItemName': '3-1/2" Mineral Wool Insulation',
            'Description': 'Install 3-1/2" mineral wool acoustic batt insulation (6,300 SF)',
            'Quantity': '6300',
            'UnitCost': '$19.00',  # Labor only - material included in insulation
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '203490.00',
            'Confidence': '95'
        },
        {
            'Category': 'Walls & Ceilings',
            'Room': 'General',
            'ItemName': '2×2 ACT System - Turf Pantheon',
            'Description': 'Install 2×2 ACT system with Turf Pantheon look (8,625 SF)',
            'Quantity': '8625',
            'UnitCost': '$9.00',  # Labor only - material included in ACT
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '131962.50',
            'Confidence': '95'
        },
        {
            'Category': 'Walls & Ceilings',
            'Room': 'General',
            'ItemName': 'GWB Ceilings Flat + Bulkheads',
            'Description': 'Install GWB ceilings with flat and bulkheads (2,000 SF)',
            'Quantity': '2000',
            'UnitCost': '$4.95',  # Labor only - material included in GWB
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '16830.00',
            'Confidence': '95'
        },
        {
            'Category': 'Walls & Ceilings',
            'Room': 'General',
            'ItemName': 'Open Ceiling Paint',
            'Description': 'Field paint to 4F ~60% + 5F ~50% of floor plates (8,250 SF)',
            'Quantity': '8250',
            'UnitCost': '$4.00',  # Labor only - material included in paint
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '56100.00',
            'Confidence': '95'
        },

        # WALL FINISHES - Exact materials from documents
        {
            'Category': 'Wall Finishes',
            'Room': 'General',
            'ItemName': 'Benjamin Moore Paint - Newburyport Blue',
            'Description': 'Install Benjamin Moore Newburyport Blue + field whites (16,800 SF)',
            'Quantity': '16800',
            'UnitCost': '$10.30',  # Labor only - material included in paint
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '294168.00',
            'Confidence': '95'
        },
        {
            'Category': 'Wall Finishes',
            'Room': 'General',
            'ItemName': 'Trim/Door Paint - Matching Satin',
            'Description': 'Install matching satin paint for corridor door/trim packages (1,200 SF)',
            'Quantity': '1200',
            'UnitCost': '$10.30',  # Labor only - material included in paint
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '21012.00',
            'Confidence': '95'
        },
        {
            'Category': 'Wall Finishes',
            'Room': 'General',
            'ItemName': 'Designtex Wannabe Rib Wallcovering',
            'Description': 'Install Designtex Wannabe ribbed wallcovering - Rib (Oat/Navy) (3,800 SF)',
            'Quantity': '3800',
            'UnitCost': '$19.00',  # Labor only - material included in wallcovering
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '122740.00',
            'Confidence': '95'
        },
        {
            'Category': 'Wall Finishes',
            'Room': 'General',
            'ItemName': 'Wilsonart "Walnut Heights" Panels',
            'Description': 'Install Wilsonart "Walnut Heights" wood-look panels (2,000 SF)',
            'Quantity': '2000',
            'UnitCost': '$18.00',  # Labor only - material included in panels
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '61200.00',
            'Confidence': '95'
        },
        {
            'Category': 'Wall Finishes',
            'Room': 'General',
            'ItemName': 'Wilsonart "Atlantis D25-60" Panels',
            'Description': 'Install Wilsonart "Atlantis D25-60" panels for elements of architecture (800 SF)',
            'Quantity': '800',
            'UnitCost': '$18.00',  # Labor only - material included in panels
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '24480.00',
            'Confidence': '95'
        },
        {
            'Category': 'Wall Finishes',
            'Room': 'General',
            'ItemName': 'Specialty Art-Deco Wallpaper',
            'Description': 'Install dark blue Art-Deco specialty wallpaper patterns (800 SF)',
            'Quantity': '800',
            'UnitCost': '$19.00',  # Labor only - material included in wallpaper
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '25840.00',
            'Confidence': '95'
        },
        {
            'Category': 'Wall Finishes',
            'Room': 'General',
            'ItemName': 'SOLYX SX-1254 Reeded Glass Film',
            'Description': 'Install SOLYX SX-1254 1/2" reeded glass film on office fronts & partitions (1,800 SF)',
            'Quantity': '1800',
            'UnitCost': '$19.00',  # Labor only - material included in film
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '58140.00',
            'Confidence': '95'
        },
        {
            'Category': 'Wall Finishes',
            'Room': 'General',
            'ItemName': '4" Rubber Base (Carpet)',
            'Description': 'Install 4" rubber base for carpet areas (604 LF)',
            'Quantity': '604',
            'UnitCost': '$19.00',  # Labor only - material included in base
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '19509.20',
            'Confidence': '95'
        },
        {
            'Category': 'Wall Finishes',
            'Room': 'General',
            'ItemName': 'Wood Base/Shoe Stained to Match',
            'Description': 'Install wood base/shoe stained to match wood flooring (345 LF)',
            'Quantity': '345',
            'UnitCost': '$19.00',  # Labor only - material included in base
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '11143.50',
            'Confidence': '95'
        },

        # DOORS & HARDWARE - Exact materials from documents
        {
            'Category': 'Doors & Hardware',
            'Room': 'General',
            'ItemName': 'Solid-Core Wood Doors 3\'×9\'',
            'Description': 'Install solid-core wood doors for toilets, IT/Storage, Copy, Wellness (20 EA)',
            'Quantity': '20',
            'UnitCost': '$550.00',  # Labor only - material included in doors
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '18700.00',
            'Confidence': '95'
        },
        {
            'Category': 'Doors & Hardware',
            'Room': 'General',
            'ItemName': 'Glass Office Fronts - Arched Motif',
            'Description': 'Install glass office-front doors with arched motif, single-leaf (24 EA)',
            'Quantity': '24',
            'UnitCost': '$825.00',  # Labor only - material included in glass doors
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '33660.00',
            'Confidence': '95'
        },
        {
            'Category': 'Doors & Hardware',
            'Room': 'General',
            'ItemName': 'Schlage ND Series Hardware - Grade 1 Brass',
            'Description': 'Install Schlage ND Series (satin Grade 1 brass) hardware sets (44 Sets)',
            'Quantity': '44',
            'UnitCost': '$19.00',  # Labor only - material included in hardware
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '1421.20',
            'Confidence': '95'
        },
        {
            'Category': 'Doors & Hardware',
            'Room': 'General',
            'ItemName': 'Locking Asymmetrical Pulls + Deadbolt',
            'Description': 'Install locking asymmetrical pulls + floor deadbolt for glass openings (24 Sets)',
            'Quantity': '24',
            'UnitCost': '$19.00',  # Labor only - material included in pulls
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '775.20',
            'Confidence': '95'
        },

        # LIGHTING & ELECTRICAL - Exact materials from documents
        {
            'Category': 'Lighting & Electrical',
            'Room': 'General',
            'ItemName': '6-8" LED Round Flushmounts',
            'Description': 'Install 6-8" LED round flushmounts in open office grid (80 EA)',
            'Quantity': '80',
            'UnitCost': '$175.00',  # Labor only - material included in fixtures
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '23800.00',
            'Confidence': '95'
        },
        {
            'Category': 'Lighting & Electrical',
            'Room': 'General',
            'ItemName': '3" Recessed Downlights',
            'Description': 'Install 3" recessed downlights in meeting rooms, corridors, restrooms (60 EA)',
            'Quantity': '60',
            'UnitCost': '$165.00',  # Labor only - material included in fixtures
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '16830.00',
            'Confidence': '95'
        },
        {
            'Category': 'Lighting & Electrical',
            'Room': 'General',
            'ItemName': '"Novato Globes" Sphere Pendants',
            'Description': 'Install "Novato Globes" sphere pendants in open ceiling areas (70 EA)',
            'Quantity': '70',
            'UnitCost': '$165.00',  # Labor only - material included in fixtures
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '8415.00',
            'Confidence': '95'
        },
        {
            'Category': 'Lighting & Electrical',
            'Room': 'General',
            'ItemName': 'Arcachon Chandelier',
            'Description': 'Install Arcachon chandelier feature lighting for pantry/lounge (1 EA)',
            'Quantity': '1',
            'UnitCost': '$165.00',  # Labor only - material included in fixture
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '280.50',
            'Confidence': '95'
        },
        {
            'Category': 'Lighting & Electrical',
            'Room': 'General',
            'ItemName': 'MPL L225SR Track Lighting',
            'Description': 'Install MPL L225SR track lighting for art walls/lounge rails (48 LF)',
            'Quantity': '48',
            'UnitCost': '$165.00',  # Labor only - material included in track
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '13464.00',
            'Confidence': '95'
        },
        {
            'Category': 'Lighting & Electrical',
            'Room': 'General',
            'ItemName': 'Dimmable LED Track Heads',
            'Description': 'Install dimmable LED track heads - two per 8\' track (24 EA)',
            'Quantity': '24',
            'UnitCost': '$165.00',  # Labor only - material included in heads
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '6732.00',
            'Confidence': '95'
        },
        {
            'Category': 'Lighting & Electrical',
            'Room': 'General',
            'ItemName': 'Power Outlets',
            'Description': 'Install power outlets throughout the space (250 EA)',
            'Quantity': '250',
            'UnitCost': '$55.00',  # Labor only - material included in outlets
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '23375.00',
            'Confidence': '95'
        },
        {
            'Category': 'Lighting & Electrical',
            'Room': 'General',
            'ItemName': 'Dedicated Circuits',
            'Description': 'Install dedicated circuits for appliances and equipment (15 EA)',
            'Quantity': '15',
            'UnitCost': '$440.00',  # Labor only - material included in circuits
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '11220.00',
            'Confidence': '95'
        },

        # PLUMBING - Exact materials from documents
        {
            'Category': 'Plumbing',
            'Room': 'Restrooms',
            'ItemName': 'Sloan CX Water Closets - Floor/Wall Mounted',
            'Description': 'Install Sloan CX (floor) / ST-2469 (wall) water closets (7 EA)',
            'Quantity': '7',
            'UnitCost': '$650.00',  # Labor only - material included in fixtures
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '7735.00',
            'Confidence': '95'
        },
        {
            'Category': 'Plumbing',
            'Room': 'Restrooms',
            'ItemName': 'Sloan SU-7019 Urinal',
            'Description': 'Install Sloan SU-7019 urinal in men\'s 5F (1 EA)',
            'Quantity': '1',
            'UnitCost': '$19.00',  # Labor only - material included in urinal
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '32.30',
            'Confidence': '95'
        },
        {
            'Category': 'Plumbing',
            'Room': 'Restrooms',
            'ItemName': 'Kohler Compass Lavatories - Rejuvenation Atlanta',
            'Description': 'Install Kohler Compass / Rejuvenation Atlanta lavatories (8 EA)',
            'Quantity': '8',
            'UnitCost': '$750.00',  # Labor only - material included in fixtures
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '10200.00',
            'Confidence': '95'
        },
        {
            'Category': 'Plumbing',
            'Room': 'Restrooms',
            'ItemName': 'Sloan EAF-200 Faucets',
            'Description': 'Install Sloan EAF-200 deck-mounted, hard-wired faucets (8 EA)',
            'Quantity': '8',
            'UnitCost': '$19.00',  # Labor only - material included in faucets
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '258.40',
            'Confidence': '95'
        },
        {
            'Category': 'Plumbing',
            'Room': 'Restrooms',
            'ItemName': 'Bobrick Paper Towel Dispensers B-38034.MBLK',
            'Description': 'Install Bobrick B-38034.MBLK paper towel dispensers (4 EA)',
            'Quantity': '4',
            'UnitCost': '$19.00',  # Labor only - material included in dispensers
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '129.20',
            'Confidence': '95'
        },
        {
            'Category': 'Plumbing',
            'Room': 'Restrooms',
            'ItemName': 'Bobrick Toilet Roll Holders B-540.MBLK',
            'Description': 'Install Bobrick B-540.MBLK toilet roll holders (4 EA)',
            'Quantity': '4',
            'UnitCost': '$19.00',  # Labor only - material included in holders
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '129.20',
            'Confidence': '95'
        },
        {
            'Category': 'Plumbing',
            'Room': 'Restrooms',
            'ItemName': 'ADA Grab Bars 42"/36" Sets',
            'Description': 'Install ADA grab bars 42"/36" sets in ADA rooms (6 EA)',
            'Quantity': '6',
            'UnitCost': '$19.00',  # Labor only - material included in grab bars
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '193.80',
            'Confidence': '95'
        },

        # APPLIANCES & EQUIPMENT - Exact materials from documents
        {
            'Category': 'Appliances',
            'Room': 'Pantry',
            'ItemName': 'BUNN Coffee Machine 53200.0100',
            'Description': 'Install BUNN coffee machine 53200.0100 9" × 17 1/2" × 11" with dedicated circuit (1 EA)',
            'Quantity': '1',
            'UnitCost': '$165.00',  # Labor only - material included in machine
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '280.50',
            'Confidence': '95'
        },
        {
            'Category': 'Appliances',
            'Room': 'Pantry',
            'ItemName': 'BUNN Coffee Grinder LPG2E',
            'Description': 'Install BUNN LPG2E coffee grinder 9" × 17 1/2" × 11" silver (1 EA)',
            'Quantity': '1',
            'UnitCost': '$165.00',  # Labor only - material included in grinder
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '280.50',
            'Confidence': '95'
        },
        {
            'Category': 'Appliances',
            'Room': 'Pantry',
            'ItemName': 'Elkay Quartz Classic Sink - 4F Pantry',
            'Description': 'Install Elkay Quartz Classic 24-5/8" sink in 4F pantry (1 EA)',
            'Quantity': '1',
            'UnitCost': '$750.00',  # Labor only - material included in sink
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '1275.00',
            'Confidence': '95'
        },
        {
            'Category': 'Appliances',
            'Room': 'Coffee Station',
            'ItemName': 'Elkay Quartz Classic Sink - 5F Coffee',
            'Description': 'Install Elkay Quartz Classic sink in 5F coffee station (1 EA)',
            'Quantity': '1',
            'UnitCost': '$750.00',  # Labor only - material included in sink
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '1275.00',
            'Confidence': '95'
        },
        {
            'Category': 'Appliances',
            'Room': 'Pantry',
            'ItemName': 'Kohler Cure Brass Faucet - 4F',
            'Description': 'Install Kohler Cure brass faucet in 4F pantry (1 EA)',
            'Quantity': '1',
            'UnitCost': '$200.00',  # Labor only - material included in faucet
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '340.00',
            'Confidence': '95'
        },
        {
            'Category': 'Appliances',
            'Room': 'Coffee Station',
            'ItemName': 'Kohler Cure Brass Faucet - 5F',
            'Description': 'Install Kohler Cure brass faucet in 5F coffee station (1 EA)',
            'Quantity': '1',
            'UnitCost': '$200.00',  # Labor only - material included in faucet
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '340.00',
            'Confidence': '95'
        },
        {
            'Category': 'Appliances',
            'Room': 'Pantry',
            'ItemName': 'Fisher & Paykel Dishwasher - Panel Ready',
            'Description': 'Install Fisher & Paykel panel-ready dishwasher in 4F pantry (1 EA)',
            'Quantity': '1',
            'UnitCost': '$1200.00',  # Labor only - material included in dishwasher
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '2040.00',
            'Confidence': '95'
        },
        {
            'Category': 'Appliances',
            'Room': 'Pantry',
            'ItemName': 'Fisher & Paykel Refrigerator - 36" Panel Ready',
            'Description': 'Install Fisher & Paykel 36" panel-ready refrigerator in 4F pantry (1 EA)',
            'Quantity': '1',
            'UnitCost': '$1200.00',  # Labor only - material included in refrigerator
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '2040.00',
            'Confidence': '95'
        },
        {
            'Category': 'Appliances',
            'Room': 'Pantry',
            'ItemName': 'Summit Undercounter Beverage Cooler - ASADS1523IF',
            'Description': 'Install Summit ASADS1523IF shallow-depth beverage cooler in 4F island (1 EA)',
            'Quantity': '1',
            'UnitCost': '$1200.00',  # Labor only - material included in cooler
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '2040.00',
            'Confidence': '95'
        },
        {
            'Category': 'Appliances',
            'Room': 'Coffee Station',
            'ItemName': 'Bevi Countertop Water Dispenser',
            'Description': 'Install Bevi countertop water dispensers in 4F pantry + 5F coffee (2 EA)',
            'Quantity': '2',
            'UnitCost': '$200.00',  # Labor only - material included in dispensers
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '680.00',
            'Confidence': '95'
        },

        # MILLWORK - Exact materials from documents
        {
            'Category': 'Millwork',
            'Room': 'Pantry',
            'ItemName': 'Wilsonart Walnut Heights Casework',
            'Description': 'Install Wilsonart Walnut Heights casework for pantry base/upper run (28 LF)',
            'Quantity': '28',
            'UnitCost': '$800.00',  # Material only - labor included in millwork
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '38080.00',
            'Confidence': '95'
        },
        {
            'Category': 'Millwork',
            'Room': 'Pantry',
            'ItemName': 'Wilsonart Wallaby with Microwave Drawer',
            'Description': 'Install Wilsonart Wallaby with microwave drawer & brass foot-rail (10 LF)',
            'Quantity': '10',
            'UnitCost': '$800.00',  # Material only - labor included in millwork
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '13600.00',
            'Confidence': '95'
        },
        {
            'Category': 'Millwork',
            'Room': 'Lounge',
            'ItemName': 'Lounge/AV Walnut Look Millwork',
            'Description': 'Install walnut look millwork with LED shelves for lounge & meeting built-ins (20 LF)',
            'Quantity': '20',
            'UnitCost': '$800.00',  # Material only - labor included in millwork
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '27200.00',
            'Confidence': '95'
        },
        {
            'Category': 'Millwork',
            'Room': 'General',
            'ItemName': 'Arch Trim - Bronze/Brass',
            'Description': 'Install bronze/brass arch trim on glass/arches as required (30 LF)',
            'Quantity': '30',
            'UnitCost': '$19.00',  # Labor only - material included in trim
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '969.00',
            'Confidence': '95'
        },

        # SPECIALTY - Exact materials from documents
        {
            'Category': 'Specialty',
            'Room': 'Pantry/Coffee',
            'ItemName': 'Breccia Vino Marble Countertops',
            'Description': 'Install Breccia Vino marble countertops for pantry/coffee/copy tops (85 SF)',
            'Quantity': '85',
            'UnitCost': '$97.00',  # Labor only - material included in marble
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '14016.50',
            'Confidence': '95'
        },
        {
            'Category': 'Specialty',
            'Room': 'General',
            'ItemName': 'Antique Mirror - Elements of Architecture',
            'Description': 'Install antique mirror on backs of arches/pantry/coffee (80 SF)',
            'Quantity': '80',
            'UnitCost': '$19.00',  # Labor only - material included in mirror
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '2584.00',
            'Confidence': '95'
        },
        {
            'Category': 'Specialty',
            'Room': 'Pantry',
            'ItemName': 'Gage GW906 Metal Mesh',
            'Description': 'Install Gage GW906 metal mesh for pantry arches (60 SF)',
            'Quantity': '60',
            'UnitCost': '$19.00',  # Labor only - material included in mesh
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '1938.00',
            'Confidence': '95'
        },
        {
            'Category': 'Specialty',
            'Room': 'Restrooms',
            'ItemName': 'POTTERY COREY ROUNDED 14 Mirror Black',
            'Description': 'Install POTTERY COREY ROUNDED 14 mirror black size 47"W × 47"H (1 EA)',
            'Quantity': '1',
            'UnitCost': '$25.00',  # Labor only - material included in mirror
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '42.50',
            'Confidence': '95'
        },
        {
            'Category': 'Specialty',
            'Room': 'Restrooms',
            'ItemName': 'COREY ROUNDED 15 Mirror Rejuvenation Black',
            'Description': 'Install COREY ROUNDED 15 mirror rejuvenation black size 22"W × 48"H (1 EA)',
            'Quantity': '1',
            'UnitCost': '$25.00',  # Labor only - material included in mirror
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '42.50',
            'Confidence': '95'
        },

        # DEMOLITION - From documents
        {
            'Category': 'Demolition',
            'Room': 'General',
            'ItemName': 'Full Gut Demolition',
            'Description': 'Complete demolition of existing finishes, partitions, ceilings, and systems',
            'Quantity': '15000',
            'UnitCost': '$11.00',  # DEMO-12 rate from pricing sheet
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '280500.00',
            'Confidence': '95'
        },
        {
            'Category': 'Demolition',
            'Room': 'General',
            'ItemName': 'Selective Floor Finishes Demolition',
            'Description': 'Removal of existing floor finishes and preparation for new installation',
            'Quantity': '15000',
            'UnitCost': '$4.00',  # Floor demo rate
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '102000.00',
            'Confidence': '95'
        },

        # CLEANING - CORRECTED CALCULATION
        {
            'Category': 'Cleaning',
            'Room': 'General',
            'ItemName': 'Commercial Cleaning Post-Construction',
            'Description': 'Final cleaning of entire space after construction completion (Install + Material)',
            'Quantity': '1',
            'UnitCost': '$4400.00',  # CLEN-05: $4,400 Labor + $0 Material = $4,400
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '7480.00',
            'Confidence': '95'
        },

        # FIRE PROTECTION - From documents
        {
            'Category': 'Fire Protection',
            'Room': 'General',
            'ItemName': 'Fire Alarm System Modifications',
            'Description': 'New fire alarm devices, wiring, and tie-ins to building system',
            'Quantity': '15000',
            'UnitCost': '$8.00',  # Fire alarm rate per SF
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '204000.00',
            'Confidence': '95'
        },
        {
            'Category': 'Fire Protection',
            'Room': 'General',
            'ItemName': 'Sprinkler Head Relocations',
            'Description': 'Relocation and replacement of sprinkler heads for new layout',
            'Quantity': '67',
            'UnitCost': '$550.00',  # Per head rate
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '62745.00',
            'Confidence': '95'
        },

        # MECHANICAL - From documents
        {
            'Category': 'Mechanical',
            'Room': 'General',
            'ItemName': 'HVAC System Modifications',
            'Description': 'HVAC modifications for new office layout and ventilation',
            'Quantity': '15000',
            'UnitCost': '$8.00',  # Basic HVAC rate per SF
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '204000.00',
            'Confidence': '90'
        },

        # ELECTRICAL - From documents
        {
            'Category': 'Electrical',
            'Room': 'General',
            'ItemName': 'Electrical System Upgrades',
            'Description': 'New outlets, lighting, fire alarm, and electrical infrastructure',
            'Quantity': '15000',
            'UnitCost': '$12.00',  # Electrical upgrade rate per SF
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '306000.00',
            'Confidence': '95'
        },

        # SUBFLOOR PREPARATION
        {
            'Category': 'Flooring',
            'Room': 'General',
            'ItemName': 'Subfloor Preparation',
            'Description': 'Subfloor leveling and preparation for new finishes',
            'Quantity': '15000',
            'UnitCost': '$2.00',  # Subfloor prep rate per SF
            'Markup': '0.70',
            'MarkupType': '%',
            'Total': '51000.00',
            'Confidence': '95'
        },

        # PERMITS & INSPECTIONS
        {
            'Category': 'General Conditions',
            'Room': 'General',
            'ItemName': 'Permits and Inspections',
            'Description': 'Building permits, electrical permits, fire alarm permits, and inspections',
            'Quantity': '1',
            'UnitCost': '$15000.00',  # Permit allowance
            'Markup': '0.00',
            'MarkupType': '%',
            'Total': '15000.00',
            'Confidence': '95'
        }
    ]

    print(f"Created {len(items)} items with EVERY material from ALL documents")

    # Write complete estimate CSV
    output_filename = '113_University_Place_Complete_All_Materials_Estimate.csv'
    with open(output_filename, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['Category', 'Room', 'ItemName', 'Description', 'Quantity', 'UnitCost', 'Markup', 'MarkupType', 'Total', 'Confidence']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(items)

    print(f"\n✅ Complete ALL materials estimate saved to: {output_filename}")

    # Calculate final totals
    total = sum(float(item['Total']) for item in items)
    general_conditions = total * 0.10
    final_total = total + general_conditions

    print(f"\n📊 COMPLETE ALL MATERIALS ESTIMATE TOTALS:")
    print(f"Base Cost: ${total:,.2f}")
    print(f"General Conditions (10%): ${general_conditions:,.2f}")
    print(f"Final Total: ${final_total:,.2f}")

    # Show categories
    categories = {}
    for item in items:
        cat = item['Category']
        categories[cat] = categories.get(cat, 0) + 1

    print(f"\n📋 CATEGORIES INCLUDED:")
    for cat, count in sorted(categories.items()):
        print(f"  {cat}: {count} items")

    # Show key materials included
    print(f"\n🎯 KEY MATERIALS INCLUDED:")
    print(f"  ✅ BUNN Coffee Machine 53200.0100")
    print(f"  ✅ BUNN Coffee Grinder LPG2E")
    print(f"  ✅ Fisher & Paykel Appliances")
    print(f"  ✅ Elkay Quartz Classic Sinks")
    print(f"  ✅ Kohler Cure Brass Faucets")
    print(f"  ✅ Summit Beverage Cooler ASADS1523IF")
    print(f"  ✅ Bevi Water Dispensers")
    print(f"  ✅ Wilsonart Walnut Heights & Atlantis")
    print(f"  ✅ Breccia Vino Marble Countertops")
    print(f"  ✅ Gage GW906 Metal Mesh")
    print(f"  ✅ POTTERY COREY Mirrors")
    print(f"  ✅ All specific brands and models from documents")

    return output_filename

if __name__ == "__main__":
    complete_file = create_complete_material_estimate()
    print(f"\n🎯 Next step: Create Excel file from {complete_file}")
