#!/usr/bin/env python3
import json
import csv
import os
import openai
from collections import defaultdict

def create_deduplication_prompt(items):
    """Create a prompt for GPT to deduplicate and select best unique scopes."""
    
    # Group items by category
    categories = defaultdict(list)
    for item in items:
        category = item.get('Category', '').strip()
        if category:
            categories[category].append(item)
    
    prompt = """You are a professional renovation estimator. Review the following items and select the BEST UNIQUE scope items for each section, removing duplicates and overlapping work.

## DEDUPLICATION RULES:
1. **Remove Duplicates**: Items with same name, room, and similar scope
2. **Remove Overlapping**: Items that cover the same work in different ways
3. **Keep Best Quality**: When duplicates exist, keep the one with:
   - Higher confidence score
   - More detailed description
   - Better pricing accuracy
   - More specific scope
4. **Ensure Uniqueness**: Each item should represent distinct work
5. **Maintain Coverage**: Don't remove items that cover different aspects

## OUTPUT FORMAT:
Provide a JSON response with this exact structure:
```json
{
  "sections": [
    {
      "name": "Section Name",
      "items": [
        {
          "room": "Room Name",
          "scope_item": "Item Name",
          "description": "Detailed description",
          "quantity": "X SF/LF/UNIT",
          "unit_cost": "$X per SF/LF/UNIT",
          "markup": "0.75",
          "subtotal": "Calculated total",
          "confidence_score": "85",
          "deduplication_notes": "Why this item was kept"
        }
      ]
    }
  ]
}
```

## ITEMS TO REVIEW:
"""
    
    for category, category_items in categories.items():
        prompt += f"\n### {category.upper()} SECTION:\n"
        for item in category_items:
            prompt += f"- **{item.get('ItemName', '')}** in {item.get('Room', '')}\n"
            prompt += f"  - Description: {item.get('Description', '')}\n"
            prompt += f"  - Quantity: {item.get('Quantity', '')}\n"
            prompt += f"  - Unit Cost: {item.get('UnitCost', '')}\n"
            prompt += f"  - Total: {item.get('Total', '')}\n"
            prompt += f"  - Confidence: {item.get('Confidence', '')}\n"
    
    prompt += """
## INSTRUCTIONS:
1. Review each section carefully
2. Remove duplicates and overlapping items
3. Keep the BEST item when duplicates exist
4. Ensure each item represents unique work
5. Maintain comprehensive coverage
6. Provide deduplication notes explaining your choices

Return only the JSON response with the cleaned, unique items for each section.
"""
    
    return prompt

def send_to_gpt_for_deduplication(items, api_key):
    """Send items to GPT for deduplication and return cleaned results."""
    
    prompt = create_deduplication_prompt(items)
    
    try:
        client = openai.OpenAI(api_key=api_key)
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional renovation estimator specializing in deduplication and scope optimization. Your task is to review renovation items and select the best unique scopes for each section."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.1,
            max_tokens=4000
        )
        
        # Extract JSON from response
        content = response.choices[0].message.content
        
        # Find JSON in the response
        start = content.find('{')
        end = content.rfind('}') + 1
        
        if start != -1 and end != 0:
            json_str = content[start:end]
            result = json.loads(json_str)
            return result
        else:
            print("[ERROR] No JSON found in GPT response")
            return None
            
    except Exception as e:
        print(f"[ERROR] GPT deduplication failed: {e}")
        return None

def convert_gpt_result_to_items(gpt_result):
    """Convert GPT deduplication result back to our item format."""
    
    items = []
    
    if 'sections' in gpt_result:
        for section in gpt_result['sections']:
            section_name = section.get('name', '')
            for item in section.get('items', []):
                csv_item = {
                    'Category': section_name,
                    'Room': item.get('room', ''),
                    'ItemName': item.get('scope_item', ''),
                    'Description': item.get('description', ''),
                    'Quantity': item.get('quantity', ''),
                    'UnitCost': item.get('unit_cost', ''),
                    'Markup': item.get('markup', ''),
                    'MarkupType': '%',
                    'Total': item.get('subtotal', ''),
                    'Confidence': item.get('confidence_score', ''),
                    'DeduplicationNotes': item.get('deduplication_notes', '')
                }
                items.append(csv_item)
    
    return items

def gpt_deduplication(items, api_key):
    """Perform GPT-based deduplication on items."""
    
    print(f"[INFO] Starting GPT-based deduplication on {len(items)} items")
    
    # Send to GPT for deduplication
    gpt_result = send_to_gpt_for_deduplication(items, api_key)
    
    if gpt_result:
        # Convert back to our format
        deduplicated_items = convert_gpt_result_to_items(gpt_result)
        print(f"[INFO] GPT deduplication completed: {len(items)} -> {len(deduplicated_items)} items")
        return deduplicated_items
    else:
        print("[WARNING] GPT deduplication failed, returning original items")
        return items

if __name__ == "__main__":
    # Test with sample data
    sample_items = [
        {
            'Category': 'Demolition',
            'Room': 'Kitchen',
            'ItemName': 'Kitchen Demolition',
            'Description': 'Full gut of kitchen area',
            'Quantity': '1 UNIT',
            'UnitCost': '$3,300',
            'Markup': '0.75',
            'Total': '5775',
            'Confidence': '95'
        },
        {
            'Category': 'Demolition',
            'Room': 'Kitchen',
            'ItemName': 'Kitchen Gut',
            'Description': 'Complete demolition of kitchen',
            'Quantity': '1 UNIT',
            'UnitCost': '$3,300',
            'Markup': '0.75',
            'Total': '5775',
            'Confidence': '90'
        }
    ]
    
    # You would need to set your API key
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key:
        result = gpt_deduplication(sample_items, api_key)
        print(f"Result: {len(result)} items")
    else:
        print("Please set OPENAI_API_KEY environment variable") 