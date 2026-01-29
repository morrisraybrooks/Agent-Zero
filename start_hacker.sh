#!/bin/bash
#
# Agent Zero - Hacker Agent Startup Script
# Runs Agent Zero with the Elite Offensive Security Specialist profile
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color

echo -e "${RED}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${RED}║                                                              ║${NC}"
echo -e "${RED}║  ${CYAN}🔒 Agent Zero - Elite Offensive Security Specialist${RED}  ║${NC}"
echo -e "${RED}║                                                              ║${NC}"
echo -e "${RED}╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${YELLOW}⚠️  WARNING: This agent is designed for AUTHORIZED penetration testing only${NC}"
echo -e "${YELLOW}⚠️  ALWAYS verify authorization before performing any security testing${NC}"
echo ""

# Check for Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed${NC}"
    exit 1
fi

# Check for virtual environment
VENV_DIR=""
if [ -d "venv312" ]; then
    VENV_DIR="venv312"
elif [ -d "venv" ]; then
    VENV_DIR="venv"
fi

if [ -n "$VENV_DIR" ]; then
    echo -e "${GREEN}✓ Activating virtual environment: $VENV_DIR${NC}"
    source "$VENV_DIR/bin/activate"
else
    echo -e "${YELLOW}⚠ Warning: No virtual environment found. Using system Python.${NC}"
fi

# Set API keys from environment or use defaults from settings
export GOOGLE_API_KEY="${GOOGLE_API_KEY:-AIzaSyDCHT2ZBP5O1uVrVcI0t2ARkcajA3n4wug}"
export MISTRAL_API_KEY="${MISTRAL_API_KEY:-7RE8k4ZBDVEZ3BtozQrJmS4XJQCOIgH1}"
export DEEPSEEK_API_KEY="${DEEPSEEK_API_KEY:-sk-0bc346e2ece24f50aebf4fbac808be58}"
export HUGGINGFACE_API_KEY="${HUGGINGFACE_API_KEY:-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}"
export VENICE_API_KEY="${VENICE_API_KEY:-juBGI6pViL3lftLiUW0xDo5KqRBEYuCx3vW9Y6EeF9}"

# Use the same settings as local_coder (or create hacker-specific settings if needed)
SETTINGS_FILE="tmp/settings.json"
LOCAL_CODER_SETTINGS="tmp/settings_local_coder.json"

if [ -f "$LOCAL_CODER_SETTINGS" ]; then
    echo -e "${GREEN}✓ Using Mistral AI configuration${NC}"
    cp "$LOCAL_CODER_SETTINGS" "$SETTINGS_FILE"
fi

# Create shared memory directory for all agents
mkdir -p "memory/default"
echo -e "${GREEN}✓ Persistent memory enabled: memory/default/${NC}"

# Run preparation script
echo ""
echo -e "${BLUE}🔧 Preparing Agent Zero...${NC}"
python3 prepare.py 2>&1 | grep -v "Error in preload" || true

# Display hacker agent capabilities
echo ""
echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${CYAN}  Hacker Agent Capabilities:${NC}"
echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}  ✓ Penetration Testing (OWASP, PTES, NIST)${NC}"
echo -e "${GREEN}  ✓ 50+ Security Tools (Metasploit, Burp Suite, Nmap, etc.)${NC}"
echo -e "${GREEN}  ✓ Web Application Security Testing${NC}"
echo -e "${GREEN}  ✓ Network Penetration Testing${NC}"
echo -e "${GREEN}  ✓ Cloud Security (AWS, Azure, GCP)${NC}"
echo -e "${GREEN}  ✓ Container & Kubernetes Security${NC}"
echo -e "${GREEN}  ✓ Persistent Memory Across Sessions${NC}"
echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"

# Start the UI
echo ""
echo -e "${GREEN}🚀 Starting Agent Zero Web UI...${NC}"
echo -e "${BLUE}🌐 Open your browser at: ${MAGENTA}http://localhost:50001${NC}"
echo ""
echo -e "${YELLOW}⌨️  Press Ctrl+C to stop${NC}"
echo ""

python3 run_ui.py --host localhost --port 50001

