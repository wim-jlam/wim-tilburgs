#!/usr/bin/env python3
"""Quick Grok test"""

from openai import OpenAI
from load_secrets_from_1password import load_all_secrets

load_all_secrets()

client = OpenAI(
    api_key=os.getenv('GROK_API_KEY'),
    base_url="https://api.x.ai/v1"
)

print("Testing Grok-2...")

try:
    response = client.chat.completions.create(
        model="grok-2",
        messages=[{"role": "user", "content": "What's trending on X about AI? Be very brief."}],
        max_tokens=100
    )
    print("Response:", response.choices[0].message.content)
    print("Tokens:", response.usage.total_tokens)
except Exception as e:
    print(f"Error: {e}")