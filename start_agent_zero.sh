#!/bin/bash

# Agent Zero Startup Script
# This script starts the Agent Zero application

# Navigate to the Agent Zero directory
cd "/home/morris/Agent Zero"

# Activate the virtual environment (venv312 is the correct one)
source venv312/bin/activate

# Start Agent Zero with proper host and port
python3 run_ui.py --host localhost --port 50001

# Keep the terminal open if there's an error
read -p "Press Enter to close..."

