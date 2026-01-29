# Agent Zero - Local Coder Setup

This is a customized Agent Zero setup configured for local execution without Docker, with persistent memory across all agents.

## Features

- **Local Execution**: No Docker required - runs directly on your system
- **Persistent Memory**: All agents share the same memory in `memory/default/`
- **Mistral AI Integration**: Uses Mistral as the primary model provider
- **Custom Agent Profiles**: Includes specialized agents (local_coder, writer)
- **File System Awareness**: Agents remember your codebase structure across sessions

## Quick Start

### 1. Prerequisites

- Python 3.13+ (tested with Python 3.13.7)
- Virtual environment (venv312)
- API Keys (see Configuration below)

### 2. Installation

```bash
# Activate virtual environment
source venv312/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration

Create a file with your API keys (not tracked in git):
- Google AI API key
- Mistral API key
- DeepSeek API key
- HuggingFace token
- Venice AI key

The settings are pre-configured in `tmp/settings_local_coder.json`.

### 4. Run Agent Zero

```bash
./start_local_coder.sh
```

Then open http://localhost:50001 in your browser.

## Agent Profiles

### Local Coder (Agent 0)
- Primary coding assistant
- Maintains awareness of your codebase structure
- Uses persistent memory for context across sessions

### Writer Agent
- Specialized in documentation and content creation
- Shares memory with other agents
- Maintains writing style consistency

## Model Configuration

| Role | Provider | Model |
|------|----------|-------|
| Chat (main) | Mistral | mistral-large-latest (128K context) |
| Utility | Mistral | mistral-small-latest |
| Browser | Mistral | mistral-small-latest |
| Embeddings | Mistral | mistral-embed (API) |

## Memory System

- **Location**: `memory/default/`
- **Type**: FAISS vector database
- **Shared**: All agents access the same memory
- **Persistent**: Survives across sessions

## Troubleshooting

### MCP/A2A Servers Disabled
The MCP and A2A servers are temporarily disabled in `run_ui.py` due to FastMCP API compatibility issues. This doesn't affect core functionality.

### Flask Async Support
Make sure Flask is installed with async support:
```bash
pip install 'flask[async]'
```

### Slow Local Embeddings
This setup uses Mistral's API for embeddings to avoid slow local compute on low-power CPUs.

## File Structure

```
Agent Zero/
├── agents/
│   ├── local_coder/          # Custom coding agent profile
│   └── writer/               # Custom writer agent profile
├── memory/
│   └── default/              # Shared persistent memory
├── tmp/
│   └── settings_local_coder.json  # Configuration
├── start_local_coder.sh      # Startup script
└── requirements.txt          # Python dependencies
```

## Notes

- The startup script automatically sets environment variables for API keys
- Memory is shared across all agents for consistent context
- Local shell execution is enabled (no SSH/Docker needed)
- MCP server functionality is disabled but can be re-enabled after fixing compatibility issues

## License

Same as Agent Zero main project.

