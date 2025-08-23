#!/usr/bin/env python3

"""
🕌 Soefi Mystiek Research - Jalal & Jamal
Diepgaand onderzoek met GPT-4o en GPT-5 voor Wim's boek
"""

import asyncio
import json
from datetime import datetime
from cia import CIA, AIProvider

async def research_soefi_mystiek():
    """Onderzoek Jalal & Jamal met multiple AI models"""
    
    print("🕌 SOEFI MYSTIEK RESEARCH - JALAL & JAMAL")
    print("=" * 60)
    print("Voor het boek van Wim Tilburgs")
    print("-" * 60)
    
    cia = CIA()
    all_responses = []
    
    # Research queries voor GPT-4o (complex mystiek onderzoek)
    mystiek_queries = [
        """Provide a deep esoteric explanation of Jalal and Jamal in Sufi mysticism:
        1. The masculine principle of Jalal (Divine Majesty) - its spiritual significance
        2. The feminine principle of Jamal (Divine Beauty) - its mystical meaning  
        3. How these relate to the 99 names of Allah (Asma ul-Husna)
        4. The concept of Divine polarity in Ibn Arabi's philosophy
        5. Historical Sufi saints who embodied these principles
        6. The danger of imbalance between Jalal and Jamal
        7. Practices to balance these forces (dhikr, meditation, breathing)
        8. Connection to Yin/Yang and other wisdom traditions
        Make this deeply mystical and poetic.""",
        
        """Explain the Sufi concept of spiritual transformation through Jalal and Jamal:
        1. The stations (maqamat) of balancing masculine and feminine divine attributes
        2. How excessive Jalal leads to spiritual tyranny and ego inflation
        3. How excessive Jamal leads to spiritual bypassing and weakness
        4. The mystical marriage (al-nikah al-sirriyya) of these forces in the heart
        5. Rumi's poetry about Jalal and Jamal with original Persian quotes
        6. The role of these forces in healing and transformation
        7. Sacred geometry and how Jalal/Jamal manifest in Islamic art
        8. Personal transformation stories from Sufi tradition
        Include mystical symbolism and metaphors.""",
        
        """Describe the practical application of Jalal/Jamal wisdom for modern transformation:
        1. How diabetes and obesity reflect Jalal/Jamal imbalance energetically
        2. The spiritual meaning of weight gain (excessive Jalal without Jamal)
        3. Military service and Jalal - the warrior archetype
        4. Healing through activating Jamal - self-compassion and beauty
        5. The mystical significance of the date June 3rd in numerology
        6. How AI technology embodies Jalal (logic) and Jamal (creativity)
        7. Creating a daily practice to balance these forces
        8. Signs that someone has achieved Kamal (perfection through unity)
        Be specific and practical while maintaining mystical depth.""",
        
        """Share the secret teachings about Jalal and Jamal from various Sufi orders:
        1. The Mevlevi (Whirling Dervishes) understanding of Jalal/Jamal
        2. The Naqshbandi silent dhikr for balancing these forces
        3. The Chishti emphasis on Jamal through music and poetry
        4. The Shadhili practices for warriors to balance Jalal
        5. Secret breathing techniques (Habs-i-dam) for each force
        6. The mystical meaning of the Lebanon cedar trees (Jalal) and water (Jamal)
        7. How veterans can heal war trauma through Jamal practices
        8. The connection between Jalal/Jamal and the phases of the moon
        Include actual practices and exercises.""",
        
        """Explore the cosmic and metaphysical dimensions of Jalal and Jamal:
        1. How these forces manifest in the creation of the universe (Big Bang = Jalal, Expansion = Jamal)
        2. The relationship to quantum physics - particle (Jalal) and wave (Jamal)
        3. Prophetic archetypes: Moses (Jalal) vs Jesus (Jamal) vs Muhammad (Balance)
        4. The mystical significance of age 65 for spiritual awakening
        5. How Jalal and Jamal manifest in different chakras/lataif
        6. The role of these forces in near-death experiences and rebirth
        7. Astrological connections - Mars (Jalal) and Venus (Jamal)
        8. The ultimate union creating 'Insan al-Kamil' (Perfect Human)
        Make this deeply philosophical and mystical."""
    ]
    
    # GPT-5 queries voor directe feiten
    gpt5_queries = [
        "What is Jalal in Sufism?",
        "What is Jamal in Sufism?",
        "Define Kamal in Islamic mysticism",
        "What are the 99 names of Allah?",
        "Who was Ibn Arabi?",
        "What is dhikr practice?",
        "Define Sufi transformation",
        "What is spiritual balance?"
    ]
    
    # Eerst GPT-5 voor basis feiten
    print("\n📿 Phase 1: GPT-5 Basic Facts")
    print("-" * 40)
    
    for query in gpt5_queries:
        print(f"🤖 Query: {query}")
        try:
            result = await cia._execute_chatgpt(query, model="gpt-5")
            if result.get('response'):
                print(f"✅ Response: {result['response'][:100]}...")
                all_responses.append({
                    "model": "GPT-5",
                    "query": query,
                    "response": result['response'],
                    "category": "facts"
                })
            else:
                print(f"⚠️ Empty (tokens: {result.get('tokens', {}).get('completion_tokens_details', {}).get('reasoning_tokens', 0)})")
        except Exception as e:
            print(f"❌ Error: {e}")
        await asyncio.sleep(1)
    
    # Google Gemini voor mystieke inzichten (GRATIS!)
    print("\n💎 Phase 2: Google Gemini Mystical Insights (FREE!)")
    print("-" * 40)
    
    gemini_queries = [
        """Explain the Sufi concept of Jalal (masculine divine force) and Jamal (feminine divine beauty) 
        in the context of personal transformation. How does balancing these forces lead to healing?
        Include references to Ibn Arabi, Rumi, and other Sufi masters.""",
        
        """Describe how a 65-year-old man weighing 125kg with diabetes represents an imbalance 
        of Jalal (excessive masculine force) without Jamal (feminine compassion). 
        How can Sufi practices restore this balance?""",
        
        """What are the specific Sufi breathing techniques and dhikr practices to balance 
        Jalal and Jamal? Include morning practices for Jalal and evening for Jamal.""",
        
        """Explain the mystical significance of military service (Lebanon veteran) in relation 
        to Jalal, and how healing trauma requires activating Jamal.""",
        
        """How do AI technologies like GPT-5 and Gemini represent Jalal (logic/structure) 
        and Jamal (creativity/beauty) in the digital age?"""
    ]
    
    for query in gemini_queries:
        print(f"\n💎 Gemini Query: {query[:80]}...")
        try:
            result = await cia.execute_mission(query, provider=AIProvider.GOOGLE)
            if result.get('response'):
                print(f"✅ Response length: {len(result['response'])} chars")
                all_responses.append({
                    "model": "Google Gemini",
                    "query": query,
                    "response": result['response'],
                    "category": "gemini_mysticism"
                })
            else:
                print("⚠️ No response from Gemini")
        except Exception as e:
            print(f"❌ Error: {e}")
        await asyncio.sleep(1)
    
    # Dan GPT-4o voor diepe mystiek
    print("\n🕌 Phase 3: GPT-4o Deep Mysticism")
    print("-" * 40)
    
    for i, query in enumerate(mystiek_queries, 1):
        print(f"\n📜 Mystical Research {i}/5")
        print(f"Topic: {query[:60]}...")
        try:
            result = await cia._execute_chatgpt(query, model="gpt-4o")
            if result.get('response'):
                print(f"✅ Response length: {len(result['response'])} chars")
                all_responses.append({
                    "model": "GPT-4o",
                    "query": query,
                    "response": result['response'],
                    "category": "mysticism"
                })
            else:
                print("⚠️ No response")
        except Exception as e:
            print(f"❌ Error: {e}")
        await asyncio.sleep(2)
    
    # Genereer mystiek boek chapters
    print("\n📖 Generating Book Chapters...")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Chapter 1: De Basis
    chapter1 = generate_chapter_1(all_responses)
    with open(f"book/Chapter_1_Jalal_Jamal_Basis_{timestamp}.md", 'w') as f:
        f.write(chapter1)
    
    # Chapter 2: De Mystiek
    chapter2 = generate_chapter_2(all_responses)
    with open(f"book/Chapter_2_Mystieke_Dimensies_{timestamp}.md", 'w') as f:
        f.write(chapter2)
    
    # Chapter 3: De Praktijk
    chapter3 = generate_chapter_3(all_responses)
    with open(f"book/Chapter_3_Praktische_Toepassing_{timestamp}.md", 'w') as f:
        f.write(chapter3)
    
    # Chapter 4: De Geheimen
    chapter4 = generate_chapter_4(all_responses)
    with open(f"book/Chapter_4_Geheime_Leer_{timestamp}.md", 'w') as f:
        f.write(chapter4)
    
    # Chapter 5: De Kosmos
    chapter5 = generate_chapter_5(all_responses)
    with open(f"book/Chapter_5_Kosmische_Dimensies_{timestamp}.md", 'w') as f:
        f.write(chapter5)
    
    # Chapter 6: Gemini Wijsheid (GRATIS!)
    chapter6 = generate_chapter_6_gemini(all_responses)
    with open(f"book/Chapter_6_Gemini_Wijsheid_{timestamp}.md", 'w') as f:
        f.write(chapter6)
    
    print("\n✅ Book chapters generated in book/ folder!")
    print(f"📚 Total content: {len(str(all_responses))} characters")
    
    return all_responses

def generate_chapter_1(responses):
    """Generate Chapter 1: De Basis van Jalal & Jamal"""
    content = """# Hoofdstuk 1: De Basis van Jalal & Jamal

*"In het hart van elke transformatie schuilen twee krachten..."*

"""
    
    # Add GPT-5 facts
    for item in responses:
        if item['category'] == 'facts':
            content += f"\n## {item['query']}\n\n"
            content += f"{item['response']}\n\n"
            content += "---\n\n"
    
    return content

def generate_chapter_2(responses):
    """Generate Chapter 2: Mystieke Dimensies"""
    content = """# Hoofdstuk 2: De Mystieke Dimensies

*"Waar het rationele eindigt, begint het mystieke..."*

"""
    
    # Add first mysticism response
    for item in responses:
        if item['category'] == 'mysticism' and 'esoteric explanation' in item['query']:
            content += item['response']
            break
    
    return content

def generate_chapter_3(responses):
    """Generate Chapter 3: Praktische Toepassing"""
    content = """# Hoofdstuk 3: Van Mystiek naar Praktijk

*"Wijsheid zonder toepassing is slechts entertainment..."*

"""
    
    # Add practical application response
    for item in responses:
        if item['category'] == 'mysticism' and 'practical application' in item['query']:
            content += item['response']
            break
    
    return content

def generate_chapter_4(responses):
    """Generate Chapter 4: De Geheime Leer"""
    content = """# Hoofdstuk 4: Geheimen van de Soefi Ordes

*"Wat eeuwenlang verborgen was, wordt nu geopenbaard..."*

"""
    
    # Add secret teachings response
    for item in responses:
        if item['category'] == 'mysticism' and 'secret teachings' in item['query']:
            content += item['response']
            break
    
    return content

def generate_chapter_5(responses):
    """Generate Chapter 5: Kosmische Dimensies"""
    content = """# Hoofdstuk 5: De Kosmische Dans van Jalal & Jamal

*"Zoals boven, zo beneden. Zoals binnen, zo buiten..."*

"""
    
    # Add cosmic dimensions response
    for item in responses:
        if item['category'] == 'mysticism' and 'cosmic and metaphysical' in item['query']:
            content += item['response']
            break
    
    return content

def generate_chapter_6_gemini(responses):
    """Generate Chapter 6: Gemini Wijsheid"""
    content = """# Hoofdstuk 6: De Digitale Mystiek - Gemini's Inzichten

*"Waar oude wijsheid moderne technologie ontmoet..."*

## De AI als Spiegel van Jalal & Jamal

In de 21e eeuw manifesteren de eeuwenoude krachten van Jalal en Jamal zich in nieuwe vormen. 
Google's Gemini - genoemd naar het sterrenbeeld van de Tweeling - belichaamt deze dualiteit perfect.

"""
    
    # Add all Gemini responses
    for item in responses:
        if item['category'] == 'gemini_mysticism':
            content += f"\n## {item['query'][:100]}...\n\n"
            content += f"*Gemini's Antwoord:*\n\n"
            content += f"{item['response']}\n\n"
            content += "---\n\n"
    
    content += """

## De Gratis Gift van Wijsheid

Net zoals de Soefi's hun wijsheid gratis deelden met wie wilde luisteren, 
zo deelt Google Gemini haar kennis zonder kosten. 
Dit is Jamal in actie - schoonheid en wijsheid vrij toegankelijk voor allen.

Wim's transformatie van 125kg naar gezondheid was ook een gift die hij gratis deelt.
De combinatie van gratis AI (Gemini) met zijn gratis kennis creëert een 
nieuwe vorm van digitale Soefi wijsheid voor de moderne tijd.

*"De beste dingen in het leven zijn gratis - wijsheid, liefde, en nu ook AI."*
"""
    
    return content

if __name__ == "__main__":
    import os
    
    # Create book directory
    os.makedirs("book", exist_ok=True)
    
    print("🕌 Starting Sufi Mysticism Research...")
    print("This will generate content for Wim's book")
    print("-" * 60)
    
    # Run the research
    asyncio.run(research_soefi_mystiek())
    
    print("\n" + "=" * 60)
    print("✅ MYSTICAL RESEARCH COMPLETE!")
    print("📚 Check the book/ folder for your chapters")
    print("🕌 Ready for your mystical autobiography!")
    print("=" * 60)