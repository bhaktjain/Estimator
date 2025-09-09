#!/usr/bin/env python3
import openai
import os

# Test API key
api_key = "os.getenv('OPENAI_API_KEY')"

print(f"API Key length: {len(api_key)}")
print(f"API Key starts with: {api_key[:20]}...")
print(f"API Key ends with: ...{api_key[-20:]}")

try:
    client = openai.OpenAI(api_key=api_key)
    print("✅ API key is valid - client created successfully")
    
    # Test a simple API call
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": "Say hello"}],
        max_tokens=10
    )
    print(f"✅ API call successful: {response.choices[0].message.content}")
    
except Exception as e:
    print(f"❌ API key test failed: {e}")
