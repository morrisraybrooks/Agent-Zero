#!/bin/bash

# Agent Zero Persistence Setup - Standard Edition
# Version: 2.0 (Matches documented standards)

# Configuration
CONTAINER_NAME="agent_zero_standard"
HOST_DATA_DIR="/home/morris/agent_zero_data"  # Replace with your preferred path
HOST_PROJECTS_DIR="/home/morris/agent_zero_projects"  # Keep this as-is
PORT="${2:-50080}"
IMAGE="agent0ai/agent-zero:latest"

# Create host data directory
mkdir -p "$HOST_DATA_DIR"
echo "📁 Created data directory: $HOST_DATA_DIR"

# Stop and remove existing container if it exists
docker stop "$CONTAINER_NAME" >/dev/null 2>&1 || true
docker rm "$CONTAINER_NAME" >/dev/null 2>&1 || true
echo "🗑️  Cleaned up existing container if present"

# Run new container with standard volume mapping to /a0
# Following the documented approach: -v /host/path:/a0
echo "🚀 Starting Agent Zero with persistence..."
docker run -d   --name "$CONTAINER_NAME"   -p "$PORT:80"   -v "$HOST_DATA_DIR:/a0"   --restart unless-stopped   "$IMAGE"

# Verification
echo "
✅ SETUP COMPLETE"
echo "📋 Configuration Summary:"
echo "   Container Name: $CONTAINER_NAME"
echo "   Host Data Dir: $HOST_DATA_DIR"
echo "   Web UI Port: $PORT"
echo "   Access URL: http://localhost:$PORT"
echo "
💡 All Agent Zero data will be stored in: $HOST_DATA_DIR"
echo "💡 Changes made to files in this directory will persist across container restarts"
echo "
🔍 Verification:"
echo "   docker ps | grep $CONTAINER_NAME"
echo "   ls -la $HOST_DATA_DIR"
2. Here's the enhanced setup script you should run on your host system:
#!/bin/bash
# Enhanced Agent Zero Persistence Setup
# Run this on your HOST system (not inside the container)

# Configuration - adjust these to your needs
CONTAINER_NAME="agent_zero_persistent"
HOST_DATA_DIR="/var/lib/agent_zero"
HOST_PROJECTS_DIR="/home/morris/agent_zero_projects"
WEB_PORT="55000"
SEARCH_PORT="8001"
USERNAME="morris"  # Your username for proper file ownership

# Create directories with proper permissions
echo "📁 Creating directories with proper ownership..."
sudo mkdir -p "$HOST_DATA_DIR"
sudo mkdir -p "$HOST_PROJECTS_DIR"
sudo chown -R $morris:$morris "$HOST_DATA_DIR"
sudo chown -R $morris:$morris "$HOST_PROJECTS_DIR"

# Stop and remove existing container if it exists
echo "🔄 Cleaning up existing container..."
docker stop "$CONTAINER_NAME" >/dev/null 2>&1 || true
docker rm "$CONTAINER_NAME" >/dev/null 2>&1 || true

# Create file indexing system
echo "📂 Setting up file indexing system..."
cat > file_indexer.py << 'EOF'
#!/usr/bin/env python3
import os
import json
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

WATCH_DIR = "/root"
INDEX_FILE = "/root/file_index.json"

class FileIndexer(FileSystemEventHandler):
    def __init__(self):
        self.index = self.load_index()
        self.build_initial_index()

    def load_index(self):
        try:
            with open(INDEX_FILE, "r") as f:
                return json.load(f)
        except:
            return {}

    def save_index(self):
        with open(INDEX_FILE, "w") as f:
            json.dump(self.index, f)

    def build_initial_index(self):
        for root, _, files in os.walk(WATCH_DIR):
            for file in files:
                self.index_file(os.path.join(root, file))

    def index_file(self, file_path):
        try:
            with open(file_path, "r") as f:
                content = f.read()

            rel_path = os.path.relpath(file_path, WATCH_DIR)
            self.index[rel_path] = {
                "path": file_path,
                "size": os.path.getsize(file_path),
                "modified": os.path.getmtime(file_path),
                "content": content[:1000]  # Store first 1000 chars to save memory
            }
            self.save_index()
        except Exception as e:
            print(f"Error indexing {file_path}: {e}")

    def on_modified(self, event):
        if not event.is_directory:
            self.index_file(event.src_path)

    def on_created(self, event):
        if not event.is_directory:
            self.index_file(event.src_path)

    def on_deleted(self, event):
        if not event.is_directory:
            rel_path = os.path.relpath(event.src_path, WATCH_DIR)
            if rel_path in self.index:
                del self.index[rel_path]
                self.save_index()

def main():
    event_handler = FileIndexer()
    observer = Observer()
    observer.schedule(event_handler, WATCH_DIR, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()
EOF

# Create memory synchronization
cat > memory_sync.py << 'EOF'
#!/usr/bin/env python3
import json
import requests
import time
import os

INDEX_FILE = "/root/file_index.json"
MEMORY_API = "http://localhost:8080/memory/save"

def save_to_memory(data, description):
    payload = {
        "text": json.dumps(data),
        "metadata": {
            "type": "file_content",
            "description": description,
            "source": "file_indexer"
        }
    }
    try:
        response = requests.post(MEMORY_API, json=payload, timeout=10)
        return response.json()
    except Exception as e:
        print(f"Memory save failed: {e}")
        return None

def sync_memory():
    try:
        if not os.path.exists(INDEX_FILE):
            return

        with open(INDEX_FILE, "r") as f:
            file_index = json.load(f)

        for rel_path, file_data in file_index.items():
            try:
                memory_data = {
                    "path": rel_path,
                    "content": file_data["content"],
                    "metadata": {
                        "size": file_data["size"],
                        "modified": file_data["modified"]
                    }
                }

                result = save_to_memory(memory_data, f"File content: {rel_path}")
                if result:
                    print(f"✅ Synced {rel_path} to memory")
            except Exception as e:
                print(f"❌ Error processing {rel_path}: {e}")
    except Exception as e:
        print(f"❌ Error loading index: {e}")

if __name__ == "__main__":
    while True:
        sync_memory()
        time.sleep(300)  # Sync every 5 minutes
EOF

# Create search API
cat > search_api.py << 'EOF'
#!/usr/bin/env python3
from fastapi import FastAPI, HTTPException
import json
import os
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
INDEX_FILE = "/root/file_index.json"

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def load_index():
    global file_index
    try:
        with open(INDEX_FILE, "r") as f:
            file_index = json.load(f)
    except:
        file_index = {}

@app.get("/search")
async def search(query: str, limit: int = 5):
    results = []

    for rel_path, file_data in file_index.items():
        if query.lower() in file_data["content"].lower():
            results.append({
                "path": rel_path,
                "content": file_data["content"],
                "score": 1.0,  # Simple match scoring
                "size": file_data["size"],
                "modified": file_data["modified"]
            })

            if len(results) >= limit:
                break

    return {"results": results}

@app.get("/files")
async def list_files():
    return {"files": list(file_index.keys())}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
EOF

# Make scripts executable
chmod +x file_indexer.py memory_sync.py search_api.py

# Run the container with proper volume mounts
echo "🚀 Starting Agent Zero with persistence..."
docker run -d \
  --name "$CONTAINER_NAME" \
  --restart unless-stopped \
  -p $WEB_PORT:80 \
  -p 8080:8080 \
  -p $SEARCH_PORT:8001 \
  -v "$HOST_DATA_DIR:/root" \
  -v "$HOST_PROJECTS_DIR:/root/agent_zero_projects" \
  agent0ai/agent-zero:latest

# Copy the scripts into the container
echo "📋 Copying scripts to container..."
docker cp file_indexer.py "$CONTAINER_NAME:/root/"
docker cp memory_sync.py "$CONTAINER_NAME:/root/"
docker cp search_api.py "$CONTAINER_NAME:/root/"

# Install required packages in container
echo "📦 Installing dependencies in container..."
docker exec "$CONTAINER_NAME" pip install watchdog fastapi uvicorn python-multipart requests

# Start the services in container
echo "🚀 Starting services in container..."
docker exec -d "$CONTAINER_NAME" python /root/file_indexer.py
docker exec -d "$CONTAINER_NAME" python /root/memory_sync.py
docker exec -d "$CONTAINER_NAME" python /root/search_api.py

# Create systemd service for auto-start
echo "🔧 Creating systemd service for auto-start..."
cat > /tmp/agent_zero.service << EOF
[Unit]
Description=Agent Zero Docker Container
Requires=docker.service
After=docker.service

[Service]
Restart=always
ExecStartPre=-/usr/bin/docker rm -f $CONTAINER_NAME
ExecStart=/usr/bin/docker run -d \
  --name $CONTAINER_NAME \
  --restart unless-stopped \
  -p $WEB_PORT:80 \
  -p 8080:8080 \
  -p $SEARCH_PORT:8001 \
  -v $HOST_DATA_DIR:/root \
  -v $HOST_PROJECTS_DIR:/root/agent_zero_projects \
  agent0ai/agent-zero:latest
ExecStop=/usr/bin/docker stop $CONTAINER_NAME

[Install]
WantedBy=multi-user.target
EOF

sudo mv /tmp/agent_zero.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable agent_zero.service
sudo systemctl start agent_zero.service

# Clean up
echo "🧹 Cleaning up temporary files..."
rm file_indexer.py memory_sync.py search_api.py

# Verification
echo "\n✅ SETUP COMPLETE!"
echo "📋 Configuration Summary:"
echo "   Container Name: $CONTAINER_NAME"
echo "   Host Data Dir: $HOST_DATA_DIR"
echo "   Host Projects Dir: $HOST_PROJECTS_DIR"
echo "   Web UI Port: $WEB_PORT"
echo "   Search API Port: $SEARCH_PORT"
echo "   Access URL: http://localhost:$WEB_PORT"
echo "   Search API: http://localhost:$SEARCH_PORT"
echo "\n💡 All Agent Zero data will be stored in:"
echo "   - $HOST_DATA_DIR (mapped to /root in container)"
echo "   - $HOST_PROJECTS_DIR (mapped to /root/agent_zero_projects)"
echo "\n🔍 Verification commands:"
echo "   docker ps | grep $CONTAINER_NAME"
echo "   docker exec $CONTAINER_NAME ps aux | grep -E 'file_indexer|memory_sync|search_api'"
echo "   curl http://localhost:$SEARCH_PORT/files"
echo "   ls -la $HOST_DATA_DIR"
echo "   ls -la $HOST_PROJECTS_DIR"
