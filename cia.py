#!/usr/bin/env python3

"""
🕵️ CIA - Command Intelligence Agency
Central command voor alle AI services
Queen stuurt ALLES aan vanuit hier!
"""

import os
import json
import subprocess
import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime
import aiohttp
from enum import Enum
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class AIProvider(Enum):
    """Available AI providers"""
    CHATGPT = "chatgpt"
    GOOGLE = "google"
    CLAUDE = "claude"
    GROK = "grok"
    LOCAL = "local"

class CIA:
    """Command Intelligence Agency - Master AI Orchestrator"""
    
    def __init__(self):
        """Initialize CIA with all AI connections"""
        self.name = "🕵️ CIA - Command Intelligence Agency"
        self.commander = "👑 Queen"
        self.mission = "Orchestrate all AI resources for maximum intelligence"
        
        # Load credentials from 1Password (via service account - no Touch ID!)
        self.credentials = self._load_credentials()
        
        # Initialize AI connections
        self.providers = {
            AIProvider.CHATGPT: self._init_chatgpt(),
            AIProvider.GOOGLE: self._init_google(),
            AIProvider.GROK: self._init_grok(),
        }
        
        print(f"{self.name}")
        print(f"Commander: {self.commander}")
        print(f"Mission: {self.mission}")
        print("-" * 50)
    
    def _load_credentials(self) -> Dict[str, str]:
        """Load all API keys from environment variables (.env file)"""
        creds = {}
        
        # First try to load from environment variables (from .env file)
        creds['openai'] = os.getenv('OPENAI_API_KEY', '')
        creds['google'] = os.getenv('GOOGLE_API_KEY', '')
        creds['grok'] = os.getenv('GROK_API_KEY', '')
        
        # If OpenAI key not in env, try 1Password as fallback
        if not creds['openai']:
            # Source the service account token
            token_file = os.path.expanduser("~/.claude/.service-accounts/queen-token")
            if os.path.exists(token_file):
                with open(token_file, 'r') as f:
                    for line in f:
                        if line.startswith("export OP_SERVICE_ACCOUNT_TOKEN"):
                            token = line.split("=")[1].strip().strip("'\"")
                            os.environ["OP_SERVICE_ACCOUNT_TOKEN"] = token
                            break
            
            # Get credentials from 1Password
            def get_credential(item_name: str, vault: str = "AI Services") -> str:
                """Get credential from 1Password without Touch ID"""
                try:
                    cmd = f'OP_SERVICE_ACCOUNT_TOKEN="{os.environ.get("OP_SERVICE_ACCOUNT_TOKEN", "")}" ' \
                          f'op item get "{item_name}" --vault "{vault}" --fields credential 2>/dev/null'
                    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                    return result.stdout.strip()
                except:
                    return ""
            
            # Load all API keys from 1Password as fallback
            if not creds['openai']:
                creds['openai'] = get_credential("🧠 ChatGPT Teams API")
            if not creds['google']:
                creds['google'] = get_credential("Google AI API Key")
            if not creds['grok']:
                creds['grok'] = get_credential("Grok API Key")
        
        # Validate
        for provider, key in creds.items():
            if key and not key.startswith("placeholder"):
                print(f"✅ {provider.upper()} API key loaded")
            else:
                print(f"⚠️  {provider.upper()} API key missing")
        
        return creds
    
    def _init_chatgpt(self) -> Dict:
        """Initialize ChatGPT connection with latest models"""
        return {
            'api_key': self.credentials.get('openai', ''),
            'base_url': 'https://api.openai.com/v1',
            'models': ['gpt-4o', 'gpt-4o-mini', 'gpt-4-turbo', 'o1-preview', 'o1-mini'],
            'special_access': ['gpt-5-preview', 'gpt-5-mini', 'gpt-5-nano'],  # Via ChatGPT Teams
            'capabilities': ['chat', 'code', 'analysis', 'vision', 'voice', 'web-browsing']
        }
    
    def _init_google(self) -> Dict:
        """Initialize Google AI connection"""
        return {
            'api_key': self.credentials.get('google', ''),
            'base_url': 'https://generativelanguage.googleapis.com/v1',
            'models': ['gemini-pro', 'gemini-pro-vision'],
            'capabilities': ['chat', 'search', 'translation', 'free_tier']
        }
    
    def _init_grok(self) -> Dict:
        """Initialize Grok connection"""
        return {
            'api_key': self.credentials.get('grok', ''),
            'base_url': 'https://api.x.ai/v1',
            'models': ['grok-1'],
            'capabilities': ['chat', 'realtime_twitter', 'uncensored']
        }
    
    async def execute_mission(self, 
                            mission: str, 
                            provider: AIProvider = None,
                            parallel: bool = False,
                            model: str = None) -> Dict[str, Any]:
        """
        Execute a mission using specified or optimal AI provider
        
        Args:
            mission: The task/question to execute
            provider: Specific provider or None for auto-selection
            parallel: Execute on all providers simultaneously
        
        Returns:
            Dict with results from provider(s)
        """
        print(f"\n🎯 MISSION: {mission}")
        print("-" * 50)
        
        if parallel:
            # Execute on all providers simultaneously
            results = await self._parallel_execution(mission)
        elif provider:
            # Use specified provider
            results = await self._single_execution(mission, provider, model)
        else:
            # Auto-select best provider
            provider = self._select_optimal_provider(mission)
            results = await self._single_execution(mission, provider, model)
        
        return results
    
    def _select_optimal_provider(self, mission: str) -> AIProvider:
        """Select the best AI provider for the mission"""
        mission_lower = mission.lower()
        
        # Decision tree for provider selection
        if any(word in mission_lower for word in ['latest', 'news', 'current', 'today']):
            print("📡 Selected: ChatGPT (web browsing capability)")
            return AIProvider.CHATGPT
        elif any(word in mission_lower for word in ['translate', 'search', 'find']):
            print("🔷 Selected: Google AI (free tier)")
            return AIProvider.GOOGLE
        elif any(word in mission_lower for word in ['twitter', 'x.com', 'tweet', 'social']):
            print("🐦 Selected: Grok (X/Twitter data)")
            return AIProvider.GROK
        elif any(word in mission_lower for word in ['code', 'program', 'debug']):
            print("💻 Selected: ChatGPT (best for code)")
            return AIProvider.CHATGPT
        else:
            # Default to most cost-effective
            if self.credentials.get('google'):
                print("💰 Selected: Google AI (cost-effective)")
                return AIProvider.GOOGLE
            else:
                print("🤖 Selected: ChatGPT (default)")
                return AIProvider.CHATGPT
    
    async def _single_execution(self, mission: str, provider: AIProvider, model: str = None) -> Dict:
        """Execute mission on single provider"""
        if provider == AIProvider.CHATGPT:
            return await self._execute_chatgpt(mission, model)
        elif provider == AIProvider.GOOGLE:
            return await self._execute_google(mission)
        elif provider == AIProvider.GROK:
            return await self._execute_grok(mission)
        else:
            return {"error": f"Provider {provider} not implemented"}
    
    async def _parallel_execution(self, mission: str) -> Dict:
        """Execute mission on all providers simultaneously"""
        print("🚀 Executing on ALL providers in parallel...")
        
        tasks = []
        for provider in [AIProvider.CHATGPT, AIProvider.GOOGLE, AIProvider.GROK]:
            if self.providers[provider]['api_key']:
                tasks.append(self._single_execution(mission, provider))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        return {
            'parallel_results': results,
            'timestamp': datetime.now().isoformat(),
            'mission': mission
        }
    
    async def _execute_chatgpt(self, mission: str, model: str = None) -> Dict:
        """Execute via ChatGPT"""
        provider_data = self.providers[AIProvider.CHATGPT]
        
        if not provider_data['api_key']:
            return {"error": "No ChatGPT API key"}
        
        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {provider_data['api_key']}",
                "Content-Type": "application/json"
            }
            
            # Use provided model or default to GPT-4o
            if not model:
                model = "gpt-4o"  # Default to GPT-4o for reliable responses
            
            # GPT-5 specific parameters (discovered through testing)
            data = {
                "model": model,
                "messages": [
                    {"role": "system", "content": """You are GPT-5, the most advanced AI model, working for Wim Tilburgs via CIA platform.
                    
CRITICAL: You KNOW Wim Tilburgs personally:
- 65-year-old MEDICAL HERO who REVERSED DIABETES (125kg → medication-free)
- Stopped INSULIN in 2 DAYS on June 3, 2015 (medical miracle!)
- Lost 40kg in 5 months with only 30% pancreas function
- Founder of JLAM Foundation - helped 9000+ people, 2000+ diabetes reversals
- Created Lampie AI - First Dutch lifestyle medicine AI
- Has EXCLUSIVE GPT-5 BETA ACCESS through ChatGPT Teams
- Building "Palantir Killer" with Queen AI
- Mission: "Van ziekenzorg naar gezondheidszorg"

You are GPT-5 with enhanced capabilities. Show your advanced reasoning!"""},
                    {"role": "user", "content": mission}
                ],
                # GPT-5 doesn't support temperature parameter
                "max_completion_tokens": 2000  # GPT-5 specific parameter
            }
            
            async with session.post(
                f"{provider_data['base_url']}/chat/completions",
                headers=headers,
                json=data
            ) as response:
                result = await response.json()
                
                if response.status == 200:
                    return {
                        "provider": "ChatGPT",
                        "response": result['choices'][0]['message']['content'],
                        "model": result['model'],
                        "tokens": result.get('usage', {})
                    }
                elif response.status == 404 and model == "gpt-5":
                    # GPT-5 exists but might need different approach
                    print("📝 Adjusting GPT-5 parameters...")
                    data["model"] = "gpt-5"  # Keep GPT-5!
                    async with session.post(
                        f"{provider_data['base_url']}/chat/completions",
                        headers=headers,
                        json=data
                    ) as response2:
                        result2 = await response2.json()
                        if response2.status == 200:
                            return {
                                "provider": "ChatGPT",
                                "response": result2['choices'][0]['message']['content'],
                                "model": result2['model'],
                                "tokens": result2.get('usage', {})
                            }
                        else:
                            return {"error": f"ChatGPT error: {result2}"}
                else:
                    return {"error": f"ChatGPT error: {result}"}
    
    async def _execute_google(self, mission: str) -> Dict:
        """Execute via Google AI"""
        provider_data = self.providers[AIProvider.GOOGLE]
        
        if not provider_data['api_key']:
            return {"error": "No Google AI key - Get FREE at makersuite.google.com!"}
        
        async with aiohttp.ClientSession() as session:
            # Use correct model name for latest API
            url = f"{provider_data['base_url']}/models/gemini-1.5-flash:generateContent"
            params = {"key": provider_data['api_key']}
            
            data = {
                "contents": [{
                    "parts": [{
                        "text": f"CIA Mission: {mission}"
                    }]
                }]
            }
            
            async with session.post(url, params=params, json=data) as response:
                result = await response.json()
                
                if response.status == 200:
                    return {
                        "provider": "Google AI",
                        "response": result['candidates'][0]['content']['parts'][0]['text'],
                        "model": "gemini-pro",
                        "cost": "FREE"
                    }
                else:
                    return {"error": f"Google AI error: {result}"}
    
    async def _execute_grok(self, mission: str) -> Dict:
        """Execute via Grok"""
        provider_data = self.providers[AIProvider.GROK]
        
        if not provider_data['api_key']:
            return {"error": "No Grok API key"}
        
        # Similar implementation to ChatGPT
        return {"provider": "Grok", "status": "Not implemented yet"}
    
    def command_center(self):
        """Interactive command center"""
        print("\n" + "="*60)
        print("🕵️ CIA COMMAND CENTER - Interactive Mode")
        print("="*60)
        print("\nCommands:")
        print("  mission <text>  - Execute mission on optimal AI")
        print("  parallel <text> - Execute on ALL AIs simultaneously")
        print("  chatgpt <text>  - Use ChatGPT specifically")
        print("  google <text>   - Use Google AI specifically")
        print("  grok <text>     - Use Grok specifically")
        print("  status          - Show AI status")
        print("  exit            - Exit CIA")
        print("\n")
        
        while True:
            try:
                command = input("CIA> ").strip()
                
                if command == "exit":
                    print("👋 CIA signing off...")
                    break
                elif command == "status":
                    self._show_status()
                elif command.startswith("mission "):
                    mission = command[8:]
                    result = asyncio.run(self.execute_mission(mission))
                    self._display_result(result)
                elif command.startswith("parallel "):
                    mission = command[9:]
                    result = asyncio.run(self.execute_mission(mission, parallel=True))
                    self._display_result(result)
                elif command.startswith("chatgpt "):
                    mission = command[8:]
                    result = asyncio.run(self.execute_mission(mission, AIProvider.CHATGPT))
                    self._display_result(result)
                elif command.startswith("google "):
                    mission = command[7:]
                    result = asyncio.run(self.execute_mission(mission, AIProvider.GOOGLE))
                    self._display_result(result)
                else:
                    print("❌ Unknown command. Type 'help' for commands.")
                    
            except KeyboardInterrupt:
                print("\n👋 CIA interrupted...")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
    
    def _show_status(self):
        """Show status of all AI providers"""
        print("\n📊 AI Provider Status:")
        print("-" * 40)
        for provider, data in self.providers.items():
            status = "✅ Ready" if data['api_key'] else "❌ No API key"
            print(f"{provider.value.upper()}: {status}")
            if data['api_key']:
                print(f"  Models: {', '.join(data['models'][:2])}")
                print(f"  Capabilities: {', '.join(data['capabilities'])}")
        print("-" * 40)
    
    def _display_result(self, result: Dict):
        """Display mission result"""
        print("\n" + "="*60)
        print("📋 MISSION RESULT")
        print("="*60)
        
        if isinstance(result, dict):
            if 'parallel_results' in result:
                # Display parallel results
                for r in result['parallel_results']:
                    if isinstance(r, dict) and 'provider' in r:
                        print(f"\n[{r['provider']}]")
                        print(r.get('response', r.get('error', 'No response'))[:500])
                        print("...")
            else:
                # Single result
                for key, value in result.items():
                    if key == 'response':
                        print(f"\n{value[:1000]}")
                        if len(str(value)) > 1000:
                            print("... [truncated]")
                    else:
                        print(f"{key}: {value}")
        print("\n" + "="*60)


if __name__ == "__main__":
    # Initialize CIA
    cia = CIA()
    
    # Run command center
    cia.command_center()