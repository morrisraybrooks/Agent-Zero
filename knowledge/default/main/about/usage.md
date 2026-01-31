# Morris's Coding Agent - Usage Guide

## Quick Start

### Starting the Agent

**Option 1: Local Coder Agent (Recommended for Development)**
```bash
cd "/home/morris/Agent Zero"
./start_local_coder.sh
```

**Option 2: Hacker Agent (Security Testing)**
```bash
cd "/home/morris/Agent Zero"
./start_hacker.sh
```

**Option 3: Default Agent Zero**
```bash
cd "/home/morris/Agent Zero"
./start_agent_zero.sh
```

### Accessing the Web UI

After starting any agent, open your browser to:
```
http://localhost:5000
```

The modern glassmorphism UI will load with the selected agent profile.

## Startup Scripts Explained

### start_local_coder.sh

This script performs the following steps:

1. **Navigate to Agent Zero directory**
   ```bash
   cd "/home/morris/Agent Zero"
   ```

2. **Activate virtual environment**
   ```bash
   source venv312/bin/activate
   ```

3. **Export API keys** (from your environment)
   - `MISTRAL_API_KEY`
   - `DEEPSEEK_API_KEY`
   - `GOOGLE_API_KEY`
   - `HF_TOKEN`
   - `VENICE_API_KEY`

4. **Copy settings file**
   ```bash
   cp tmp/settings_local_coder.json tmp/settings.json
   ```

5. **Launch Agent Zero**
   ```bash
   python3 run_ui.py --host localhost --port 5000
   ```

### Error Handling

All startup scripts include:
- Virtual environment validation
- API key verification
- Settings file checks
- Clear error messages
- Automatic troubleshooting hints

## Configuration

### Main Configuration File

**Location**: `tmp/settings_local_coder.json`

**Key Settings**:
```json
{
  "chat_model": {
    "provider": "mistral",
    "name": "mistral-large-latest",
    "temperature": 0.7
  },
  "utility_model": {
    "provider": "mistral",
    "name": "mistral-large-latest"
  },
  "embedding_model": {
    "provider": "huggingface",
    "name": "sentence-transformers/all-MiniLM-L6-v2"
  }
}
```

### Changing Models

To use a different LLM provider:

1. Edit `tmp/settings_local_coder.json`
2. Change the `provider` and `name` fields
3. Ensure you have the appropriate API key set
4. Restart the agent

**Supported Providers**:
- Mistral AI (default)
- DeepSeek
- Google AI (Gemini)
- OpenAI
- Anthropic (Claude)
- Venice AI

### API Key Setup

API keys should be set as environment variables. Add to your `~/.bashrc` or `~/.zshrc`:

```bash
export MISTRAL_API_KEY="your-mistral-api-key"
export DEEPSEEK_API_KEY="your-deepseek-api-key"
export GOOGLE_API_KEY="your-google-api-key"
export HF_TOKEN="your-huggingface-token"
export VENICE_API_KEY="your-venice-api-key"
```

Then reload your shell:
```bash
source ~/.bashrc
```

## Using the Local Coder Agent

### First-Time Project Setup

When starting with a new project:

1. **Index the codebase**:
   ```
   "Index this codebase and remember it"
   ```

2. **The agent will**:
   - Scan project structure
   - Identify technology stack
   - Save to persistent memory
   - Learn coding patterns

3. **Future sessions**:
   - Agent remembers everything
   - No need to re-index
   - Instant context recall

### Example Interactions

**Code Generation**:
```
"Create a React component for user authentication with TypeScript"
```

**Code Review**:
```
"Review the authentication logic in src/auth/login.ts"
```

**Debugging**:
```
"Why is the API returning 500 errors on POST /users?"
```

**Architecture**:
```
"Design a microservices architecture for this e-commerce platform"
```

**Testing**:
```
"Write unit tests for the UserService class"
```

## Using the Hacker Agent

### Authorization Workflow

The Hacker agent requires proper authorization:

1. **Verify authorization**:
   ```
   "I have written authorization to test example.com"
   ```

2. **Define scope**:
   ```
   "Scope: Web application penetration test, no DoS attacks"
   ```

3. **Begin engagement**:
   ```
   "Start reconnaissance on example.com"
   ```

### Example Security Tasks

**Reconnaissance**:
```
"Perform OSINT on target.com"
```

**Vulnerability Scanning**:
```
"Scan the web application for SQL injection vulnerabilities"
```

**Exploitation**:
```
"Develop a proof-of-concept for the XSS vulnerability found"
```

**Reporting**:
```
"Generate a professional vulnerability report with remediation steps"
```

## Memory System

### How Memory Works

- **Automatic**: Agent saves important information automatically
- **Persistent**: Memory survives across sessions
- **Searchable**: Agent can recall specific information
- **Contextual**: Memory is used to provide better responses

### Memory Commands

**Save to memory**:
```
"Remember that we use React 18 with TypeScript for all frontend projects"
```

**Recall from memory**:
```
"What technology stack do we use for frontend?"
```

**Clear specific memory**:
```
"Forget the old database schema, we've migrated to PostgreSQL"
```

## File Operations

### Working with Files

**Read files**:
```
"Show me the contents of src/components/Header.tsx"
```

**Create files**:
```
"Create a new API endpoint in src/routes/users.ts"
```

**Edit files**:
```
"Update the authentication middleware to use JWT tokens"
```

**Search files**:
```
"Find all files that import the UserService"
```

## Advanced Features

### Multi-Agent Cooperation

The agent can spawn subordinate agents for complex tasks:

```
"Create a full-stack application with authentication, database, and API"
```

The main agent will:
1. Break down the task
2. Spawn specialized sub-agents
3. Coordinate their work
4. Integrate the results

### Code Execution

The agent can execute code to test solutions:

```
"Test if this Python script works correctly"
```

### Web Search

The agent can search the web for information:

```
"What are the latest best practices for React 18 performance?"
```

## Troubleshooting

### Agent Not Starting

1. Check virtual environment:
   ```bash
   source venv312/bin/activate
   python --version  # Should be 3.12.x
   ```

2. Verify API keys are set:
   ```bash
   echo $MISTRAL_API_KEY
   ```

3. Check settings file exists:
   ```bash
   ls -la tmp/settings_local_coder.json
   ```

### Port Already in Use

If port 5000 is already in use:

1. Find the process:
   ```bash
   lsof -i :5000
   ```

2. Kill it:
   ```bash
   kill -9 <PID>
   ```

3. Or change the port in the startup script

### Memory Issues

If the agent seems to have forgotten context:

1. Check memory directory:
   ```bash
   ls -la memory/default/
   ```

2. Verify memory files exist and are not corrupted

3. Re-index if necessary:
   ```
   "Re-index this project and save to memory"
   ```

## Best Practices

1. **Be Specific**: Provide clear, detailed instructions
2. **Use Memory**: Let the agent remember important context
3. **Iterate**: Start simple, then refine
4. **Review Code**: Always review generated code before using
5. **Test**: Ask the agent to write tests for generated code
6. **Document**: Have the agent document complex logic

## Related Documentation

- See `setup.md` for configuration details
- See `customizations.md` for what makes this setup unique
- See `/agents/local_coder/README.md` for Local Coder capabilities
- See `/agents/hacker/README.md` for Hacker agent capabilities

