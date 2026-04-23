## Triple-Helix Innovation Chatbot

A lightweight web chatbot that helps you think through innovation challenges using the
**Academia × Industry × Government (Triple Helix)** framework.

---

### Deploy to Netlify (one-click)

[![Deploy to Netlify](https://www.netlify.com/img/deploy/button.svg)](https://app.netlify.com/start/deploy?repository=https://github.com/yabo1234/helix)

**Manual steps:**

1. Fork / push this repo to your GitHub account.
2. Log in to [Netlify](https://app.netlify.com/) and click **"Add new site → Import an existing project"**.
3. Connect your GitHub account and select this repository.
4. Leave the build settings at their defaults (Netlify reads `netlify.toml` automatically):
   - **Build command:** *(leave blank)*
   - **Publish directory:** `.`
5. Click **"Deploy site"**.

Netlify will deploy `index.html` as the static frontend and
`netlify/functions/chat.py` as a serverless Python function reachable at `/api/chat`.

> **No environment variables are required** for the built-in rule-based engine.
> If you swap `generate_reply()` for an LLM API, add your API key via
> **Site settings → Environment variables**.

### Share the URL with your team

After the deploy finishes, Netlify shows your live URL at the top of the
**"Site overview"** page (e.g. `https://your-site-name.netlify.app`).

**To make the URL easy for everyone to find:**

1. Copy the URL from Netlify.
2. Open [`SITE_URL.md`](SITE_URL.md) in this repo.
3. Replace the `https://YOUR-SITE-NAME.netlify.app` placeholder with your real URL.
4. Commit and push the file — teammates can now find the link directly in GitHub.

> See [`SITE_URL.md`](SITE_URL.md) for the current live URL and step-by-step instructions.

---

### Run locally (Gradio UI)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Then open the Gradio link printed in the terminal (default port: `7860`).

### Run the static frontend locally

You can serve `index.html` with any static server and test the Netlify Function locally
using the [Netlify CLI](https://docs.netlify.com/cli/get-started/):

```bash
npm install -g netlify-cli
netlify dev
```

This starts a local dev server (default: `http://localhost:8888`) that serves the
static site **and** runs the Python function at `/api/chat`.

---

### Repository layout

| Path | Description |
|------|-------------|
| `SITE_URL.md` | **Record the live Netlify URL here** to share with your team |
| `index.html` | Static chat UI (deployed as the Netlify site root) |
| `netlify.toml` | Netlify build & functions configuration |
| `netlify/functions/chat.py` | Serverless Python function — handles `POST /api/chat` |
| `netlify/functions/requirements.txt` | Dependencies for the serverless function |
| `app.py` | Alternative Gradio chat UI (for local dev) |
| `triple_helix_engine.py` | Lightweight reply engine (swap for LLM/API when ready) |
| `requirements.txt` | Python dependencies for the Gradio UI |
