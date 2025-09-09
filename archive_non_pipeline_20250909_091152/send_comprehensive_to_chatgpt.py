#!/usr/bin/env python3
"""
Send comprehensive estimate request to ChatGPT with takeoff and pricing sheet
"""
import os
from openai import OpenAI
from dotenv import load_dotenv

def send_comprehensive_estimate():
    """Send comprehensive estimate request to ChatGPT."""
    
    print("🚀 SENDING COMPREHENSIVE ESTIMATE REQUEST TO CHATGPT")
    print("=" * 60)
    
    # Load environment variables
    load_dotenv()
    api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key:
        print("❌ OPENAI_API_KEY not found in .env file")
        return
    
    # Initialize OpenAI client
    client = OpenAI(api_key=api_key)
    
    # Read the comprehensive prompt
    with open('comprehensive_estimate_prompt_v2.txt', 'r', encoding='utf-8') as f:
        prompt = f.read()
    
    print("📋 Comprehensive prompt loaded")
    print(f"Prompt length: {len(prompt)} characters")
    
    try:
        print("\n🤖 Sending to ChatGPT...")
        
        # Send to ChatGPT
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional construction estimator. Provide accurate, detailed estimates using only the provided pricing rates."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=4000,
            temperature=0.1
        )
        
        # Extract the response
        estimate_response = response.choices[0].message.content
        
        # Save the response
        with open('comprehensive_estimate_chatgpt_response.txt', 'w', encoding='utf-8') as f:
            f.write(estimate_response)
        
        print("✅ Response received and saved to: comprehensive_estimate_chatgpt_response.txt")
        print(f"Response length: {len(estimate_response)} characters")
        
        # Show first 500 characters as preview
        print(f"\n📝 RESPONSE PREVIEW:")
        print("-" * 60)
        print(estimate_response[:500] + "..." if len(estimate_response) > 500 else estimate_response)
        
        return estimate_response
        
    except Exception as e:
        print(f"❌ Error sending to ChatGPT: {e}")
        return None

if __name__ == "__main__":
    response = send_comprehensive_estimate()
    if response:
        print(f"\n🎯 Next step: Process the ChatGPT response and create final estimate")
