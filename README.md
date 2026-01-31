# Morris's Coding Agent

A customized [Agent Zero](https://github.com/frdel/agent-zero) setup optimized for local software development with persistent memory and modern UI.

## 🎯 What This Is

This is **not** a fork of Agent Zero - it's my personal coding assistant built on top of the Agent Zero framework. I've customized it specifically for:

- **Local development** without Docker
- **Persistent memory** across all coding sessions
- **Enhanced agent profiles** for specialized tasks
- **Modern glassmorphism UI** theme
- **Mistral AI integration** as the primary LLM provider

## 🚀 Key Customizations

### 1. **Enhanced Local Coder Agent**
- Full-stack development specialist with persistent memory
- Remembers your entire codebase structure across sessions
- Specialized in React, Node.js, Python, and modern frameworks
- See: [`agents/local_coder/README.md`](agents/local_coder/README.md)

### 2. **Enhanced Hacker Agent**
- Offensive security specialist for penetration testing
- Maintains engagement history and findings across sessions
- Ethical hacking with proper authorization workflows
- See: [`agents/hacker/README.md`](agents/hacker/README.md)

### 3. **Modern UI Theme**
- Sleek glassmorphism design with gradient backgrounds
- Smooth animations and contemporary styling
- Dark mode optimized for long coding sessions
- See: [`webui/css/modern-theme.css`](webui/css/modern-theme.css)

### 4. **Simplified Startup Scripts**
- `start_local_coder.sh` - Launch the coding assistant
- `start_hacker.sh` - Launch the security testing agent
- `start_agent_zero.sh` - Launch default Agent Zero
- All scripts handle virtual environment activation automatically

## 📦 Installation

### Prerequisites
- Python 3.12+ (tested with 3.12.8)
- Virtual environment support
- API keys for Mistral AI (or other LLM providers)

### Setup

```bash
# Clone this repository
git clone https://github.com/morrisraybrooks/Agent-Zero.git
cd Agent-Zero

# Create virtual environment
python3 -m venv venv312
source venv312/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure your API keys
# Edit tmp/settings_local_coder.json with your API keys
```

### Quick Start

```bash
# Launch the Local Coder agent
./start_local_coder.sh

# Then open http://localhost:5000 in your browser
```

## 🔧 Configuration

The main configuration is in `tmp/settings_local_coder.json`:

- **Chat Model**: Mistral Large (mistral-large-latest)
- **Utility Model**: Mistral Large
- **Browser Model**: Mistral Large
- **Embedding Model**: HuggingFace sentence-transformers/all-MiniLM-L6-v2
- **Rate Limits**: 5 req/min, 50k tokens/min (configurable)

See [`SETUP_LOCAL_CODER.md`](SETUP_LOCAL_CODER.md) for detailed configuration options.

## 📚 Documentation

- **[Local Coder Agent Guide](agents/local_coder/README.md)** - Full-stack development assistant
- **[Hacker Agent Guide](agents/hacker/README.md)** - Security testing specialist
- **[Setup Guide](SETUP_LOCAL_CODER.md)** - Detailed installation and configuration
- **[API Key Setup](API_KEY_SETUP.md)** - How to configure API keys

## 🎨 What Makes This Different

Unlike the base Agent Zero framework, this setup is:

1. **Optimized for local execution** - No Docker complexity
2. **Memory-persistent** - Agents remember your projects across sessions
3. **Visually modern** - Custom UI theme for better UX
4. **Pre-configured** - Ready to use for coding tasks out of the box
5. **Specialized agents** - Enhanced profiles for specific use cases

## 🔗 Credits

Built on top of [Agent Zero](https://github.com/frdel/agent-zero) by [@frdel](https://github.com/frdel)

Agent Zero is an organic, evolving AI agent framework. This repository contains my personal customizations for software development workflows.

## 📝 License

Same as Agent Zero - see [LICENSE](LICENSE)

## 🤝 Contributing

This is a personal setup, but feel free to:
- Fork it for your own customizations
- Open issues if you find bugs in my customizations
- Share your own Agent Zero setups!

---

**Note**: This is a personal coding assistant setup, not a general-purpose Agent Zero distribution. For the official Agent Zero framework, visit [agent-zero.ai](https://agent-zero.ai) or the [official repository](https://github.com/frdel/agent-zero).
