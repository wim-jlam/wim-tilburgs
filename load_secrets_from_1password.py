#!/usr/bin/env python3
"""
Load secrets from 1Password for CIA app
No Touch ID required with service account!
"""

import os
import subprocess
import json

def get_1password_secret(item_name, field="credential"):
    """Get secret from 1Password"""
    try:
        result = subprocess.run(
            ["op", "item", "get", item_name, "--fields", field, "--reveal"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"❌ Error getting {item_name}: {e}")
        return None

def load_all_secrets():
    """Load all AI API keys from 1Password"""
    secrets = {}
    
    # Grok API Key
    print("🔑 Loading Grok API key from 1Password...")
    grok_key = get_1password_secret("Grok API Key (xAI)")
    if grok_key:
        secrets['GROK_API_KEY'] = grok_key
        os.environ['GROK_API_KEY'] = grok_key
        print("✅ Grok API key loaded")
    
    # Add more keys as needed
    # openai_key = get_1password_secret("OpenAI API Key")
    # google_key = get_1password_secret("Google AI API Key")
    
    return secrets

def test_grok_with_1password():
    """Test Grok using key from 1Password"""
    from openai import OpenAI
    
    # Load secret
    secrets = load_all_secrets()
    
    if not secrets.get('GROK_API_KEY'):
        print("❌ Could not load Grok API key from 1Password")
        return
    
    print("\n🧪 Testing Grok API...")
    
    try:
        client = OpenAI(
            api_key=secrets['GROK_API_KEY'],
            base_url="https://api.x.ai/v1"
        )
        
        response = client.chat.completions.create(
            model="grok-2",
            messages=[{"role": "user", "content": "Say 'Hello from 1Password integration!'"}],
            max_tokens=20
        )
        
        print("✅ Grok response:", response.choices[0].message.content)
        
    except Exception as e:
        print(f"❌ Grok API error: {e}")
        if "credits" in str(e).lower():
            print("\n💡 Reminder: Je hebt API credits nodig!")
            print("   Ga naar: https://console.x.ai/team/")
            print("   Koop credits of claim beta access")

if __name__ == "__main__":
    print("🔐 1Password + CIA Integration")
    print("=" * 40)
    
    # Check if op CLI is available
    try:
        subprocess.run(["op", "--version"], capture_output=True, check=True)
        print("✅ 1Password CLI is installed")
    except:
        print("❌ 1Password CLI not found. Install with: brew install 1password-cli")
        exit(1)
    
    # Test the integration
    test_grok_with_1password()
    
    print("\n📝 To use in CIA app:")
    print("   from load_secrets_from_1password import load_all_secrets")
    print("   secrets = load_all_secrets()")
    print("   # Now all API keys are in os.environ!")