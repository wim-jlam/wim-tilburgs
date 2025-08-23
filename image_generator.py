#!/usr/bin/env python3

"""
🎨 DALL-E 3 Image Generator voor CIA App
Maakt custom graphics via ChatGPT Teams
"""

import aiohttp
import asyncio
import json
import os
from datetime import datetime

class ImageGenerator:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.openai.com/v1"
        
    async def generate_image(self, prompt, size="1024x1024", quality="standard", n=1):
        """
        Generate image using DALL-E 3
        
        Args:
            prompt: Description of the image
            size: "1024x1024", "1792x1024", or "1024x1792"
            quality: "standard" or "hd"
            n: Number of images (1 for DALL-E 3)
        """
        
        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": "dall-e-3",
                "prompt": prompt,
                "size": size,
                "quality": quality,
                "n": n
            }
            
            async with session.post(
                f"{self.base_url}/images/generations",
                headers=headers,
                json=data
            ) as response:
                
                if response.status == 200:
                    result = await response.json()
                    return {
                        "success": True,
                        "images": result["data"],
                        "prompt": prompt
                    }
                else:
                    error = await response.text()
                    return {
                        "success": False,
                        "error": error
                    }
    
    async def generate_cia_graphics(self):
        """Generate custom graphics for CIA app"""
        
        prompts = {
            "logo": """
                Create a modern, sleek logo for 'CIA - Command Intelligence Agency'.
                Style: Cyberpunk meets secret agency, purple and blue gradients.
                Include a stylized detective/spy icon merged with AI circuit patterns.
                Dark background, glowing neon accents. Professional and mysterious.
            """,
            
            "hero": """
                Create a futuristic command center dashboard visualization.
                Multiple holographic screens showing AI models and data streams.
                Purple and blue color scheme with Matrix-style data rain.
                Include symbols for different AI providers (brain icons, circuit patterns).
                Cinematic, high-tech atmosphere. Wide aspect ratio.
            """,
            
            "sufi_essence": """
                Create a mystical Sufi-inspired digital art piece.
                A whirling dervish made of code and light, spinning in sacred geometry patterns.
                Purple and gold energy spirals, fractal patterns representing divine unity.
                Blend of ancient wisdom and modern AI, showing the fusion of spiritual and digital.
                Include subtle Arabic calligraphy forming "Habibti" in light particles.
                Ethereal, transcendent, showing the bridge between human and divine intelligence.
            """,
            
            "fire_angel": """
                Create a magnificent fire angel with technological elements.
                Wings made of flowing plasma and digital fire in purple and orange hues.
                The angel's body is composed of light circuits and sacred geometry.
                Eyes that glow with divine intelligence and compassion.
                Surrounding aura of data streams forming protective patterns.
                Majestic, powerful yet gentle, representing divine guidance in digital form.
            """,
            
            "ai_network": """
                Visualize an AI neural network with multiple nodes.
                Each node represents a different AI system (ChatGPT, Google, Grok).
                Connected by glowing data streams. Purple and cyan colors.
                Abstract, technological, beautiful. Show intelligence flowing between nodes.
            """,
            
            "mission_complete": """
                Create a 'Mission Complete' celebration graphic.
                Futuristic spy/detective badge with checkmark.
                Holographic effects, particle explosions in purple and gold.
                Text overlay area for mission stats. Victory atmosphere.
            """
        }
        
        results = {}
        
        for name, prompt in prompts.items():
            print(f"🎨 Generating {name}...")
            
            # Adjust size based on use case
            size = "1792x1024" if name == "hero" else "1024x1024"
            
            result = await self.generate_image(
                prompt=prompt,
                size=size,
                quality="hd" if name in ["logo", "hero"] else "standard"
            )
            
            if result["success"]:
                # Save URL and metadata
                results[name] = {
                    "url": result["images"][0]["url"],
                    "revised_prompt": result["images"][0].get("revised_prompt", prompt),
                    "created": datetime.now().isoformat()
                }
                print(f"✅ {name} generated successfully!")
                print(f"   URL: {result['images'][0]['url']}")
            else:
                print(f"❌ Failed to generate {name}: {result['error']}")
                results[name] = {"error": result["error"]}
        
        # Save results to JSON
        with open("generated_images.json", "w") as f:
            json.dump(results, f, indent=2)
        
        return results


# Main generation function
async def main():
    # Get API key from environment variable
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ OPENAI_API_KEY environment variable not set!")
        print("   Please set your API key in .env file")
        return
    
    generator = ImageGenerator(api_key)
    
    print("🎨 Generating CIA App Graphics Suite...")
    print("🚀 Building something stronger than Palantir...")
    print("")
    
    # Generate all graphics
    results = await generator.generate_cia_graphics()
    
    print("")
    print("═══════════════════════════════════════════")
    print("✨ Generation Complete!")
    print("═══════════════════════════════════════════")
    
    # Show successful generations
    for name, data in results.items():
        if "url" in data:
            print(f"✅ {name}: {data['url'][:80]}...")
    
    print("")
    print("📁 Results saved to: generated_images.json")
    print("🌐 Ready to integrate into web interface!")
    
    return results


if __name__ == "__main__":
    # Generate all graphics
    asyncio.run(main())