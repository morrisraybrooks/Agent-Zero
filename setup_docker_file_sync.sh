#!/bin/bash

# Setup Docker File Sync for Agent Zero Coding Agent
# This script configures proper volume mounts so Agent Zero can edit files
# and you can see the changes on your host machine

echo "=========================================="
echo "Agent Zero Docker File Sync Setup"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Step 1: Stop running containers
echo -e "${YELLOW}Step 1: Stopping running containers...${NC}"
docker stop agent-zero 2>/dev/null && echo "  Stopped agent-zero" || true
docker stop agent_zero_persistent 2>/dev/null && echo "  Stopped agent_zero_persistent" || true
echo -e "${GREEN}✓ Containers stopped${NC}"

# Step 2: Remove old containers
echo -e "${YELLOW}Step 2: Removing old containers...${NC}"
docker rm agent-zero 2>/dev/null && echo "  Removed agent-zero" || true
docker rm agent_zero_persistent 2>/dev/null && echo "  Removed agent_zero_persistent" || true
echo -e "${GREEN}✓ Old containers removed${NC}"

# Step 3: Create required directories
echo -e "${YELLOW}Step 3: Creating required directories...${NC}"
mkdir -p /home/morris/agent_zero_projects
echo -e "${GREEN}✓ Created /home/morris/agent_zero_projects${NC}"

# Step 4: Create persistence directory (may need sudo)
echo -e "${YELLOW}Step 4: Creating persistence directory...${NC}"
if [ ! -d "/var/lib/agent_zero" ]; then
    sudo mkdir -p /var/lib/agent_zero
    sudo chown 1000:1000 /var/lib/agent_zero
    sudo chmod 755 /var/lib/agent_zero
    echo -e "${GREEN}✓ Created /var/lib/agent_zero${NC}"
else
    echo -e "${GREEN}✓ /var/lib/agent_zero already exists${NC}"
fi

# Step 5: Start container with docker run
echo -e "${YELLOW}Step 5: Starting container with docker run...${NC}"
docker run -d \
  --name agent_zero_persistent \
  --restart unless-stopped \
  -p 55000:80 \
  -v /home/morris/Weapons-main:/weapons \
  -v /home/morris/agent_zero_projects:/projects \
  -v /var/lib/agent_zero:/root \
  -e USER_ID=1000 \
  -e GROUP_ID=1000 \
  agent0ai/agent-zero:latest > /dev/null 2>&1
echo -e "${GREEN}✓ Container started${NC}"

# Step 6: Wait for container to be ready
echo -e "${YELLOW}Step 6: Waiting for container to be ready...${NC}"
sleep 5

# Step 7: Verify mounts
echo -e "${YELLOW}Step 7: Verifying volume mounts...${NC}"
docker inspect agent_zero_persistent --format='{{json .Mounts}}' | python3 -m json.tool
echo -e "${GREEN}✓ Mounts verified${NC}"

# Step 8: Test file sync
echo -e "${YELLOW}Step 8: Testing file sync...${NC}"
echo "test from setup script" > /home/morris/Weapons-main/setup_test.txt
if docker exec agent_zero_persistent cat /weapons/setup_test.txt > /dev/null 2>&1; then
    echo -e "${GREEN}✓ File sync working!${NC}"
    rm /home/morris/Weapons-main/setup_test.txt
else
    echo -e "${RED}✗ File sync test failed${NC}"
fi

echo ""
echo "=========================================="
echo -e "${GREEN}Setup Complete!${NC}"
echo "=========================================="
echo ""
echo "Your Agent Zero is now configured as a coding agent!"
echo ""
echo "File locations:"
echo "  Host: /home/morris/Weapons-main/"
echo "  Container: /weapons/"
echo ""
echo "When Agent Zero edits files in the container,"
echo "they will automatically appear on your host machine!"
echo ""
echo "Next steps:"
echo "1. Give Agent Zero a coding task"
echo "2. Check /home/morris/Weapons-main/ for the results"
echo "3. Commit changes to GitHub:"
echo "   cd /home/morris/Weapons-main"
echo "   git add ."
echo "   git commit -m 'Changes from Agent Zero'"
echo "   git push origin main"
echo ""

