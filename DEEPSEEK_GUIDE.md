# How to Select DeepSeek

This guide explains how to configure the Triple-Helix Chatbot to use **DeepSeek** as the AI provider.

## Overview

The chatbot supports three modes:
1. **Rule-based** (default): Uses built-in pattern matching and templates
2. **DeepSeek**: Uses DeepSeek AI models for intelligent responses
3. **OpenAI**: Uses OpenAI models (GPT-4, etc.)

## Quick Start with DeepSeek

### Step 1: Get a DeepSeek API Key

1. Visit [DeepSeek Platform](https://platform.deepseek.com/)
2. Sign up or log in to your account
3. Navigate to API Keys section
4. Create a new API key and copy it

### Step 2: Configure Your Environment

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your DeepSeek configuration:
   ```bash
   LLM_PROVIDER=deepseek
   DEEPSEEK_API_KEY=sk-your-actual-api-key-here
   DEEPSEEK_MODEL=deepseek-chat  # Optional, this is the default
   ```

### Step 3: Run the Application

```bash
python app.py
```

The UI will now show "**Powered by DeepSeek AI** 🤖" to indicate it's using DeepSeek.

## Configuration Options

### DeepSeek Models

You can choose different DeepSeek models by setting `DEEPSEEK_MODEL`:

```bash
DEEPSEEK_MODEL=deepseek-chat      # General chat model (default)
DEEPSEEK_MODEL=deepseek-coder     # Optimized for coding tasks
```

### Advanced Configuration

```bash
# Change the base URL (if using a proxy or different endpoint)
DEEPSEEK_BASE_URL=https://api.deepseek.com

# Switch providers easily
LLM_PROVIDER=deepseek    # Use DeepSeek
LLM_PROVIDER=openai      # Use OpenAI instead
LLM_PROVIDER=rule-based  # Use built-in rules (no API needed)
```

## Troubleshooting

### Issue: Still using rule-based responses

**Solutions:**
- Verify `.env` file exists in the project root
- Check that `LLM_PROVIDER=deepseek` is set correctly (no typos)
- Ensure `DEEPSEEK_API_KEY` is set with a valid key
- Restart the application after changing `.env`

### Issue: API errors or rate limiting

**Solutions:**
- Verify your API key is valid and active
- Check your DeepSeek account has sufficient credits
- Review rate limits for your API plan
- Check the console/terminal for specific error messages

### Issue: Responses are still generic

**Possible causes:**
- If the API fails, it automatically falls back to rule-based responses
- Check console output for error messages like "LLM error: ..."
- Verify network connectivity to DeepSeek API

## Switching Between Providers

You can easily switch between providers by changing `LLM_PROVIDER`:

```bash
# In .env file
LLM_PROVIDER=deepseek   # Use DeepSeek AI
# or
LLM_PROVIDER=openai     # Use OpenAI (requires OPENAI_API_KEY)
# or
LLM_PROVIDER=rule-based # Use built-in rules (no API needed)
```

Restart the app after making changes.

## Cost Considerations

- DeepSeek offers competitive pricing compared to other LLM providers
- The app limits responses to ~1000 tokens to manage costs
- Monitor your usage on the [DeepSeek Platform](https://platform.deepseek.com/)
- Consider setting spending limits in your DeepSeek account

## Security Best Practices

1. **Never commit your `.env` file** - it's already in `.gitignore`
2. **Keep your API key private** - treat it like a password
3. **Rotate keys regularly** - especially if shared or exposed
4. **Use environment-specific keys** - different keys for dev/prod
5. **Monitor API usage** - watch for unauthorized access

## Example .env Configuration

```bash
# Complete example configuration for DeepSeek
LLM_PROVIDER=deepseek
DEEPSEEK_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
DEEPSEEK_MODEL=deepseek-chat
DEEPSEEK_BASE_URL=https://api.deepseek.com
```

## Need Help?

- DeepSeek Documentation: https://platform.deepseek.com/docs
- Check the project's README.md for general setup
- Review console/terminal output for error messages
