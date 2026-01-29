#!/bin/bash
#
# Agent Zero - Local Coding Assistant Startup Script
# Runs Agent Zero locally without Docker
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Agent Zero - Local Coding Assistant  ${NC}"
echo -e "${BLUE}========================================${NC}"
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
    echo -e "${GREEN}Activating virtual environment: $VENV_DIR${NC}"
    source "$VENV_DIR/bin/activate"
else
    echo -e "${YELLOW}Warning: No virtual environment found. Using system Python.${NC}"
fi

# Set API keys from environment or use defaults from settings
export GOOGLE_API_KEY="${GOOGLE_API_KEY:-AIzaSyDCHT2ZBP5O1uVrVcI0t2ARkcajA3n4wug}"
export MISTRAL_API_KEY="${MISTRAL_API_KEY:-7RE8k4ZBDVEZ3BtozQrJmS4XJQCOIgH1}"
export DEEPSEEK_API_KEY="${DEEPSEEK_API_KEY:-sk-0bc346e2ece24f50aebf4fbac808be58}"
export HUGGINGFACE_API_KEY="${HUGGINGFACE_API_KEY:-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}"

# Copy local coder settings if not already the active settings
SETTINGS_FILE="tmp/settings.json"
LOCAL_CODER_SETTINGS="tmp/settings_local_coder.json"

if [ -f "$LOCAL_CODER_SETTINGS" ]; then
    echo -e "${GREEN}Using Local Coder settings${NC}"
    cp "$LOCAL_CODER_SETTINGS" "$SETTINGS_FILE"
fi

# Create shared memory directory for all agents
mkdir -p "memory/default"

# Run preparation script
echo -e "${BLUE}Preparing Agent Zero...${NC}"
python3 prepare.py 2>&1 | grep -v "Error in preload" || true

# Start the UI
echo ""
echo -e "${GREEN}Starting Agent Zero Web UI...${NC}"
echo -e "${BLUE}Open your browser at: http://localhost:50001${NC}"
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop${NC}"
echo ""

python3 run_ui.py --host localhost --port 50001

