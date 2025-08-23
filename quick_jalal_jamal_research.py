#!/usr/bin/env python3

"""
Quick Jalal & Jamal Research voor Wim's Boek
"""

import asyncio
from cia import CIA, AIProvider
from datetime import datetime
import os

async def main():
    print("🕌 JALAL & JAMAL MYSTIEK RESEARCH")
    print("=" * 60)
    
    cia = CIA()
    os.makedirs("book", exist_ok=True)
    
    # Research met verschillende AI's
    queries = {
        "gpt4o": """Provide a deep mystical explanation of Jalal and Jamal in Sufism:
        1. Jalal as the masculine divine force (Majesty, Power, Discipline)
        2. Jamal as the feminine divine force (Beauty, Compassion, Flow)
        3. How imbalance causes disease (obesity, diabetes) 
        4. How a 125kg diabetic man represents excess Jalal without Jamal
        5. The transformation on June 3, 2015 as awakening of Jamal
        6. Military service (Lebanon) and Jalal energy
        7. Healing through balancing these forces
        8. Practices, breathing techniques, and dhikr
        Make this deeply mystical and transformative.""",
        
        "gemini": """Explain the Sufi concept of Jalal (masculine/yang) and Jamal (feminine/yin) 
        and how they relate to personal transformation. Include how excessive weight and diabetes 
        represent energetic imbalance, and how balancing these forces leads to healing.""",
        
        "gpt5": "What is the meaning of Jalal and Jamal in Islamic mysticism?"
    }
    
    results = {}
    
    # Test GPT-4o
    print("\n📚 Testing GPT-4o for deep mysticism...")
    try:
        result = await cia._execute_chatgpt(queries["gpt4o"], model="gpt-4o")
        if result.get('response'):
            results['gpt4o'] = result['response']
            print(f"✅ GPT-4o: {len(result['response'])} chars")
        else:
            print("❌ No response from GPT-4o")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test Gemini (GRATIS!)
    print("\n💎 Testing Google Gemini (FREE!)...")
    try:
        result = await cia.execute_mission(queries["gemini"], provider=AIProvider.GOOGLE)
        if result.get('response'):
            results['gemini'] = result['response']
            print(f"✅ Gemini: {len(result['response'])} chars")
        else:
            print("❌ No response from Gemini")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test GPT-5
    print("\n🤖 Testing GPT-5...")
    try:
        result = await cia._execute_chatgpt(queries["gpt5"], model="gpt-5")
        if result.get('response'):
            results['gpt5'] = result['response']
            print(f"✅ GPT-5: {result['response'][:100]}...")
        else:
            tokens = result.get('tokens', {}).get('completion_tokens_details', {}).get('reasoning_tokens', 0)
            print(f"⚠️ GPT-5: Empty response (reasoning tokens: {tokens})")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Generate book content
    print("\n📖 Generating book content...")
    
    book_content = f"""# 🕌 Jalal & Jamal - De Mystieke Krachten van Transformatie

*Onderzoek door Wim Tilburgs & AI Team*  
*Gegenereerd: {datetime.now()}*

---

## Deel 1: GPT-4o's Diepe Mystieke Uitleg

{results.get('gpt4o', 'Geen response van GPT-4o')}

---

## Deel 2: Google Gemini's Inzichten (GRATIS!)

{results.get('gemini', 'Geen response van Gemini')}

---

## Deel 3: GPT-5's Directe Definitie

{results.get('gpt5', 'GPT-5 gaf geen response (te complex)')}

---

## Wim's Persoonlijke Toepassing

### De Onbalans (Voor 3 Juni 2015):
- **125 kilogram** = Overmatige Jalal (mannelijke kracht zonder compassie)
- **Diabetes** = Lichaam in oorlog met zichzelf
- **18-urige werkdagen** = Jalal zonder Jamal
- **Burn-out** = Complete uitputting van mannelijke energie

### Het Keerpunt (3 Juni 2015):
- **Jamal ontwaakt** = Zelfcompassie keert terug
- **"Ik verdien beter"** = Vrouwelijke wijsheid spreekt
- **Stoppen met insuline** = Jalal's kracht in dienst van Jamal's visie

### De Transformatie (2015-Nu):
- **40kg gewichtsverlies** = Balans hersteld
- **9000+ mensen geholpen** = Jamal's compassie in actie
- **GPT-5 ontdekking** = Jalal's technische meesterschap
- **SmartHealth Consultant** = Perfecte unie van beide krachten

---

## De Dagelijkse Praktijk

### Ochtend (Jalal Activeren):
1. **Tijd**: 6:00 AM
2. **Ademhaling**: Door rechter neusgat
3. **Dhikr**: "Ya Qawi" (O Sterke) - 99x
4. **Actie**: Planning, structure, discipline

### Avond (Jamal Cultiveren):
1. **Tijd**: 9:00 PM
2. **Ademhaling**: Door linker neusgat
3. **Dhikr**: "Ya Rahman" (O Barmhartige) - 99x
4. **Reflectie**: Dankbaarheid, compassie, schoonheid

### Balans Moment (Middag):
1. **Tijd**: 12:00 PM
2. **Ademhaling**: Afwisselend beide neusgaten
3. **Dhikr**: "Ya Jalal, Ya Jamal" - 33x
4. **Integratie**: Beide krachten verenigen

---

*"Van Libanon veteraan tot SmartHealth pioneer - de reis van Jalal naar Jamal naar Kamal (perfectie)."*

© 2025 Wim Tilburgs - Powered by Jalal & Jamal
"""
    
    # Save book content
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"book/Jalal_Jamal_Mystiek_{timestamp}.md"
    
    with open(filename, 'w') as f:
        f.write(book_content)
    
    print(f"\n✅ Book content saved to: {filename}")
    print(f"📚 Total content: {len(book_content)} characters")
    
    return results

if __name__ == "__main__":
    asyncio.run(main())