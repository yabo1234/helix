## Triple-Helix Chatbot API (Python)

A small Python HTTP API for a Triple-Helix (University–Industry–Government) innovation chatbot.

### Run locally

Install dependencies:

```bash
python3 -m pip install -r requirements.txt
```

Start the server:

```bash
python3 -m uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```

Open the web UI:

- `http://localhost:8000/`

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

- `GET /` → simple web UI
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

### Share on a website (deploy)

This repo includes a `Dockerfile`, which is the easiest way to deploy on most platforms.

#### Option A: Deploy on Render / Railway / Fly.io (Docker)
- Create a new service from this repo
- Choose **Docker**
- Set environment variables:
  - `OPENAI_API_KEY` (optional but recommended)
  - `OPENAI_MODEL` (optional)
- Expose port **8000** (or rely on platform `PORT`)

#### Option B: Run on a VPS (Nginx reverse proxy)
- Run the API on port 8000 (systemd or docker)
- Put Nginx in front with HTTPS and proxy to `127.0.0.1:8000`

