# 🤖 Grok toevoegen aan CIA App

## Stap 1: API Key toevoegen aan .env

```bash
# Voeg deze regel toe aan .env file:
GROK_API_KEY=xai_[jouw_key_hier]
```

## Stap 2: Test script

Maak `test_grok.py`:

```python
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Setup Grok client
client = OpenAI(
    api_key=os.getenv('GROK_API_KEY'),
    base_url="https://api.x.ai/v1"
)

# Test Grok-2
print("🤖 Testing Grok-2 with X Premium access...")

response = client.chat.completions.create(
    model="grok-2",
    messages=[
        {"role": "user", "content": "Wat is er trending op X over AI vandaag?"}
    ],
    max_tokens=500
)

print("\n📍 Grok-2 Response:")
print(response.choices[0].message.content)

# Check usage
print(f"\n📊 Tokens used: {response.usage.total_tokens}")
print(f"💰 Messages remaining today: ~{100 - 1}/100")
```

## Stap 3: Integreer in CIA

Update `cia.py` om Grok toe te voegen:

```python
def _init_grok(self):
    """Initialize Grok AI (X Premium)"""
    api_key = os.getenv('GROK_API_KEY')
    if api_key:
        print("✅ GROK API key loaded (X Premium - Grok-2)")
        from openai import OpenAI
        return OpenAI(
            api_key=api_key,
            base_url="https://api.x.ai/v1"
        )
    else:
        print("⚠️  GROK API key missing")
        return None
```

## Daily Limits met X Premium:

- **API Calls**: 100/dag
- **Reset**: Midnight UTC
- **Monitor**: Check console.x.ai voor usage

## Pro Tips:

1. **Gebruik Grok voor**:
   - Real-time X/Twitter trends
   - Current events
   - Social sentiment analysis

2. **Bespaar messages**:
   - Batch vragen waar mogelijk
   - Cache responses lokaal
   - Gebruik andere AI's voor non-realtime

3. **Maximale waarde**:
   ```python
   # Combineer real-time met analysis
   prompt = """
   1. Wat trending op X over [topic]?
   2. Analyseer sentiment
   3. Voorspel volgende trend
   4. Geef actionable insights
   """
   ```

Ready om te testen! 🚀