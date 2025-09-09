#!/usr/bin/env python3
"""
Process ChatGPT response and convert to CSV format
"""
import json
import csv
import re

def process_chatgpt_response():
    """Process the ChatGPT response and convert to CSV."""
    
    print("🔧 PROCESSING CHATGPT RESPONSE")
    print("=" * 50)
    
    # Read the ChatGPT response
    with open('comprehensive_estimate_chatgpt_response.txt', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract JSON from the response (remove markdown formatting)
    json_match = re.search(r'```json\s*(\[.*?\])\s*```', content, re.DOTALL)
    if json_match:
        json_str = json_match.group(1)
    else:
        # Try to find JSON array without markdown
        json_match = re.search(r'(\[.*\])', content, re.DOTALL)
        if json_match:
            json_str = json_match.group(1)
        else:
            print("❌ Could not extract JSON from response")
            return
    
    try:
        # Parse JSON
        items = json.loads(json_str)
        print(f"✅ Successfully parsed {len(items)} items from ChatGPT response")
        
        # Convert to CSV
        output_filename = '113_University_Place_ChatGPT_Response.csv'
        with open(output_filename, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['Category', 'Room', 'ItemName', 'Description', 'Quantity', 'UnitCost', 'Markup', 'MarkupType', 'Total', 'Confidence']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for item in items:
                # Ensure UnitCost is formatted as currency
                if isinstance(item['UnitCost'], (int, float)):
                    item['UnitCost'] = f"${item['UnitCost']:.2f}"
                
                # Ensure Total is formatted as currency
                if isinstance(item['Total'], (int, float)):
                    item['Total'] = f"{item['Total']:.2f}"
                
                writer.writerow(item)
        
        print(f"✅ CSV saved to: {output_filename}")
        
        # Show summary
        print(f"\n📊 CHATGPT RESPONSE SUMMARY:")
        print(f"Total items: {len(items)}")
        
        categories = {}
        for item in items:
            cat = item['Category']
            categories[cat] = categories.get(cat, 0) + 1
        
        print(f"Categories: {', '.join([f'{cat}: {count}' for cat, count in categories.items()])}")
        
        # Calculate totals
        total = sum(float(str(item['Total']).replace('$', '')) for item in items)
        print(f"Total estimate: ${total:,.2f}")
        
        return output_filename
        
    except json.JSONDecodeError as e:
        print(f"❌ JSON parsing error: {e}")
        print("Raw content:")
        print(content)
        return None
    except Exception as e:
        print(f"❌ Error processing response: {e}")
        return None

if __name__ == "__main__":
    csv_file = process_chatgpt_response()
    if csv_file:
        print(f"\n🎯 Next step: Verify and improve the estimate with actual takeoff data")

