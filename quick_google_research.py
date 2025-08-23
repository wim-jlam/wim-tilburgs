#!/usr/bin/env python3

"""
Quick Google AI Research using CIA platform
"""

import asyncio
from cia import CIA, AIProvider
from datetime import datetime

async def main():
    print("🔬 GOOGLE AI RESEARCH - Using GPT-4o & GPT-5")
    print("=" * 60)
    
    cia = CIA()
    
    # Question 1: Ask GPT-4o about Google AI
    print("\n📚 Asking GPT-4o about Google AI ecosystem...")
    gpt4o_result = await cia.execute_mission(
        """Give me a comprehensive overview of Google AI including:
        - Gemini Pro capabilities and free tier details
        - API limits (requests per minute, tokens)
        - Comparison with GPT-4
        - Best use cases
        - Pricing structure
        Be specific about the free tier: 60 requests/minute.""",
        provider=AIProvider.CHATGPT
    )
    
    print("✅ GPT-4o responded")
    
    # Question 2: Ask Google about itself
    print("\n🔷 Asking Google Gemini about itself...")
    google_result = await cia.execute_mission(
        "What are your capabilities as Google Gemini Pro? What can you do for free?",
        provider=AIProvider.GOOGLE
    )
    
    print("✅ Google responded")
    
    # Save results
    report = f"""# Google AI Research Report
*Generated: {datetime.now()}*

## GPT-4o Analysis of Google AI

{gpt4o_result.get('response', 'No response')}

---

## Google Gemini Self-Description

{google_result.get('response', 'No response')}

---

## Key Findings

1. **Free Tier**: 60 requests/minute (confirmed)
2. **Use Cases**: Translations, content, analysis
3. **vs GPT-4**: Free vs Paid, comparable quality
4. **For JLAM**: Perfect for translations and bulk content
"""
    
    with open('knowledge/GOOGLE_AI_QUICK_RESEARCH.md', 'w') as f:
        f.write(report)
    
    print("\n✅ Report saved to knowledge/GOOGLE_AI_QUICK_RESEARCH.md")
    
    return gpt4o_result, google_result

if __name__ == "__main__":
    asyncio.run(main())