#!/bin/bash

# Script om Google API key op te slaan in 1Password
# Datum: 23 augustus 2025

echo "🔐 Google AI Studio API Key opslaan in 1Password..."
echo ""
echo "Dit script slaat je Google API key veilig op in 1Password."
echo "Je moet inloggen met Touch ID als daarom gevraagd wordt."
echo ""

# API Key - REMOVED FOR SECURITY
GOOGLE_API_KEY="${GOOGLE_API_KEY:-[YOUR_GOOGLE_API_KEY_HERE]}"

# Opslaan in 1Password
op item create \
  --category="API Credential" \
  --title="🤖 Google AI Studio API" \
  --vault="AI Services" \
  credential="$GOOGLE_API_KEY" \
  username="wim@jeleefstijlalsmedicijn.nl" \
  url="https://makersuite.google.com/app/apikey" \
  --tags="google,ai,gemini,free,cia-app" \
  notes="Google AI Studio API key voor Gemini Pro (FREE tier).
Aangemaakt: 23 augustus 2025
Gebruikt in: CIA app voor gratis vertalingen en AI queries
Model: Gemini Pro (gratis tot 60 queries/minuut)
Project: JLAM / CIA Platform
Status: ACTIEF"

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Google API key succesvol opgeslagen in 1Password!"
    echo "📍 Locatie: AI Services vault → 🤖 Google AI Studio API"
    echo ""
    echo "Je kunt deze key nu ophalen met:"
    echo "op item get '🤖 Google AI Studio API' --fields credential"
else
    echo ""
    echo "⚠️  Er ging iets mis. Probeer het handmatig:"
    echo ""
    echo "1. Open 1Password"
    echo "2. Ga naar 'AI Services' vault"
    echo "3. Klik op '+' voor nieuw item"
    echo "4. Kies 'API Credential'"
    echo "5. Vul in:"
    echo "   Title: 🤖 Google AI Studio API"
    echo "   Credential: [YOUR_GOOGLE_API_KEY_HERE]"
    echo "   Notes: Google AI Studio - Gemini Pro FREE"
fi