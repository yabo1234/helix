## Triple-Helix Chatbot API (Python)

A small Python HTTP API for a Triple-Helix (University–Industry–Government) innovation chatbot.

### Run locally

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Start the server:

```bash
python3 -m uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```

### Configure (optional)

- **OpenAI**
  - `OPENAI_API_KEY`: required to use OpenAI responses
  - `OPENAI_MODEL`: optional (default: `gpt-4o-mini`)
- **Sessions**
  - `SESSION_MAX_MESSAGES`: optional (default: `50`)
- **CORS**
  - `CORS_ALLOW_ORIGINS`: optional comma-separated list (default: `*`)

If `OPENAI_API_KEY` is not set, the API will still work using a deterministic local fallback response.

### Endpoints

- `GET /health` → health check
- `POST /chat` → generate a response

Example request:

```bash
curl -s http://localhost:8000/chat \
  -H 'content-type: application/json' \
  -d '{
    "messages": [{"role":"user","content":"Design a triple-helix innovation plan for a smart agriculture pilot."}]
  }'
```
