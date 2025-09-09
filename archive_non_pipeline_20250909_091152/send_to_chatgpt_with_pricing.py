#!/usr/bin/env python3
"""
Send takeoff and master pricing sheet to ChatGPT for proper pricing
"""
import os
import subprocess
import json

def send_to_chatgpt_with_pricing():
    """Send both takeoff and pricing sheet to ChatGPT for proper estimate."""
    
    print("🚀 SENDING TAKEOFF + MASTER PRICING TO CHATGPT")
    print("=" * 60)
    
    # Combine all takeoff chunks
    takeoff_content = ""
    takeoff_dir = "pdf_analysis"
    for i in range(1, 8):  # We have chunks 1-7
        chunk_file = os.path.join(takeoff_dir, f"chunk_{i}.txt")
        if os.path.exists(chunk_file):
            with open(chunk_file, 'r', encoding='utf-8') as f:
                takeoff_content += f"\n\n--- CHUNK {i} ---\n"
                takeoff_content += f.read()
    
    # Combine all pricing sheet chunks
    pricing_content = ""
    pricing_dir = "master_pricing_analysis"
    for i in range(1, 26):  # We have chunks 1-25
        chunk_file = os.path.join(pricing_dir, f"chunk_{i}.txt")
        if os.path.exists(chunk_file):
            with open(chunk_file, 'r', encoding='utf-8') as f:
                pricing_content += f"\n\n--- PRICING SECTION {i} ---\n"
                pricing_content += f.read()
    
    # Create comprehensive prompt
    prompt = f"""
You are a professional construction estimator. I need you to create a detailed renovation estimate for a commercial office space renovation project.

PROJECT: 113 University Place - 2 Floor Commercial Office Renovation
SCOPE: Complete interior renovation including demolition, framing, drywall, ceilings, flooring, painting, electrical, plumbing, millwork, and finishes

I will provide you with:
1. DETAILED TAKEOFF with quantities and specifications
2. INTERNAL MASTER PRICING SHEET with our company's actual rates

REQUIREMENTS:
- Use ONLY the pricing from our internal master pricing sheet
- Apply the correct margins as specified in the pricing sheet
- Calculate totals correctly (quantity × unit cost × (1 + margin))
- Ensure all items from the takeoff are included
- Use the exact item descriptions and specifications from the takeoff
- Apply minimum pricing requirements where applicable

OUTPUT FORMAT:
Return a JSON object with this structure:
{{
  "items": [
    {{
      "Category": "Category Name",
      "Room": "Room/Location",
      "ItemName": "Brief Item Name",
      "Description": "Full description from takeoff",
      "Quantity": "Quantity from takeoff",
      "UnitCost": "Unit cost from pricing sheet",
      "Markup": "Margin from pricing sheet (as decimal)",
      "MarkupType": "%",
      "Total": "Calculated total with markup",
      "Confidence": "95"
    }}
  ]
}}

TAKEOFF CONTENT:
{takeoff_content}

MASTER PRICING SHEET:
{pricing_content}

IMPORTANT NOTES:
- Use the exact rates from our pricing sheet
- Apply the correct margins (50%, 65%, 70%, 80% as specified)
- Respect minimum pricing requirements
- For items not in pricing sheet, use reasonable market rates but note with lower confidence
- Ensure all calculations are mathematically correct
- Include all items from the takeoff

Please analyze both documents carefully and provide a comprehensive estimate using our internal pricing.
"""
    
    # Save the prompt to a file
    prompt_file = "comprehensive_estimate_prompt.txt"
    with open(prompt_file, 'w', encoding='utf-8') as f:
        f.write(prompt)
    
    print(f"✅ Created comprehensive prompt: {prompt_file}")
    print(f"📏 Takeoff content: {len(takeoff_content)} characters")
    print(f"💰 Pricing content: {len(pricing_content)} characters")
    
    # Now send to ChatGPT using our existing script
    print("\n🔄 Sending to ChatGPT...")
    
    # Use the existing send_files_to_chatgpt_text.py script
    cmd = f'python3 send_files_to_chatgpt_text.py "{prompt_file}" --api_key "sk-proj-OEveuX_jpD_Z..." --output_file "comprehensive_estimate_with_pricing.txt"'
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Successfully sent to ChatGPT!")
            print("📁 Output saved to: comprehensive_estimate_with_pricing.txt")
        else:
            print("❌ Error sending to ChatGPT:")
            print(result.stderr)
    except Exception as e:
        print(f"❌ Error: {e}")
    
    return prompt_file

if __name__ == "__main__":
    prompt_file = send_to_chatgpt_with_pricing()
    print(f"\n🎯 Next steps:")
    print(f"1. Check the output file: comprehensive_estimate_with_pricing.txt")
    print(f"2. Convert the JSON response to CSV if needed")
    print(f"3. Create the final Excel file")

