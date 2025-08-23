#!/usr/bin/env python3
"""
Simple Grok AI Research using CIA
"""

import asyncio
from datetime import datetime
from cia import CIA

async def main():
    print("🔬 GROK AI RESEARCH - SIMPLIFIED")
    print("=" * 60)
    
    cia = CIA()
    
    # GPT-4o research (GPT-5 seems to have issues with complex queries)
    print("\n🤖 Asking GPT-4o about Grok...")
    gpt4_prompt = """Research Grok AI from xAI/X.com. Provide information about:
    1. What is Grok AI and who created it
    2. Key features and capabilities
    3. How to get API access
    4. Pricing and availability
    5. How it compares to GPT-4, Claude, and Gemini
    6. Code example for using the Grok API
    Be comprehensive and practical."""
    
    try:
        gpt4_result = await cia.execute_mission(gpt4_prompt, provider="chatgpt")
        
        # Extract the response text
        if isinstance(gpt4_result, dict):
            response_text = gpt4_result.get('response', str(gpt4_result))
        else:
            response_text = str(gpt4_result)
        
        # Save GPT-4 research
        with open("knowledge/GROK_GPT4_RESEARCH.md", "w") as f:
            f.write("# Grok AI Research by GPT-4o\n")
            f.write(f"*Generated: {datetime.now()}*\n\n")
            f.write(response_text)
        print("✅ GPT-4o research saved")
        
    except Exception as e:
        print(f"❌ GPT-4o error: {e}")
    
    # Gemini research
    print("\n🤖 Asking Gemini about Grok...")
    gemini_prompt = """Provide a comprehensive analysis of Grok AI from xAI (Elon Musk's AI company).
    Include:
    - Technical specifications and model sizes
    - Integration with X/Twitter platform
    - Unique features like real-time information
    - API documentation and developer resources
    - Comparison with other large language models
    - Pricing structure and access tiers
    Be detailed and technical."""
    
    try:
        gemini_result = await cia.execute_mission(gemini_prompt, provider="google")
        
        # Extract the response text
        if isinstance(gemini_result, dict):
            response_text = gemini_result.get('response', str(gemini_result))
        else:
            response_text = str(gemini_result)
        
        # Save Gemini research
        with open("knowledge/GROK_GEMINI_RESEARCH.md", "w") as f:
            f.write("# Grok AI Research by Gemini\n")
            f.write(f"*Generated: {datetime.now()}*\n\n")
            f.write(response_text)
        print("✅ Gemini research saved")
        
    except Exception as e:
        print(f"❌ Gemini error: {e}")
    
    print("\n✅ Research complete! Check knowledge/ folder for results.")

if __name__ == "__main__":
    asyncio.run(main())