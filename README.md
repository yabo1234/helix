## Triple-Helix Chatbot UI

This repo contains a simple web UI for a **Triple-Helix chatbot** (Academia × Industry × Government).

### Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Then open the Gradio link printed in the terminal (default port: `7860`).

### Using DeepSeek or Other LLMs

By default, the chatbot uses a rule-based response engine. To use **DeepSeek** or other LLMs:

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and configure your preferred LLM provider:

   **For DeepSeek:**
   ```bash
   LLM_PROVIDER=deepseek
   DEEPSEEK_API_KEY=your_api_key_here
   ```
   
   Get your API key from [DeepSeek Platform](https://platform.deepseek.com/)

   **For OpenAI:**
   ```bash
   LLM_PROVIDER=openai
   OPENAI_API_KEY=your_api_key_here
   ```

3. Restart the app - it will automatically use the configured LLM provider.

### Files

- `app.py`: Gradio chat UI
- `triple_helix_engine.py`: Reply engine with support for rule-based or LLM-powered responses
- `.env.example`: Configuration template for LLM providers
