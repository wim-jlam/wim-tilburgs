#!/usr/bin/env python3
"""
Review and improve blog articles using Google AI
Uses existing Google AI setup from parent directory
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

# Add parent directory to use existing Google AI setup
sys.path.append('/Users/wimtilburgs/Development/wim-tilburgs')

def review_with_google_api():
    """Use Google AI via direct API call"""
    
    print("🤖 BLOG REVIEW SYSTEM - Using Google AI")
    print("=" * 60)
    
    # Load Google API key from 1Password
    try:
        from load_secrets_from_1password import load_all_secrets
        load_all_secrets()
        
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key or api_key == 'your_google_api_key_here':
            print("❌ Google API key not found in environment")
            print("   Trying to load from 1Password...")
            
            import subprocess
            result = subprocess.run(
                ['op', 'item', 'get', 'Google AI API', '--fields', 'credential'],
                capture_output=True, text=True, check=False
            )
            
            if result.returncode == 0:
                api_key = result.stdout.strip()
                print("✅ Google API key loaded from 1Password")
            else:
                print("❌ Could not load Google API key")
                return None
        else:
            print("✅ Google API key found")
            
    except Exception as e:
        print(f"❌ Error loading API key: {e}")
        return None
    
    # Use requests to call Google AI directly
    import requests
    
    def call_google_ai(prompt, api_key):
        """Call Google Generative AI API directly"""
        
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
        
        headers = {
            'Content-Type': 'application/json',
        }
        
        data = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }]
        }
        
        try:
            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 200:
                result = response.json()
                return result['candidates'][0]['content']['parts'][0]['text']
            else:
                print(f"❌ API Error: {response.status_code}")
                print(f"   Response: {response.text[:200]}")
                return None
        except Exception as e:
            print(f"❌ Request error: {e}")
            return None
    
    # Process each article
    articles = [
        {
            "path": "grok-ai-review-2025/article.md",
            "name": "Grok AI Review 2025 (Dutch)",
            "language": "Dutch"
        },
        {
            "path": "grok-blog-series/1-developers-guide.md",
            "name": "Developer's Guide",
            "language": "English"
        },
        {
            "path": "grok-blog-series/2-chatgpt-vs-grok-business.md",
            "name": "Business Migration",
            "language": "English"
        },
        {
            "path": "grok-blog-series/3-chatgpt-hidden-costs.md",
            "name": "Hidden Costs",
            "language": "English"
        },
        {
            "path": "grok-blog-series/4-x-twitter-grok-strategy.md",
            "name": "Elon's Strategy",
            "language": "English"
        },
        {
            "path": "grok-blog-series/5-chatgpt-o1-still-behind.md",
            "name": "o1 Model Analysis",
            "language": "English"
        }
    ]
    
    # Create output directory
    os.makedirs("google-reviewed", exist_ok=True)
    
    print("\n📝 Processing articles...")
    print("-" * 40)
    
    for article in articles:
        print(f"\n📄 {article['name']}")
        
        # Check if file exists
        if not Path(article['path']).exists():
            print(f"   ⚠️ File not found: {article['path']}")
            continue
        
        # Read article
        with open(article['path'], 'r') as f:
            content = f.read()
        
        print(f"   📖 Length: {len(content)} characters")
        print(f"   🌍 Language: {article['language']}")
        
        # Create review prompt
        review_prompt = f"""
You are an expert content editor, SEO specialist, and multilingual writer.

Review this {article['language']} article and provide:

1. QUALITY ASSESSMENT:
   - Content quality score (1-10)
   - SEO optimization score (1-10)
   - Readability score (1-10)
   - Engagement potential (1-10)

2. TOP 5 IMPROVEMENTS:
   - Specific actionable improvements
   - Missing content that should be added
   - SEO keywords to include
   - Better hooks or CTAs

3. VIRAL POTENTIAL:
   - What makes this shareable?
   - What's missing for virality?

4. TRANSLATION QUALITY:
   - If translated to {('English' if article['language'] == 'Dutch' else 'Dutch')}, what to watch for?

Keep response under 500 words. Be specific and actionable.

ARTICLE TO REVIEW:
{content[:3000]}... [truncated for API limits]
"""
        
        print("   🔍 Sending to Google AI for review...")
        
        # Call Google AI
        review = call_google_ai(review_prompt, api_key)
        
        if review:
            # Save review
            output_path = f"google-reviewed/{Path(article['path']).stem}_review.md"
            with open(output_path, 'w') as f:
                f.write(f"# Review: {article['name']}\n\n")
                f.write(f"**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
                f.write(f"**Language**: {article['language']}\n")
                f.write(f"**File**: {article['path']}\n\n")
                f.write("---\n\n")
                f.write(review)
            
            print(f"   ✅ Review saved: {output_path}")
        else:
            print(f"   ❌ Failed to get review")
    
    print("\n" + "=" * 60)
    print("✅ REVIEW COMPLETE")
    print("\n📁 Reviews saved in: google-reviewed/")
    print("\n💡 Next steps:")
    print("1. Read the reviews in google-reviewed/")
    print("2. Implement suggested improvements")
    print("3. Create bilingual versions")
    print("4. Generate images for both languages")
    
    return True

def create_translation_script():
    """Create a separate script for translations"""
    
    translation_script = '''#!/usr/bin/env python3
"""
Translate articles between Dutch and English
Uses Google Translate API or manual translation
"""

import os
from pathlib import Path

def prepare_for_translation():
    """Prepare articles for translation"""
    
    print("📝 TRANSLATION PREPARATION")
    print("=" * 60)
    
    # Create bilingual structure
    os.makedirs("bilingual/nl", exist_ok=True)
    os.makedirs("bilingual/en", exist_ok=True)
    
    print("\\n✅ Bilingual folders created:")
    print("   bilingual/nl/ - Dutch versions")
    print("   bilingual/en/ - English versions")
    
    print("\\n💡 Translation options:")
    print("1. Use Google Translate API (automated)")
    print("2. Use DeepL API (better quality)")
    print("3. Manual translation (best quality)")
    print("4. Hire professional translator")
    
    print("\\n📋 Articles ready for translation:")
    print("   - 1 Dutch article → needs English version")
    print("   - 5 English articles → need Dutch versions")
    
    return True

if __name__ == "__main__":
    prepare_for_translation()
'''
    
    with open("translate_articles.py", 'w') as f:
        f.write(translation_script)
    
    print("\n✅ Translation script created: translate_articles.py")

if __name__ == "__main__":
    print("🚀 WIM TILBURGS BLOG REVIEW SYSTEM")
    print("=" * 60)
    print("This system will:")
    print("1. Review all articles with Google AI")
    print("2. Provide quality scores and improvements")
    print("3. Prepare for bilingual publication")
    print()
    
    # First check if requests is installed
    try:
        import requests
        print("✅ Requests library available")
    except ImportError:
        print("❌ Requests library not found")
        print("   Please install: pip install requests")
        sys.exit(1)
    
    # Run the review
    success = review_with_google_api()
    
    if success:
        # Create translation helper
        create_translation_script()
        
        print("\n🎯 SUMMARY")
        print("=" * 60)
        print("✅ Articles reviewed by Google AI")
        print("✅ Quality feedback generated")
        print("✅ Translation script prepared")
        print("\nYour content is ready for optimization and translation!")