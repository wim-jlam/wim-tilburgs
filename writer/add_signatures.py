#!/usr/bin/env python3
"""
Add W.R.I.T.E.R. signatures to all blog articles
"""

import os
from pathlib import Path
from datetime import datetime

def add_writer_signature(filepath, language="en"):
    """Add W.R.I.T.E.R. signature to an article"""
    
    # Read original content
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Check if already has signature
    if "W.R.I.T.E.R." in content:
        print(f"   ⏭️  Already signed")
        return False
    
    # Choose signature based on language
    if language == "nl":
        signature = """

---

*Dit artikel is gemaakt met **W.R.I.T.E.R.***  
*Wim's Revolutionaire Intelligente Tekst Engineering Robot*

**W.R.I.T.E.R.** combineert de kracht van:
- 🤖 **Grok** - Real-time data van X/Twitter
- 💬 **ChatGPT** - Creatieve content generatie
- 🎓 **Claude** - Genuanceerde analyse
- 🔍 **Gemini** - Diepgaand onderzoek

*Build. Write. Disrupt.*

---"""
    else:
        signature = """

---

*This article was created with **W.R.I.T.E.R.***  
*Wim's Revolutionary Intelligent Text Engineering Robot*

**W.R.I.T.E.R.** combines the power of:
- 🤖 **Grok** - Real-time X/Twitter data
- 💬 **ChatGPT** - Creative content generation
- 🎓 **Claude** - Nuanced analysis
- 🔍 **Gemini** - Deep research

*Build. Write. Disrupt.*

---"""
    
    # Add signature
    signed_content = content + signature
    
    # Save with signature
    with open(filepath, 'w') as f:
        f.write(signed_content)
    
    return True

def process_all_articles():
    """Add signatures to all blog articles"""
    
    print("🤖 W.R.I.T.E.R. SIGNATURE SYSTEM")
    print("=" * 60)
    print("Adding W.R.I.T.E.R. signatures to all articles...")
    print()
    
    # Articles to sign
    articles = [
        ("../blog/grok-ai-review-2025/article.md", "nl"),
        ("../blog/grok-blog-series/1-developers-guide.md", "en"),
        ("../blog/grok-blog-series/2-chatgpt-vs-grok-business.md", "en"),
        ("../blog/grok-blog-series/3-chatgpt-hidden-costs.md", "en"),
        ("../blog/grok-blog-series/4-x-twitter-grok-strategy.md", "en"),
        ("../blog/grok-blog-series/5-chatgpt-o1-still-behind.md", "en")
    ]
    
    signed_count = 0
    
    for filepath, language in articles:
        article_name = Path(filepath).stem
        print(f"📝 {article_name}")
        
        full_path = Path(__file__).parent / filepath
        
        if not full_path.exists():
            print(f"   ❌ File not found")
            continue
        
        if add_writer_signature(full_path, language):
            print(f"   ✅ Signed with W.R.I.T.E.R.")
            signed_count += 1
    
    print()
    print("=" * 60)
    print(f"✅ COMPLETE: {signed_count} articles signed")
    print()
    print("📋 Signature includes:")
    print("   • W.R.I.T.E.R. branding (with periods)")
    print("   • AI models used")
    print("   • Tagline: Build. Write. Disrupt.")
    print()
    print("🎯 Articles now show they were created by W.R.I.T.E.R.!")
    
    return signed_count

def create_writer_badge():
    """Create a W.R.I.T.E.R. badge/logo description"""
    
    badge = """# W.R.I.T.E.R. Badge Design

## Visual Identity

### Logo Concept
```
 W.R.I.T.E.R.
 [AI POWERED]
```

### Color Scheme
- Primary: Electric Blue (#00D4FF) - Like Arc Reactor
- Secondary: Gold (#FFD700) - Iron Man colors
- Accent: Purple (#8B5CF6) - AI/Tech vibe
- Text: White/Black for contrast

### Badge Variations

1. **Full Badge** (for articles)
   ```
   ┌─────────────────────────┐
   │     W.R.I.T.E.R.       │
   │   [AI CONTENT SYSTEM]   │
   └─────────────────────────┘
   ```

2. **Compact Badge** (for social)
   ```
   [W.R.I.T.E.R.]
   ```

3. **Icon Only** (for apps)
   ```
   [W]
   ```

### Usage
- Always include periods in W.R.I.T.E.R.
- Can be placed at article top or bottom
- Should link to W.R.I.T.E.R. documentation
- Include version number for technical content

### ASCII Art Version
```
╔═══════════════════════════════╗
║        W.R.I.T.E.R.          ║
║   AI-Powered Content Robot    ║
║     Build. Write. Disrupt.    ║
╚═══════════════════════════════╝
```
"""
    
    with open("badge.md", 'w') as f:
        f.write(badge)
    
    print("\n🎨 W.R.I.T.E.R. badge design saved to badge.md")

if __name__ == "__main__":
    # Add signatures
    process_all_articles()
    
    # Create badge design
    create_writer_badge()
    
    print("\n🚀 W.R.I.T.E.R. is ready!")
    print("   Your AI content creation system is operational.")
    print("   'Sir, shall we write something amazing?'")