# Morris's Coding Agent - Customizations

## Overview

This document details the specific customizations made to the base Agent Zero framework to create Morris's personal coding assistant.

## 1. Enhanced Local Coder Agent

**Location**: `/agents/local_coder/`

### Key Features

- **Persistent Memory**: Remembers entire project structure, architecture decisions, and code patterns across all sessions
- **Full-Stack Expertise**: Specialized in React, Vue, Angular, Node.js, Python, Go, and modern frameworks
- **Database Knowledge**: PostgreSQL, MySQL, MongoDB, Redis, Elasticsearch
- **DevOps Integration**: Docker, Kubernetes, CI/CD pipelines, cloud platforms

### Custom Prompt

The Local Coder agent has a custom system prompt (`agent.system.md`) that emphasizes:
- Code quality and best practices
- Security-first development
- Performance optimization
- Comprehensive testing
- Clear documentation

### Capabilities

1. **Frontend Development**: React 18+, TypeScript, Vite, Next.js, Nuxt
2. **Backend Development**: Node.js, Express, FastAPI, Django, Go, Rust
3. **Architecture**: Microservices, serverless, event-driven, monolithic
4. **Testing**: Unit tests, integration tests, E2E tests
5. **Code Review**: Automated code analysis and suggestions

### Documentation

See `/agents/local_coder/README.md` for complete documentation (280 lines).

## 2. Enhanced Hacker Agent

**Location**: `/agents/hacker/`

### Key Features

- **Offensive Security**: Penetration testing, vulnerability assessment, exploit development
- **Persistent Engagement History**: Maintains findings and progress across sessions
- **Ethical Framework**: Built-in authorization workflows and legal compliance
- **Comprehensive Reporting**: Detailed vulnerability reports and remediation guidance

### Custom Prompt

The Hacker agent has a custom system prompt that emphasizes:
- Ethical hacking principles
- Proper authorization verification
- Comprehensive documentation
- Legal compliance
- Responsible disclosure

### Capabilities

1. **Reconnaissance**: OSINT, network scanning, service enumeration
2. **Vulnerability Assessment**: Web apps, networks, APIs, mobile apps
3. **Exploitation**: Proof-of-concept development, privilege escalation
4. **Post-Exploitation**: Persistence, lateral movement, data exfiltration
5. **Reporting**: Professional vulnerability reports with CVSS scoring

### Documentation

See `/agents/hacker/README.md` for complete documentation.

## 3. Modern Glassmorphism UI Theme

**Location**: `/webui/css/modern-theme.css`

### Design Features

- **Glassmorphism**: Translucent backgrounds with backdrop blur effects
- **Gradient Backgrounds**: Modern color gradients throughout the interface
- **Smooth Animations**: Fluid transitions and hover effects
- **Dark Mode Optimized**: Designed for long coding sessions
- **Responsive Design**: Works on desktop and mobile devices

### Technical Details

- **File Size**: 757 lines of custom CSS
- **Color Palette**: Modern dark mode with purple/blue accents
- **Typography**: Clean, readable fonts optimized for code
- **Components**: Custom styled buttons, inputs, cards, modals

### Color Scheme

```css
--modern-bg-primary: #0a0e1a
--modern-bg-secondary: #111827
--modern-gradient-primary: linear-gradient(135deg, #667eea 0%, #764ba2 100%)
--modern-gradient-accent: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)
--modern-text-primary: #f8fafc
--modern-accent-purple: #8b5cf6
```

### Integration

The theme is loaded in `/webui/index.html` at line 20:
```html
<link rel="stylesheet" href="css/modern-theme.css">
```

## 4. Simplified Startup Scripts

### start_local_coder.sh

**Purpose**: Launch the Local Coder agent with full error checking

**Features**:
- Virtual environment activation (`venv312`)
- API key environment variable export
- Settings file management
- Error handling and validation
- Automatic port configuration (5000)

**Location**: `/home/morris/Agent Zero/start_local_coder.sh`

### start_hacker.sh

**Purpose**: Launch the Hacker agent for security testing

**Features**:
- Same robust error checking as Local Coder
- Hacker-specific settings configuration
- Authorization verification prompts
- Engagement logging

**Location**: `/home/morris/Agent Zero/start_hacker.sh`

### start_agent_zero.sh

**Purpose**: Launch default Agent Zero

**Features**:
- Simplified launcher for base Agent Zero
- Correct virtual environment path (`venv312`)
- Proper host and port arguments
- Updated Python command (`python3`)

**Location**: `/home/morris/Agent Zero/start_agent_zero.sh`

## 5. Configuration Management

### Settings File

**Location**: `tmp/settings_local_coder.json`

**Customizations**:
- Pre-configured Mistral AI models
- Rate limiting optimized for development
- Custom memory settings
- Browser agent configuration

### Environment Variables

All API keys are managed via environment variables:
- Loaded automatically by startup scripts
- Never committed to version control
- Easy to update without code changes

## 6. Documentation Updates

### README.md

**Customizations**:
- Removed all original Agent Zero changelog (v0.9.7 - v0.7)
- Removed community links and marketing content
- Added focus on personal coding assistant use case
- Documented specific customizations
- Reduced from 434 lines to 123 lines

### Knowledge Base

**Location**: `/knowledge/default/main/about/`

**Custom Files**:
- `setup.md` - Configuration and architecture
- `customizations.md` - This file
- `usage.md` - How to use the system

**Removed**:
- Original Agent Zero installation guide (555 lines)
- Original Agent Zero documentation index (66 lines)

## 7. Repository Cleanup

### Removed Files

- `.github/FUNDING.yml` - No sponsorship/donation requests

### Updated Files

- `README.md` - Focused on personal setup
- `start_agent_zero.sh` - Fixed virtual environment path

## Summary of Changes

| Component | Original | Customized |
|-----------|----------|------------|
| Execution | Docker-based | Local execution |
| LLM Provider | OpenAI/OpenRouter | Mistral AI |
| UI Theme | Default | Modern glassmorphism |
| Agents | Generic | Enhanced (Local Coder, Hacker) |
| Startup | Manual setup | Automated scripts |
| Documentation | Generic Agent Zero | Morris's Coding Agent |
| Memory | Session-based | Persistent across sessions |
| Configuration | Manual | Pre-configured |

## Philosophy

This setup prioritizes:
1. **Simplicity**: Easy to start and use
2. **Persistence**: Agents remember context
3. **Specialization**: Enhanced agents for specific tasks
4. **Aesthetics**: Modern, pleasant UI
5. **Control**: Local execution, full data ownership

