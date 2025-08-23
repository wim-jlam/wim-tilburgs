#!/usr/bin/env python3
"""
Generate blog images for Grok AI article using DALL-E 3
Creates hero image, social media cards, and article illustrations
"""

import os
import sys
from openai import OpenAI
from datetime import datetime

# Add parent directory to path for imports
sys.path.append('/Users/wimtilburgs/Development/cia-app')

# Try to load from 1Password first
try:
    from load_secrets_from_1password import load_all_secrets
    load_all_secrets()
    print("🔑 Attempting to load OpenAI API key from 1Password...")
except:
    print("⚠️ 1Password integration not available, checking .env file...")

def generate_blog_images(test_mode=False):
    """Generate all images for the Grok AI blog post
    
    Args:
        test_mode: If True, only show prompts without calling API
    """
    
    if not test_mode:
        # Initialize OpenAI client for real generation
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    print("🎨 Generating blog images with DALL-E 3...")
    print("=" * 60)
    
    # Image configurations
    images = [
        {
            "name": "hero-image",
            "size": "1792x1024",  # Blog hero 16:9
            "prompt": """Create a stunning hero image for a tech blog article about Grok AI vs ChatGPT. 
            Show a futuristic battle scene between two AI entities - one representing Grok (edgy, rebellious, 
            with X/Twitter blue accents) and one representing ChatGPT (corporate, polished, green accents). 
            Include subtle references to Elon Musk (Tesla, SpaceX elements). 
            Style: Modern, dramatic, tech-focused, professional blog header.
            Text overlay areas should be left clear for article title."""
        },
        {
            "name": "linkedin-card",
            "size": "1024x1024",  # LinkedIn square
            "prompt": """Design a eye-catching LinkedIn social media card for sharing an article about Grok AI. 
            Feature the Grok logo/mascot in a dynamic pose with X (Twitter) bird logo integrated. 
            Background: Gradient from X blue to purple. 
            Include visual elements suggesting real-time data streams and social media connections.
            Style: Professional but edgy, tech-forward, shareable.
            Leave space for text overlay."""
        },
        {
            "name": "twitter-card",
            "size": "1024x1024",  # X/Twitter square
            "prompt": """Create a viral-worthy Twitter/X card image for Grok AI article. 
            Show Grok as a mischievous AI entity emerging from the X logo, surrounded by trending tweets 
            and real-time data visualizations. Include subtle humor - maybe Grok winking or making a face.
            Colors: X brand blue, black, white with electric accents.
            Style: Meme-able but professional, highly shareable."""
        },
        {
            "name": "comparison-chart",
            "size": "1024x1024",  # Article illustration
            "prompt": """Design a visually striking comparison infographic: Grok AI vs ChatGPT vs Claude vs Gemini.
            Show four AI entities/robots in a lineup, each with distinct personalities:
            - Grok: Rebellious, edgy, X blue
            - ChatGPT: Corporate, polished, green
            - Claude: Thoughtful, purple
            - Gemini: Colorful, Google colors
            Include visual indicators for: price tags (€8 vs €20), real-time data capability, humor level.
            Style: Clean infographic style, easy to understand at a glance."""
        },
        {
            "name": "elon-masterplan",
            "size": "1792x1024",  # Article section image
            "prompt": """Illustrate Elon Musk's AI masterplan with X/Twitter at the center. 
            Show Elon as a chess master moving pieces on a board where the pieces are: 
            X logo, Tesla car, SpaceX rocket, Neuralink chip, all connecting to a central Grok AI brain.
            Background: Space/stars suggesting universal ambition.
            Style: Editorial illustration, slightly dramatic, business magazine quality."""
        },
        {
            "name": "real-time-data",
            "size": "1024x1024",  # Feature highlight
            "prompt": """Visualize Grok AI's real-time data advantage. 
            Show streams of tweets, trending topics, and live data flowing into a Grok AI brain/entity,
            while competitor AIs (shadowed figures) look at old newspapers and outdated books.
            Include clock showing 'NOW' for Grok and 'APRIL 2024' for others.
            Style: Dynamic, data visualization, clear contrast between real-time vs outdated."""
        },
        {
            "name": "instagram-story",
            "size": "1024x1792",  # Instagram story 9:16
            "prompt": """Design a vertical Instagram story image for Grok AI article promotion.
            Feature a smartphone with X app open showing Grok AI interface.
            Surround with comic-style speech bubbles containing provocative Grok responses.
            Price tag showing '€8/month' prominently.
            Style: Mobile-first, Instagram aesthetic, young and trendy, high contrast."""
        },
        {
            "name": "facebook-cover",
            "size": "1792x1024",  # Facebook cover
            "prompt": """Create a Facebook cover image announcing 'I switched from ChatGPT to Grok AI'.
            Show a person's silhouette walking away from a corporate ChatGPT building 
            towards a vibrant, edgy Grok/X headquarters.
            Include visual metaphor of liberation/freedom.
            Style: Storytelling, emotional, shareable on Facebook."""
        }
    ]
    
    # Create images directory
    os.makedirs("images", exist_ok=True)
    
    # Generate each image
    for i, img_config in enumerate(images, 1):
        print(f"\n🖼️ [{i}/8] {img_config['name']}...")
        print(f"   Size: {img_config['size']}")
        
        if test_mode:
            # Test mode: Just show the prompt
            print(f"   📝 PROMPT:")
            print(f"   {'-' * 50}")
            for line in img_config['prompt'].strip().split('\n'):
                print(f"   {line.strip()}")
            print(f"   {'-' * 50}")
            
            # Save prompt to file
            with open(f"images/{img_config['name']}_prompt.txt", 'w') as f:
                f.write(f"Image: {img_config['name']}\n")
                f.write(f"Size: {img_config['size']}\n")
                f.write(f"Quality: HD\n\n")
                f.write("DALL-E 3 Prompt:\n")
                f.write("=" * 60 + "\n")
                f.write(img_config['prompt'])
            print(f"   ✅ Prompt saved to: images/{img_config['name']}_prompt.txt")
        else:
            # Real mode: Generate with DALL-E 3
            try:
                print("   🎨 Calling DALL-E 3 API...")
                response = client.images.generate(
                    model="dall-e-3",
                    prompt=img_config['prompt'],
                    size=img_config['size'],
                    quality="hd",  # High quality for blog
                    n=1
                )
                
                image_url = response.data[0].url
                print(f"   ✅ Generated! URL: {image_url[:50]}...")
                
                # Save URL to file for reference
                with open(f"images/{img_config['name']}_url.txt", 'w') as f:
                    f.write(image_url)
                    f.write(f"\n\nGenerated: {datetime.now()}")
                    f.write(f"\nPrompt: {img_config['prompt'][:200]}...")
                
                # Download the image
                print(f"   📥 Downloading image...")
                import requests
                img_response = requests.get(image_url)
                if img_response.status_code == 200:
                    with open(f"images/{img_config['name']}.png", 'wb') as f:
                        f.write(img_response.content)
                    print(f"   💾 Saved to: images/{img_config['name']}.png")
                
            except Exception as e:
                print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 60)
    
    if test_mode:
        print("✅ Test mode complete - Prompts saved!")
        print("\n📁 Generated files:")
        print("   - 8 prompt files in images/ folder")
        print("\n📋 To generate real images:")
        print("1. Add your OpenAI API key to .env")
        print("2. Run: python generate_images.py")
        print("\n💡 Or copy prompts to ChatGPT Plus for manual generation")
    else:
        print("✅ Image generation complete!")
        print("\n📁 Generated files:")
        print("   - 8 PNG images in images/ folder")
        print("   - 8 URL reference files")
        print("\n📋 Next steps:")
        print("1. Review generated images")
        print("2. Optimize for web (compress)")
        print("3. Add to blog post")
        print("4. Upload to social media platforms")
    
    # Create social media posts file
    create_social_posts()

def create_social_posts():
    """Create social media posts for different platforms"""
    
    posts = """# 📱 Social Media Posts for Grok AI Article

## LinkedIn Post:
```
🚀 I just spent €25 testing Grok AI, and the results shocked me.

While everyone's obsessing over ChatGPT, Elon Musk quietly gave 500 million X users an AI assistant that:

✅ Has real-time data (ChatGPT is stuck in April 2024)
✅ Costs €8/month (vs €20 for ChatGPT Plus)  
✅ Lives where people already are (inside X)
✅ Actually has personality and humor

After 50+ test queries, my verdict: For 80% of use cases, Grok is BETTER than ChatGPT.

Full review with comparison data → [link]

#AI #GrokAI #ChatGPT #TechReview #ArtificialIntelligence
```

## X/Twitter Thread:
```
1/ 🧵 I just spent €25 testing @xai's Grok API

The tech world is looking the wrong way

While everyone counts ChatGPT downloads, @elonmusk quietly deployed the biggest AI distribution in history

500M people now have AI built into their social media

Here's what I found →

2/ First, the basics:
- €8/month with X Premium (vs €20 ChatGPT)
- Real-time data access (this is HUGE)
- 100 messages/day
- Actually funny and honest
- No corporate censorship

But that's not the real story...

3/ The REAL innovation:

Grok doesn't make you go to IT
IT comes to YOU

You're scrolling X, see something interesting, ask Grok about it INSTANTLY

No app switching. No copy-paste. It's just THERE.

4/ My test results after €25 in API credits:

✅ Current events: Grok DESTROYS ChatGPT
✅ Trending topics: Not even close
✅ Personality: Grok is hilarious
❌ Coding: ChatGPT still wins
✅ Price/value: Grok by a mile

5/ The controversy nobody talks about:

Grok knows what you tweet
Sees who you follow
Understands your interests

Privacy nightmare? Yes
Incredibly useful? Also yes

We gave our data to X anyway. At least now we get an AI back.

6/ My prediction:

In 12 months, X won't be a social network with an AI

It'll be an AI with a social network attached

Bank + Payments + Social + AI = Everything App

Elon's not building Twitter 2.0
He's building the Matrix

7/ Bottom line:

Stop waiting. Get X Premium today.

Not for the blue check
Not for less ads
For the AI that knows what's happening NOW

Full review: [link]

What's your take on Grok? 👇
```

## Instagram Caption:
```
Switch your AI, change your life 🤖⚡

I went from ChatGPT ($20/month, outdated) to Grok AI ($8/month, real-time) and I'm never going back.

Swipe for the comparison that'll blow your mind →

The future isn't about having AI.
It's about AI that KNOWS what's happening NOW.

Full review in bio 🔗

#GrokAI #AIRevolution #TechReview #ChatGPT #ElonMusk #FutureTech #ArtificialIntelligence #TechTips #DigitalTransformation #Innovation
```

## Facebook Post:
```
🤖 I just discovered something that's going to change how we all use AI...

Remember when you had to choose between:
- Expensive AI ($20/month for ChatGPT)
- Or outdated free options?

Well, Elon Musk just changed the game.

For €8/month with X Premium, you get Grok AI which:
→ Knows what's happening RIGHT NOW (not months ago)
→ Is built into X (Twitter) - no extra app needed
→ Actually has personality and makes jokes
→ Gives honest answers without corporate filters

I spent €25 testing it thoroughly, comparing with ChatGPT, Claude, and Gemini.

The verdict? For most everyday uses, Grok is BETTER and CHEAPER.

Full detailed review here: [link]

What AI assistant are you using? Let me know in the comments! 👇
```

## YouTube Community Post:
```
🚨 NEW ARTICLE: Grok AI vs ChatGPT - The €25 Test

Just dropped my full review after extensive testing.

Spoiler: The €8 option beats the €20 option 🤯

Read here: [link]

Video review coming next week!
```
"""
    
    with open("social-media/posts.md", 'w') as f:
        f.write(posts)
    
    print("📱 Social media posts created in social-media/posts.md")

if __name__ == "__main__":
    print("🎨 DALL-E 3 Blog Image Generator")
    print("=" * 60)
    
    # Check if OpenAI API key is configured
    # Check API key status
    api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key or api_key == 'your_openai_api_key_here':
        print("\n⚠️ OpenAI API key not configured!")
        print("\n📋 OPTIONS:")
        print("1. Add your OpenAI API key to .env file:")
        print("   OPENAI_API_KEY=sk-proj-...")
        print("\n2. Or use --test mode to see the prompts:")
        print("   python generate_images.py --test")
        print("\n3. Or copy the prompts and use ChatGPT Plus manually")
        
        if len(sys.argv) > 1 and sys.argv[1] == '--test':
            print("\n🧪 TEST MODE - Showing prompts only...")
            generate_blog_images(test_mode=True)
        else:
            print("\n❌ Exiting. Add API key or use --test mode.")
            sys.exit(1)
    else:
        print(f"✅ OpenAI API key found: {api_key[:10]}...")
        print("\n💰 COST ESTIMATE:")
        print("   - 8 HD images × $0.08 = $0.64")
        print("   - Total: ~€0.59")
        print("\n🚀 Generating real images with DALL-E 3...")
        generate_blog_images(test_mode=False)