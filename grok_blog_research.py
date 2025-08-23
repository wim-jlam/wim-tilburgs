#!/usr/bin/env python3
"""
Grok Blog Research - Smart X/Twitter queries for blog content
ZUINIG met €25 credits!
"""

import os
from datetime import datetime
from openai import OpenAI
from load_secrets_from_1password import load_all_secrets

def research_grok_for_blog():
    """Smart queries to get maximum value from Grok for blog"""
    
    # Load API key
    load_all_secrets()
    
    client = OpenAI(
        api_key=os.getenv('GROK_API_KEY'),
        base_url="https://api.x.ai/v1"
    )
    
    print("🔬 GROK BLOG RESEARCH - Maximale waarde uit €25!")
    print("=" * 60)
    
    # ONE SMART QUERY that gets everything we need
    smart_query = """Analyze X/Twitter for a comprehensive blog article about Grok AI. 

Please provide:

1. TRENDING DISCUSSIONS about Grok on X right now:
   - What are users saying about Grok?
   - Most liked/retweeted posts about Grok
   - Common complaints or praise

2. USER EXPERIENCES:
   - Real examples of how people use Grok
   - Comparisons users make with ChatGPT/Claude
   - Success stories or failures

3. ELON MUSK & xAI UPDATES:
   - Latest tweets from @elonmusk about Grok/xAI
   - Official @xai announcements
   - Roadmap hints or teasers

4. DEVELOPER COMMUNITY:
   - What are developers building with Grok API?
   - Code examples being shared
   - Integration tips from the community

5. UNIQUE GROK MOMENTS:
   - Funny or viral Grok responses
   - Examples of Grok's humor/personality
   - Real-time information wins

6. CRITICAL OPINIONS:
   - What AI experts say about Grok
   - Technical critiques
   - Market position analysis

Format as structured data for a blog article. Include specific tweet examples with engagement metrics where relevant."""

    print("📝 Research Query prepared (saving credits with 1 comprehensive query)")
    print("\n🚀 Executing research query...")
    
    try:
        response = client.chat.completions.create(
            model="grok-2",
            messages=[
                {
                    "role": "system", 
                    "content": "You are Grok with real-time X access. Provide comprehensive, factual data with specific examples."
                },
                {
                    "role": "user",
                    "content": smart_query
                }
            ],
            max_tokens=2000,  # Get substantial content but not too much
            temperature=0.3    # Lower temp for factual accuracy
        )
        
        result = response.choices[0].message.content
        
        # Calculate cost
        tokens_used = response.usage.total_tokens
        # Rough estimate: $0.02 per 1K input, $0.10 per 1K output
        cost_usd = (response.usage.prompt_tokens * 0.02 + 
                   response.usage.completion_tokens * 0.10) / 1000
        cost_eur = cost_usd * 0.92
        
        print(f"\n✅ Research complete!")
        print(f"📊 Tokens used: {tokens_used:,}")
        print(f"💰 Cost: €{cost_eur:.3f} (van je €25 budget)")
        print(f"📏 Response length: {len(result)} characters")
        
        # Save to file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"knowledge/GROK_BLOG_RESEARCH_{timestamp}.md"
        
        with open(filename, 'w') as f:
            f.write("# 🔬 Grok Blog Research - Live X/Twitter Data\n")
            f.write(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n")
            f.write(f"*Cost: €{cost_eur:.3f} | Tokens: {tokens_used:,}*\n\n")
            f.write("---\n\n")
            f.write(result)
            f.write("\n\n---\n\n")
            f.write("## Blog Article Outline\n\n")
            f.write("Based on this research, here's the blog structure:\n\n")
            f.write("1. **Intro**: Grok's unique position (real-time X data)\n")
            f.write("2. **User Experiences**: Real stories from X\n")
            f.write("3. **Grok vs Competition**: What users actually say\n")
            f.write("4. **Developer Perspective**: API usage examples\n")
            f.write("5. **The Musk Factor**: Latest from Elon\n")
            f.write("6. **Viral Moments**: Grok's personality in action\n")
            f.write("7. **Critical Analysis**: Balanced view\n")
            f.write("8. **Future Outlook**: Based on X discussions\n")
            f.write("9. **Conclusion**: Is Grok worth it?\n")
        
        print(f"\n📁 Research saved to: {filename}")
        
        # Show preview
        print("\n📋 Preview of research:")
        print("-" * 40)
        print(result[:500] + "...")
        print("-" * 40)
        
        return result
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def main():
    print("🚀 Starting Grok Blog Research")
    print("💡 This will use ~€0.20-0.50 of your €25 credits")
    print("-" * 60)
    
    # Confirm before spending credits
    confirm = input("\n❓ Ready to research? (type 'yes' to continue): ")
    
    if confirm.lower() == 'yes':
        research_grok_for_blog()
        print("\n✅ Research complete! Check knowledge/ folder for results")
        print("💡 Use this data to write an amazing blog about Grok!")
    else:
        print("❌ Research cancelled - no credits spent")

if __name__ == "__main__":
    main()