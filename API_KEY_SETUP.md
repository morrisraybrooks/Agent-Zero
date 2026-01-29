# Agent Zero API Key Configuration Guide

## 🎯 Overview

Agent Zero requires API keys to access LLM (Large Language Model) providers. This guide will help you configure API keys for both the Docker instance and the local hybrid setup.

## 📋 Supported LLM Providers

Agent Zero supports multiple LLM providers:

1. **OpenAI** - GPT-4, GPT-4 Turbo, GPT-3.5
2. **Anthropic** - Claude 3.5 Sonnet, Claude 3 Opus, Claude 3 Haiku
3. **OpenRouter** - Access to multiple models through one API
4. **Google AI** - Gemini models
5. **Ollama** - Local models (no API key needed)
6. **Azure OpenAI** - Enterprise OpenAI access
7. **Groq** - Fast inference models

## 🔑 Getting API Keys

### OpenAI
1. Go to https://platform.openai.com/api-keys
2. Sign in or create an account
3. Click "Create new secret key"
4. Copy the key (starts with `sk-`)
5. **Important**: Save it securely - you won't see it again!

### Anthropic (Claude)
1. Go to https://console.anthropic.com/
2. Sign in or create an account
3. Navigate to "API Keys"
4. Click "Create Key"
5. Copy the key (starts with `sk-ant-`)

### OpenRouter (Recommended for Multiple Models)
1. Go to https://openrouter.ai/
2. Sign in with Google/GitHub
3. Go to "Keys" section
4. Click "Create Key"
5. Copy the key (starts with `sk-or-`)
6. **Benefit**: Access to 100+ models with one API key

### Google AI (Gemini)
1. Go to https://makersuite.google.com/app/apikey
2. Sign in with Google account
3. Click "Create API Key"
4. Copy the key

### Groq
1. Go to https://console.groq.com/
2. Sign in or create an account
3. Navigate to "API Keys"
4. Click "Create API Key"
5. Copy the key

## � Model Names Reference

### Google AI (Gemini) - 2025-2026 Models
**Latest Models (Recommended):**
- `gemini-2.5-pro` - Most capable reasoning model
- `gemini-2.5-flash` - Fast, balanced performance
- `gemini-2.5-flash-lite` - Fastest, most cost-effective
- `gemini-3-pro-preview` - Newest experimental model (preview)

**Also Available:**
- `gemini-2.0-flash` - Second generation flash model
- `gemini-2.0-flash-exp` - Experimental variant
- `gemini-1.5-pro` - Previous generation (still works)
- `gemini-1.5-flash` - Previous generation flash

**Important:**
- Use model names WITHOUT the `models/` prefix
- ✅ Correct: `gemini-2.5-pro`
- ❌ Wrong: `models/gemini-2.5-pro`
- Leave API Base URL empty for Google AI

## �🐳 Configuring API Keys in Docker Instance

### Step 1: Access the Web UI
1. Open your browser
2. Go to **http://localhost:50001**
3. You should see the Agent Zero interface

### Step 2: Open Settings
1. Click the **⚙️ Settings** icon (gear icon in the top right)
2. The settings panel will open on the right side

### Step 3: Navigate to API Keys
1. In the settings panel, look for the **"API Keys"** section
2. Click on it to expand

### Step 4: Add Your API Keys
1. You'll see fields for different providers:
   - **OpenAI API Key**
   - **Anthropic API Key**
   - **OpenRouter API Key**
   - **Google AI API Key**
   - **Groq API Key**
   - **Azure OpenAI** (requires additional configuration)

2. Paste your API key(s) into the appropriate field(s)
3. You can add multiple keys for different providers

### Step 5: Configure Model Settings
1. Go to the **"Models"** section in settings
2. Select your preferred model provider:
   - **Chat Model Provider**: Main model for conversations
   - **Utility Model Provider**: Smaller model for quick tasks
   - **Embedding Model Provider**: For semantic search

3. Choose specific models:
   - For OpenAI: `gpt-4-turbo`, `gpt-4`, `gpt-3.5-turbo`
   - For Anthropic: `claude-3-5-sonnet-20241022`, `claude-3-opus-20240229`
   - For OpenRouter: `openai/gpt-4-turbo`, `anthropic/claude-3.5-sonnet`
   - For Google AI: `gemini-2.5-pro`, `gemini-2.5-flash`, `gemini-2.5-flash-lite`
     - Preview: `gemini-3-pro-preview` (Latest, most advanced)

### Step 6: Save Settings
1. Click the **"Save"** button at the bottom of the settings panel
2. The settings will be persisted in the Docker container

### Step 7: Test the Configuration
1. Close the settings panel
2. Type a message in the chat: "Hello, can you introduce yourself?"
3. If configured correctly, Agent Zero will respond using your selected model

## 💻 Configuring API Keys for Local Hybrid Setup

### Method 1: Using .env File (Recommended)

1. Create a `.env` file in the project root:
   ```bash
   cd "/home/morris/Agent Zero"
   touch .env
   ```

2. Add your API keys to the `.env` file:
   ```bash
   # OpenAI
   OPENAI_API_KEY=sk-your-openai-key-here

   # Anthropic
   ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here

   # OpenRouter
   OPENROUTER_API_KEY=sk-or-your-openrouter-key-here

   # Google AI
   GOOGLE_AI_API_KEY=your-google-ai-key-here

   # Groq
   GROQ_API_KEY=your-groq-key-here
   ```

3. Save the file

### Method 2: Using the Web UI (Same as Docker)

When you run the local instance, you can configure API keys through the Web UI just like the Docker instance.

## 🔒 Security Best Practices

1. **Never commit API keys to Git**
   - The `.env` file is already in `.gitignore`
   - Double-check before committing

2. **Use environment variables**
   - Keeps keys separate from code
   - Easy to rotate keys

3. **Limit API key permissions**
   - Use read-only keys when possible
   - Set spending limits on provider dashboards

4. **Rotate keys regularly**
   - Change keys every few months
   - Immediately rotate if compromised

5. **Monitor usage**
   - Check provider dashboards for unusual activity
   - Set up billing alerts

## 💰 Cost Management

### Free Tiers
- **OpenRouter**: $1 free credit for new users
- **Google AI**: Free tier available
- **Groq**: Generous free tier

### Recommended for Testing
1. **OpenRouter** - Best for trying multiple models
2. **Groq** - Fast and free for testing
3. **Google AI (Gemini)** - Generous free tier, latest models
4. **Ollama** - Completely free, runs locally (no API key needed)

### Production Use
- **Google AI Gemini 2.5 Pro**: Excellent reasoning, competitive pricing
- **OpenAI GPT-4**: High quality, moderate cost
- **Anthropic Claude 3.5 Sonnet**: Excellent for complex tasks
- **Google AI Gemini 2.5 Flash**: Fast, cost-effective for high volume
- **OpenRouter**: Flexible, pay-as-you-go

## 🚀 Next Steps

After configuring your API keys:

1. **Test basic functionality**
   - Ask Agent Zero simple questions
   - Try code execution: "List files in the current directory"

2. **Explore capabilities**
   - Web search: "Search for the latest news about AI"
   - Code generation: "Write a Python function to calculate fibonacci"
   - File operations: "Create a file called test.txt with hello world"

3. **Customize behavior**
   - Edit prompts in the `prompts/` folder
   - Adjust model parameters in settings

4. **Create custom tools**
   - See `docs/extensibility.md` for details
   - Add your own Python tools in `python/tools/`

## ❓ Troubleshooting

### "API key not found" error
- Check that you've saved the settings
- Verify the key is correct (no extra spaces)
- Restart the Docker container: `docker restart agent-zero`

### "Rate limit exceeded" error
- You've hit the provider's rate limit
- Wait a few minutes and try again
- Consider upgrading your plan

### "Invalid API key" error
- The key is incorrect or expired
- Generate a new key from the provider
- Update the key in settings

### Model not responding
- Check your internet connection
- Verify the model name is correct
- Try a different model provider

## 📚 Additional Resources

- **Agent Zero Documentation**: See `docs/` folder
- **OpenAI Pricing**: https://openai.com/pricing
- **Anthropic Pricing**: https://www.anthropic.com/pricing
- **OpenRouter Models**: https://openrouter.ai/models

