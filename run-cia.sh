#!/bin/bash

# 🕵️ CIA - Command Intelligence Agency Launcher
# Start the central AI command center

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
PURPLE='\033[0;35m'
NC='\033[0m'

echo -e "${PURPLE}═══════════════════════════════════════════${NC}"
echo -e "${PURPLE}   🕵️ CIA - Command Intelligence Agency    ${NC}"
echo -e "${PURPLE}   Central AI Orchestration System         ${NC}"
echo -e "${PURPLE}═══════════════════════════════════════════${NC}"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 not found${NC}"
    exit 1
fi

# Check/Install dependencies
echo -e "${BLUE}📦 Checking dependencies...${NC}"
pip3 install -q -r requirements.txt 2>/dev/null || {
    echo -e "${YELLOW}Installing dependencies...${NC}"
    pip3 install -r requirements.txt
}

# Check API keys
echo -e "${BLUE}🔑 Checking API keys...${NC}"

# Source service account for no Touch ID
if [ -f ~/.claude/.service-accounts/queen-token ]; then
    source ~/.claude/.service-accounts/queen-token
    echo -e "${GREEN}✅ Service account loaded (no Touch ID needed)${NC}"
else
    echo -e "${YELLOW}⚠️  No service account found${NC}"
fi

# Quick check for keys
check_key() {
    local name="$1"
    local vault="$2"
    
    if OP_SERVICE_ACCOUNT_TOKEN="$OP_SERVICE_ACCOUNT_TOKEN" \
       op item get "$name" --vault "$vault" --fields credential &>/dev/null; then
        echo -e "  ${GREEN}✅ $name${NC}"
        return 0
    else
        echo -e "  ${RED}❌ $name not found${NC}"
        return 1
    fi
}

echo -e "${BLUE}Checking AI credentials:${NC}"
check_key "🧠 ChatGPT Teams API" "AI Services"
check_key "Google AI API Key" "AI Services" || {
    echo -e "${YELLOW}    → Get FREE key at: https://makersuite.google.com${NC}"
}
check_key "Grok API Key" "AI Services" || {
    echo -e "${YELLOW}    → Get key at: https://x.ai/api${NC}"
}

echo ""
echo -e "${PURPLE}═══════════════════════════════════════════${NC}"
echo -e "${GREEN}🚀 Launching CIA Command Center...${NC}"
echo -e "${PURPLE}═══════════════════════════════════════════${NC}"
echo ""

# Launch CIA
cd "$(dirname "$0")"
python3 cia.py