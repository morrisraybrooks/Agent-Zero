# Morris's Coding Agent - Setup and Configuration

## Overview

Morris's Coding Agent is a customized Agent Zero setup optimized for local software development. This is **not** a fork of Agent Zero, but a personal coding assistant built on top of the Agent Zero framework.

## Key Configuration Details

### System Architecture

- **Execution Environment**: Local execution without Docker
- **Python Version**: Python 3.12.8
- **Virtual Environment**: `venv312` (located at `/home/morris/Agent Zero/venv312`)
- **Web UI Port**: `http://localhost:5000`
- **Repository**: https://github.com/morrisraybrooks/Agent-Zero

### LLM Configuration

All models are configured to use **Mistral AI** as the primary provider:

- **Chat Model**: `mistral-large-latest` (Mistral AI)
- **Utility Model**: `mistral-large-latest` (Mistral AI)
- **Browser Model**: `mistral-large-latest` (Mistral AI)
- **Embedding Model**: `sentence-transformers/all-MiniLM-L6-v2` (HuggingFace)

### Rate Limits

Configured in `tmp/settings_local_coder.json`:
- **Requests**: 5 requests per minute
- **Input Tokens**: 50,000 tokens per minute
- **Output Tokens**: 50,000 tokens per minute

### API Keys

The system supports multiple LLM providers (configured but Mistral is primary):
- Mistral AI (primary)
- DeepSeek
- Google AI
- HuggingFace
- Venice AI

API keys are stored in environment variables and loaded via startup scripts.

### Memory System

- **Location**: `/home/morris/Agent Zero/memory/`
- **Type**: Persistent memory across all sessions
- **Subdirectories**:
  - `default/` - Main memory storage
  - Agent-specific memory folders

### Knowledge Base

- **Location**: `/home/morris/Agent Zero/knowledge/`
- **Subdirectories**:
  - `default/main/` - Main knowledge files
  - `default/fragments/` - Knowledge fragments
  - `default/instruments/` - Custom instruments
  - `default/solutions/` - Saved solutions
  - `custom/` - Custom knowledge (same structure)

### File Structure

```
/home/morris/Agent Zero/
├── agents/
│   ├── local_coder/          # Enhanced coding agent
│   └── hacker/                # Enhanced security agent
├── memory/                    # Persistent memory storage
├── knowledge/                 # Knowledge base
├── webui/
│   └── css/
│       └── modern-theme.css   # Custom glassmorphism UI
├── tmp/
│   └── settings_local_coder.json  # Main configuration
├── venv312/                   # Python virtual environment
├── start_local_coder.sh       # Coding agent launcher
├── start_hacker.sh            # Security agent launcher
└── start_agent_zero.sh        # Default launcher
```

### Configuration Files

1. **Main Settings**: `tmp/settings_local_coder.json`
   - Contains all LLM configurations
   - API provider settings
   - Rate limits and model parameters

2. **Environment Variables**: Loaded by startup scripts
   - `MISTRAL_API_KEY`
   - `DEEPSEEK_API_KEY`
   - `GOOGLE_API_KEY`
   - `HF_TOKEN`
   - `VENICE_API_KEY`

3. **Agent Profiles**:
   - `agents/local_coder/agent.system.md` - Local Coder system prompt
   - `agents/hacker/agent.system.md` - Hacker agent system prompt

### Startup Process

1. Virtual environment activation (`venv312`)
2. Environment variable export (API keys)
3. Settings file copy to `tmp/settings.json`
4. Launch `run_ui.py` with host and port arguments
5. Web UI accessible at `http://localhost:5000`

### Differences from Base Agent Zero

1. **No Docker**: Runs directly on the host system
2. **Pre-configured**: Ready to use without extensive setup
3. **Persistent Memory**: Agents remember context across sessions
4. **Custom UI**: Modern glassmorphism theme
5. **Specialized Agents**: Enhanced profiles for specific tasks
6. **Mistral AI**: Primary LLM provider instead of OpenAI/OpenRouter

### System Requirements

- **OS**: Linux (tested on Ubuntu/Debian)
- **Python**: 3.12+
- **RAM**: 8GB+ recommended
- **Storage**: 2GB+ for dependencies and memory
- **Network**: Internet connection for API calls

### Security Notes

- API keys stored in environment variables (not in code)
- Local execution provides full control over data
- No external Docker containers
- All data stored locally in `/home/morris/Agent Zero/`

## Related Documentation

- See `customizations.md` for details on specific customizations
- See `usage.md` for how to use the system
- See `/agents/local_coder/README.md` for Local Coder agent details
- See `/agents/hacker/README.md` for Hacker agent details

