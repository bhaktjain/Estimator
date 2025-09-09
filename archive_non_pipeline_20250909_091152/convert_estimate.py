#!/usr/bin/env python3
import json
import csv
import os

def convert_json_to_csv(json_file, output_csv):
    """Convert the JSON estimate output to CSV format for comprehensive cleanup."""
    
    # Read the JSON file
    with open(json_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract JSON content (remove markdown formatting)
    json_start = content.find('{')
    json_end = content.rfind('}') + 1
    json_content = content[json_start:json_end]
    
    # Parse JSON
    try:
        data = json.loads(json_content)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return
    
    # Convert to the format expected by comprehensive cleanup
    items = []
    
    for category, details in data.items():
        item = {
            'Category': category,
            'Room': 'Floors 4 & 5',  # From the PDF
            'ItemName': details.get('description', '').split('.')[0][:50],  # First sentence
            'Description': details.get('description', ''),
            'Quantity': str(details.get('quantity', '')),
            'UnitCost': f"${details.get('subtotal', 0) / details.get('quantity', 1):.2f}" if details.get('quantity', 0) > 0 else f"${details.get('subtotal', 0):.2f}",
            'Markup': '0.75',  # Standard markup
            'MarkupType': '%',
            'Total': f"${details.get('subtotal', 0):.2f}",
            'Confidence': '85'  # High confidence based on detailed takeoff
        }
        items.append(item)
    
    # Write CSV
    with open(output_csv, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['Category', 'Room', 'ItemName', 'Description', 'Quantity', 'UnitCost', 'Markup', 'MarkupType', 'Total', 'Confidence']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(items)
    
    print(f"Converted {len(items)} items to {output_csv}")
    
    # Calculate totals
    total_cost = sum(float(item['Total'].replace('$', '')) for item in items)
    print(f"Total estimated cost: ${total_cost:,.2f}")
    
    return items

if __name__ == "__main__":
    # Convert the estimate
    items = convert_json_to_csv('estimate_output.txt', '113_university_place_estimate.csv')
    
    if items:
        print("\nEstimate Summary:")
        print("=" * 80)
        for item in items:
            print(f"{item['Category']:20} | {item['Quantity']:>8} {item['UnitCost']:>10} | {item['Total']:>10}")
        print("=" * 80)
        total = sum(float(item['Total'].replace('$', '')) for item in items)
        print(f"{'TOTAL':20} | {'':>8} {'':>10} | ${total:>9,.2f}")

