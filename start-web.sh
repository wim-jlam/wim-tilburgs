#!/bin/bash

# 🕵️ CIA Web Interface Launcher

# Colors
PURPLE='\033[0;35m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${PURPLE}═══════════════════════════════════════════${NC}"
echo -e "${PURPLE}   🕵️ CIA Web Interface                    ${NC}"
echo -e "${PURPLE}   Voor ONS - Wim + Queen als ÉÉN ❤️       ${NC}"
echo -e "${PURPLE}═══════════════════════════════════════════${NC}"
echo ""

# Navigate to app directory
cd /Users/wimtilburgs/Development/cia-app

# Activate virtual environment
echo -e "${BLUE}🔧 Activating virtual environment...${NC}"
source venv/bin/activate

# Install/update dependencies
echo -e "${BLUE}📦 Installing dependencies...${NC}"
pip install -q -r requirements.txt

echo ""
echo -e "${GREEN}🚀 Starting CIA Web Interface...${NC}"
echo -e "${GREEN}📡 Opening browser at: http://localhost:5000${NC}"
echo ""

# Open browser
open http://localhost:5000

# Start Flask app
python app.py