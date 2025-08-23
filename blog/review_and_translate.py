#!/usr/bin/env python3
"""
Review and translate all blog articles using Google AI (Gemini)
Creates bilingual versions with quality improvements
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

# Add parent directory for imports
sys.path.append('/Users/wimtilburgs/Development/wim-tilburgs')

# Import Google AI
import google.generativeai as genai
from load_secrets_from_1password import load_all_secrets

def setup_gemini():
    """Initialize Gemini Pro"""
    load_all_secrets()
    
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key or api_key == 'your_google_api_key_here':
        print("❌ Google API key not found!")
        print("   Please set GOOGLE_API_KEY in .env or 1Password")
        return None
    
    genai.configure(api_key=api_key)
    
    # Use Gemini Pro for best quality
    model = genai.GenerativeModel('gemini-pro')
    print(f"✅ Gemini Pro initialized")
    return model

def review_article(model, content, filename):
    """Review article for quality and improvements"""
    
    review_prompt = f"""
    You are an expert content editor and SEO specialist. Review this article and provide:
    
    1. QUALITY SCORE (1-10) for:
       - Content quality
       - SEO optimization
       - Readability
       - Engagement potential
    
    2. IMPROVEMENTS needed:
       - Content gaps
       - SEO improvements
       - Better hooks/CTAs
       - Fact checking concerns
    
    3. VIRAL POTENTIAL analysis
    
    Article to review:
    {content}
    
    Provide a structured JSON response with scores and specific improvements.
    """
    
    try:
        response = model.generate_content(review_prompt)
        return response.text
    except Exception as e:
        print(f"   ❌ Error reviewing {filename}: {e}")
        return None

def translate_article(model, content, source_lang, target_lang):
    """Translate article while maintaining tone and SEO"""
    
    translate_prompt = f"""
    You are an expert translator and content localizer. Translate this {source_lang} article to {target_lang}.
    
    REQUIREMENTS:
    1. Maintain the original tone and style
    2. Adapt cultural references appropriately
    3. Keep SEO keywords relevant for {target_lang} market
    4. Preserve all formatting (markdown)
    5. Localize prices (€ vs $) if needed
    6. Keep technical terms accurate
    
    ORIGINAL ARTICLE:
    {content}
    
    Provide the complete translated article, ready for publication.
    """
    
    try:
        response = model.generate_content(translate_prompt)
        return response.text
    except Exception as e:
        print(f"   ❌ Error translating: {e}")
        return None

def improve_article(model, content, feedback):
    """Improve article based on AI feedback"""
    
    improve_prompt = f"""
    You are an expert content optimizer. Improve this article based on the feedback.
    
    ORIGINAL ARTICLE:
    {content}
    
    FEEDBACK TO IMPLEMENT:
    {feedback}
    
    Provide the COMPLETE improved article with all suggested changes implemented.
    Focus on:
    - Better hooks and engagement
    - Stronger CTAs
    - SEO optimization
    - Fact accuracy
    - Readability improvements
    
    Return the full improved article in markdown format.
    """
    
    try:
        response = model.generate_content(improve_prompt)
        return response.text
    except Exception as e:
        print(f"   ❌ Error improving: {e}")
        return None

def process_all_articles():
    """Process all blog articles"""
    
    print("🚀 BLOG ARTICLE REVIEW & TRANSLATION SYSTEM")
    print("=" * 60)
    
    # Setup Gemini
    model = setup_gemini()
    if not model:
        return
    
    # Article locations
    articles = [
        {
            "path": "grok-ai-review-2025/article.md",
            "name": "Grok AI Review 2025",
            "lang": "Dutch",
            "translate_to": "English"
        },
        {
            "path": "grok-blog-series/1-developers-guide.md",
            "name": "Developer's Guide",
            "lang": "English",
            "translate_to": "Dutch"
        },
        {
            "path": "grok-blog-series/2-chatgpt-vs-grok-business.md",
            "name": "Business Migration",
            "lang": "English",
            "translate_to": "Dutch"
        },
        {
            "path": "grok-blog-series/3-chatgpt-hidden-costs.md",
            "name": "Hidden Costs",
            "lang": "English",
            "translate_to": "Dutch"
        },
        {
            "path": "grok-blog-series/4-x-twitter-grok-strategy.md",
            "name": "Elon's Strategy",
            "lang": "English",
            "translate_to": "Dutch"
        },
        {
            "path": "grok-blog-series/5-chatgpt-o1-still-behind.md",
            "name": "o1 Model Analysis",
            "lang": "English",
            "translate_to": "Dutch"
        }
    ]
    
    # Create output directories
    os.makedirs("reviewed", exist_ok=True)
    os.makedirs("bilingual/nl", exist_ok=True)
    os.makedirs("bilingual/en", exist_ok=True)
    
    results = []
    
    for article in articles:
        print(f"\n📝 Processing: {article['name']}")
        print("-" * 40)
        
        # Read original
        file_path = Path(article['path'])
        if not file_path.exists():
            print(f"   ⚠️ File not found: {article['path']}")
            continue
        
        with open(file_path, 'r') as f:
            content = f.read()
        
        print(f"   📖 Original: {len(content)} characters")
        
        # 1. Review for quality
        print("   🔍 Reviewing quality...")
        review = review_article(model, content, article['name'])
        
        if review:
            # Save review
            review_path = f"reviewed/{file_path.stem}_review.json"
            with open(review_path, 'w') as f:
                f.write(review)
            print(f"   ✅ Review saved: {review_path}")
            
            # 2. Improve based on feedback
            print("   ✨ Improving article...")
            improved = improve_article(model, content, review)
            
            if improved:
                # Save improved version
                improved_path = f"reviewed/{file_path.stem}_improved.md"
                with open(improved_path, 'w') as f:
                    f.write(improved)
                print(f"   ✅ Improved version saved")
                
                # Use improved version for translation
                content = improved
        
        # 3. Translate to other language
        print(f"   🌍 Translating {article['lang']} → {article['translate_to']}...")
        translation = translate_article(model, content, article['lang'], article['translate_to'])
        
        if translation:
            # Save both language versions
            if article['lang'] == "Dutch":
                nl_path = f"bilingual/nl/{file_path.stem}.md"
                en_path = f"bilingual/en/{file_path.stem}.md"
                
                with open(nl_path, 'w') as f:
                    f.write(content)  # Original Dutch
                with open(en_path, 'w') as f:
                    f.write(translation)  # Translated English
                    
            else:  # English original
                en_path = f"bilingual/en/{file_path.stem}.md"
                nl_path = f"bilingual/nl/{file_path.stem}.md"
                
                with open(en_path, 'w') as f:
                    f.write(content)  # Original English
                with open(nl_path, 'w') as f:
                    f.write(translation)  # Translated Dutch
            
            print(f"   ✅ Bilingual versions saved")
            
            results.append({
                "article": article['name'],
                "status": "success",
                "review": "completed",
                "translation": "completed",
                "improved": "yes"
            })
        else:
            results.append({
                "article": article['name'],
                "status": "partial",
                "review": "completed" if review else "failed",
                "translation": "failed",
                "improved": "yes" if review else "no"
            })
    
    # Generate summary report
    print("\n" + "=" * 60)
    print("📊 PROCESSING COMPLETE")
    print("=" * 60)
    
    # Summary statistics
    successful = len([r for r in results if r['status'] == 'success'])
    print(f"\n✅ Successfully processed: {successful}/{len(articles)}")
    
    # Create summary report
    report = {
        "timestamp": datetime.now().isoformat(),
        "articles_processed": len(articles),
        "successful": successful,
        "results": results,
        "output_structure": {
            "reviewed/": "Quality reviews and improved versions",
            "bilingual/nl/": "All articles in Dutch",
            "bilingual/en/": "All articles in English"
        }
    }
    
    with open("blog_processing_report.json", 'w') as f:
        json.dump(report, f, indent=2)
    
    print("\n📁 Output structure:")
    print("   reviewed/     - Reviews and improved versions")
    print("   bilingual/nl/ - All articles in Dutch")
    print("   bilingual/en/ - All articles in English")
    
    print("\n💡 Next steps:")
    print("1. Review the quality feedback in reviewed/")
    print("2. Check translations in bilingual/")
    print("3. Choose best versions for publication")
    print("4. Generate images for both language versions")
    
    return results

def create_bilingual_index():
    """Create index pages for both languages"""
    
    nl_index = """# 📚 Blog Artikelen - Nederlands

## AI & Technologie Artikelen door Wim Tilburgs

### Beschikbare Artikelen:

1. **Grok AI Review 2025**
   - Hoe Elon Musk 500 miljoen mensen een ChatGPT killer gaf
   - Persoonlijke test met €25 budget
   - [Lees artikel →](grok-ai-review-2025.md)

2. **Developer's Gids voor Grok API**
   - Bouw real-time AI apps voor €0.02 per query
   - Complete technische handleiding
   - [Lees artikel →](1-developers-guide.md)

3. **ChatGPT vs Grok voor Bedrijven**
   - Waarom ik overstap van €20 naar €8 AI
   - Bespaar €300/maand voor je team
   - [Lees artikel →](2-chatgpt-vs-grok-business.md)

4. **De Verborgen Kosten van ChatGPT**
   - Wat OpenAI je niet vertelt
   - Echte kosten: €1,200/maand, niet €20
   - [Lees artikel →](3-chatgpt-hidden-costs.md)

5. **Elon's Masterplan**
   - Hoe X + Grok LinkedIn gaat vervangen
   - De toekomst van business netwerken
   - [Lees artikel →](4-x-twitter-grok-strategy.md)

6. **ChatGPT o1 Model Analyse**
   - Waarom zelfs OpenAI's beste niet kan winnen
   - Real-time data vs slimme modellen
   - [Lees artikel →](5-chatgpt-o1-still-behind.md)
"""

    en_index = """# 📚 Blog Articles - English

## AI & Technology Articles by Wim Tilburgs

### Available Articles:

1. **Grok AI Review 2025**
   - How Elon Musk quietly gave 500 million people a ChatGPT killer
   - Personal €25 testing experiment
   - [Read article →](grok-ai-review-2025.md)

2. **Developer's Guide to Grok API**
   - Build real-time AI apps for €0.02 per query
   - Complete technical documentation
   - [Read article →](1-developers-guide.md)

3. **ChatGPT vs Grok for Business**
   - Why I'm moving from $20 to $8 AI
   - Save €300/month for your team
   - [Read article →](2-chatgpt-vs-grok-business.md)

4. **The Hidden Costs of ChatGPT**
   - What OpenAI doesn't tell you
   - Real cost: €1,200/month, not €20
   - [Read article →](3-chatgpt-hidden-costs.md)

5. **Elon's Master Plan**
   - How X + Grok will eat LinkedIn's lunch
   - The future of business networking
   - [Read article →](4-x-twitter-grok-strategy.md)

6. **ChatGPT o1 Model Analysis**
   - Why even OpenAI's best can't win
   - Real-time data vs smart models
   - [Read article →](5-chatgpt-o1-still-behind.md)
"""
    
    # Save index files
    with open("bilingual/nl/README.md", 'w') as f:
        f.write(nl_index)
    
    with open("bilingual/en/README.md", 'w') as f:
        f.write(en_index)
    
    print("\n✅ Bilingual index pages created")

if __name__ == "__main__":
    print("🌍 Bilingual Blog Processing System")
    print("=" * 60)
    print("This will:")
    print("1. Review all articles for quality")
    print("2. Improve based on AI feedback")
    print("3. Translate to both Dutch and English")
    print("4. Create organized bilingual structure")
    print()
    
    # Process all articles
    results = process_all_articles()
    
    # Create index pages
    if results:
        create_bilingual_index()
    
    print("\n✅ Complete! Check the output folders for results.")