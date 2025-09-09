#!/usr/bin/env python3
"""
Direct OpenAI API call for comprehensive estimate
"""
import os
import openai
from dotenv import load_dotenv

def call_openai_for_estimate():
    """Call OpenAI API directly for comprehensive estimate."""
    
    # Load environment variables
    load_dotenv()
    
    # Set up OpenAI client
    client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    print("🚀 CALLING OPENAI API FOR COMPREHENSIVE ESTIMATE")
    print("=" * 60)
    
    # Read the comprehensive prompt
    prompt_file = "comprehensive_estimate_prompt.txt"
    if not os.path.exists(prompt_file):
        print(f"❌ Prompt file not found: {prompt_file}")
        return
    
    with open(prompt_file, 'r', encoding='utf-8') as f:
        prompt_content = f.read()
    
    print(f"📝 Prompt loaded: {len(prompt_content)} characters")
    
    try:
        print("🔄 Calling OpenAI API...")
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional construction estimator with expertise in commercial renovations. Provide accurate estimates using the provided pricing data and takeoff information."
                },
                {
                    "role": "user",
                    "content": prompt_content
                }
            ],
            temperature=0.1,
            max_tokens=8000
        )
        
        # Extract the response
        estimate_response = response.choices[0].message.content
        
        # Save the response
        output_file = "comprehensive_estimate_with_pricing.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(estimate_response)
        
        print("✅ Successfully received estimate from OpenAI!")
        print(f"📁 Response saved to: {output_file}")
        print(f"📊 Response length: {len(estimate_response)} characters")
        
        # Show a preview
        print("\n📋 RESPONSE PREVIEW:")
        print("-" * 40)
        lines = estimate_response.split('\n')
        for i, line in enumerate(lines[:20]):
            print(line)
        if len(lines) > 20:
            print(f"... and {len(lines) - 20} more lines")
        
        return output_file
        
    except Exception as e:
        print(f"❌ Error calling OpenAI API: {e}")
        return None

if __name__ == "__main__":
    output_file = call_openai_for_estimate()
    if output_file:
        print(f"\n🎯 Next steps:")
        print(f"1. Review the estimate in: {output_file}")
        print(f"2. Convert JSON to CSV if needed")
        print(f"3. Create final Excel file")
    else:
        print("\n❌ Failed to get estimate from OpenAI")

