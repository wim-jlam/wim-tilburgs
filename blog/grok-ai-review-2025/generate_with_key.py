#!/usr/bin/env python3
import os
import sys
sys.path.append('/Users/wimtilburgs/Development/cia-app')

# Load the API key
with open('/tmp/openai_key.txt', 'r') as f:
    api_key = f.read().strip()
    
os.environ['OPENAI_API_KEY'] = api_key
print(f"✅ API Key loaded: {api_key[:15]}...")

# Now run the generation
import generate_images
