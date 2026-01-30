#!/bin/bash

# Agent Zero Startup Script
# This script starts the Agent Zero application

# Navigate to the Agent Zero directory
cd "/home/morris/Agent Zero"

# Activate the virtual environment
source venv/bin/activate

# Start Agent Zero
python run_ui.py

# Keep the terminal open if there's an error
read -p "Press Enter to close..."

