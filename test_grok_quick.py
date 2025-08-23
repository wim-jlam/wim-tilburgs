#!/usr/bin/env python3
"""
Quick Grok API test
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

print("🔍 Testing Grok API access...")
print("API Key loaded:", "Yes" if os.getenv('GROK_API_KEY') else "No")

try:
    client = OpenAI(
        api_key=os.getenv('GROK_API_KEY'),
        base_url="https://api.x.ai/v1"
    )
    
    # Try simple request
    response = client.chat.completions.create(
        model="grok-2",
        messages=[{"role": "user", "content": "Hello"}],
        max_tokens=10
    )
    
    print("✅ Success:", response.choices[0].message.content)
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("\n📍 Dit betekent waarschijnlijk:")
    print("1. X Premium geeft Grok IN de X app")
    print("2. Voor API toegang moet je credits kopen op console.x.ai")
    print("3. Beta programma: $25/maand gratis credits")
    print("4. Of betaal voor API credits apart")