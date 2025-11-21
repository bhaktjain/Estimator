#!/usr/bin/env python3
"""
Diagnostic script to check chunk output files
"""
import os
import sys
import json

def diagnose_chunk_file(filepath):
    """Diagnose a single chunk output file"""
    print(f"\n{'='*60}")
    print(f"Diagnosing: {filepath}")
    print(f"{'='*60}")
    
    if not os.path.exists(filepath):
        print("❌ File does not exist")
        return
    
    # Check file size
    size = os.path.getsize(filepath)
    print(f"File size: {size} bytes")
    
    if size == 0:
        print("❌ File is empty")
        return
    
    # Read content
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"Content length: {len(content)} characters")
    print(f"\nFirst 500 characters:")
    print("-" * 60)
    print(content[:500])
    print("-" * 60)
    
    # Check for JSON
    if '```json' in content:
        print("\n✅ Found ```json marker")
        
        # Extract JSON
        try:
            start = content.find('```json') + 7
            end = content.find('```', start)
            if end == -1:
                print("❌ No closing ``` found")
                return
            
            json_str = content[start:end].strip()
            print(f"\nExtracted JSON length: {len(json_str)} characters")
            
            # Try to parse
            try:
                data = json.loads(json_str)
                print("✅ JSON is valid")
                
                # Check structure
                if 'sections' in data:
                    print(f"✅ Has 'sections' key")
                    print(f"   Number of sections: {len(data['sections'])}")
                    
                    total_items = 0
                    for section in data['sections']:
                        if 'items' in section:
                            total_items += len(section['items'])
                    
                    print(f"   Total items: {total_items}")
                    
                    if total_items == 0:
                        print("❌ No items found in sections")
                    else:
                        print("✅ Items found!")
                        
                        # Show first item
                        for section in data['sections']:
                            if section.get('items'):
                                first_item = section['items'][0]
                                print(f"\nFirst item example:")
                                print(f"  Room: {first_item.get('room', 'N/A')}")
                                print(f"  Scope: {first_item.get('scope_item', 'N/A')}")
                                print(f"  Quantity: {first_item.get('quantity', 'N/A')}")
                                print(f"  Subtotal: {first_item.get('subtotal', 'N/A')}")
                                break
                else:
                    print("❌ No 'sections' key in JSON")
                    print(f"   Keys found: {list(data.keys())}")
                    
            except json.JSONDecodeError as e:
                print(f"❌ JSON parse error: {e}")
                print(f"\nJSON content (first 200 chars):")
                print(json_str[:200])
                
        except Exception as e:
            print(f"❌ Error extracting JSON: {e}")
    else:
        print("\n❌ No ```json marker found")
        
        # Check for refusal patterns
        refusal_patterns = [
            "cannot provide",
            "unable to provide",
            "I cannot",
            "I'm unable",
            "not able to",
            "insufficient information"
        ]
        
        content_lower = content.lower()
        for pattern in refusal_patterns:
            if pattern in content_lower:
                print(f"⚠️  Found refusal pattern: '{pattern}'")
                # Show context
                idx = content_lower.find(pattern)
                context_start = max(0, idx - 50)
                context_end = min(len(content), idx + 100)
                print(f"   Context: ...{content[context_start:context_end]}...")
                break

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 diagnose_chunk_outputs.py <run_directory>")
        print("Example: python3 diagnose_chunk_outputs.py chunked_outputs/run_20251121_022658_965b12d3")
        sys.exit(1)
    
    run_dir = sys.argv[1]
    
    if not os.path.exists(run_dir):
        print(f"❌ Directory not found: {run_dir}")
        sys.exit(1)
    
    # Find all chunk output files
    chunk_files = sorted([
        f for f in os.listdir(run_dir)
        if f.startswith('estimate_output_chunk_') and f.endswith('.txt')
    ])
    
    if not chunk_files:
        print(f"❌ No chunk output files found in {run_dir}")
        sys.exit(1)
    
    print(f"Found {len(chunk_files)} chunk output files")
    
    # Diagnose each file
    for chunk_file in chunk_files:
        filepath = os.path.join(run_dir, chunk_file)
        diagnose_chunk_file(filepath)
    
    print(f"\n{'='*60}")
    print("Diagnosis complete")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
