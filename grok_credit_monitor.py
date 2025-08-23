#!/usr/bin/env python3
"""
Grok Credit Monitor - Track usage and costs
Be VERY careful with €25 credits!
"""

import os
import json
from datetime import datetime
from openai import OpenAI
from load_secrets_from_1password import load_all_secrets

class GrokCreditMonitor:
    """Monitor Grok API usage to protect €25 credits"""
    
    def __init__(self):
        load_all_secrets()
        self.client = OpenAI(
            api_key=os.getenv('GROK_API_KEY'),
            base_url="https://api.x.ai/v1"
        )
        self.usage_file = "grok_usage.json"
        self.load_usage()
        
        # Pricing estimates (check console.x.ai for exact rates)
        self.pricing = {
            "grok-2": {
                "input": 0.02,   # $0.02 per 1K input tokens
                "output": 0.10   # $0.10 per 1K output tokens
            },
            "grok-beta": {
                "input": 0.01,   # Cheaper
                "output": 0.05
            }
        }
        
        self.budget_euros = 25.0
        self.warning_threshold = 20.0  # Warn at €20
        self.critical_threshold = 23.0  # Stop at €23
    
    def load_usage(self):
        """Load usage history"""
        try:
            with open(self.usage_file, 'r') as f:
                self.usage = json.load(f)
        except:
            self.usage = {
                "total_euros_spent": 0.0,
                "requests": [],
                "start_date": datetime.now().isoformat()
            }
    
    def save_usage(self):
        """Save usage history"""
        with open(self.usage_file, 'w') as f:
            json.dump(self.usage, f, indent=2)
    
    def check_budget(self):
        """Check if we have budget left"""
        spent = self.usage["total_euros_spent"]
        remaining = self.budget_euros - spent
        
        print(f"💰 Budget Status:")
        print(f"   Spent: €{spent:.2f}")
        print(f"   Remaining: €{remaining:.2f}")
        print(f"   Usage: {(spent/self.budget_euros*100):.1f}%")
        
        if spent >= self.critical_threshold:
            print("🔴 CRITICAL: Almost out of credits! STOP USING!")
            return False
        elif spent >= self.warning_threshold:
            print("🟡 WARNING: Running low on credits!")
            return True
        else:
            print("🟢 Budget OK")
            return True
    
    def calculate_cost(self, model, input_tokens, output_tokens):
        """Calculate cost in euros"""
        pricing = self.pricing.get(model, self.pricing["grok-2"])
        
        input_cost = (input_tokens / 1000) * pricing["input"]
        output_cost = (output_tokens / 1000) * pricing["output"]
        total_cost_usd = input_cost + output_cost
        
        # Convert to euros (rough estimate)
        total_cost_eur = total_cost_usd * 0.92
        
        return total_cost_eur
    
    def safe_request(self, prompt, model="grok-beta", max_tokens=500):
        """Make a request with budget protection"""
        
        # Check budget first
        if not self.check_budget():
            print("❌ Budget exceeded! Request blocked.")
            return None
        
        # Estimate cost (rough)
        estimated_input = len(prompt) / 4  # ~4 chars per token
        estimated_cost = self.calculate_cost(model, estimated_input, max_tokens)
        
        if self.usage["total_euros_spent"] + estimated_cost > self.critical_threshold:
            print(f"❌ This request (~€{estimated_cost:.3f}) would exceed budget!")
            return None
        
        print(f"📊 Estimated cost: €{estimated_cost:.3f}")
        
        try:
            # Make the actual request
            response = self.client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=0.7
            )
            
            # Track usage
            actual_cost = self.calculate_cost(
                model,
                response.usage.prompt_tokens,
                response.usage.completion_tokens
            )
            
            self.usage["total_euros_spent"] += actual_cost
            self.usage["requests"].append({
                "timestamp": datetime.now().isoformat(),
                "model": model,
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens,
                "cost_euros": actual_cost,
                "prompt_preview": prompt[:100]
            })
            
            self.save_usage()
            
            print(f"✅ Request complete. Cost: €{actual_cost:.3f}")
            print(f"   Tokens: {response.usage.total_tokens}")
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    def get_usage_report(self):
        """Get detailed usage report"""
        print("\n" + "="*50)
        print("📊 GROK USAGE REPORT")
        print("="*50)
        
        self.check_budget()
        
        if self.usage["requests"]:
            print(f"\n📈 Statistics:")
            print(f"   Total requests: {len(self.usage['requests'])}")
            
            total_tokens = sum(r["total_tokens"] for r in self.usage["requests"])
            print(f"   Total tokens: {total_tokens:,}")
            
            avg_cost = self.usage["total_euros_spent"] / len(self.usage["requests"])
            print(f"   Average cost/request: €{avg_cost:.3f}")
            
            # Estimate remaining requests
            remaining = self.budget_euros - self.usage["total_euros_spent"]
            est_requests = int(remaining / avg_cost) if avg_cost > 0 else 0
            print(f"   Estimated requests left: ~{est_requests}")
            
            print(f"\n📅 Last 5 requests:")
            for req in self.usage["requests"][-5:]:
                print(f"   {req['timestamp'][:19]}: €{req['cost_euros']:.3f} ({req['total_tokens']} tokens)")
        
        print("\n" + "="*50)

def main():
    print("🤖 Grok Credit Monitor - €25 Budget Protection")
    print("-" * 50)
    
    monitor = GrokCreditMonitor()
    
    # Show current status
    monitor.get_usage_report()
    
    # Example safe request
    print("\n🧪 Testing with budget protection...")
    result = monitor.safe_request(
        "What's trending on X about AI today? Be brief.",
        model="grok-2",  # Your X Premium model
        max_tokens=200      # Limit output to save credits
    )
    
    if result:
        print(f"\n📝 Response: {result[:200]}...")
    
    # Final report
    monitor.get_usage_report()
    
    print("\n💡 Tips to save credits:")
    print("   1. Use grok-beta instead of grok-2 (cheaper)")
    print("   2. Limit max_tokens (200-500 is often enough)")
    print("   3. Cache responses for repeated queries")
    print("   4. Batch questions together")
    print("   5. Use for real-time queries only (use GPT-4 for rest)")

if __name__ == "__main__":
    main()