## Triple-Helix Innovation Chatbot

This repo contains a **Triple-Helix chatbot** (Academia × Industry × Government) built with Gradio, plus a static Netlify showcase page so your team can view and comment on the project.

---

### Run locally

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Then open the Gradio link printed in the terminal (default port: `7860`).

---

### Share with your team via Netlify

The `public/` folder contains a static HTML page (`index.html`) that describes the chatbot and guides reviewers. A `netlify.toml` in the repo root configures Netlify to serve this page automatically.

#### Steps

1. **Connect this repo to Netlify**
   Go to [app.netlify.com](https://app.netlify.com) → *Add new site → Import an existing project* → select `yabo1234/helix`.

2. **Build settings are auto-detected**
   Netlify reads `netlify.toml`; the publish directory is `public/` and no build command is needed.

3. **Deploy**
   Click *Deploy site*. Netlify gives you a URL like `https://your-site-name.netlify.app`. Share this link with your team.

4. **Enable team commenting**
   In the Netlify dashboard go to *Site settings → Collaboration → Deploy Previews* and enable the **Netlify Drawer**. Team members can open the live URL, click the Netlify icon in the bottom-left corner, and leave inline comments directly on the page.

> **Note:** The Python/Gradio chatbot itself cannot run on Netlify (it needs a Python server). To host the live chatbot publicly, deploy it to [Hugging Face Spaces](https://huggingface.co/spaces) or [Render](https://render.com), then share the resulting URL with your team.

---

### Files

| File | Purpose |
|------|---------|
| `app.py` | Gradio chat UI |
| `triple_helix_engine.py` | Lightweight rule-based reply engine (swap for an LLM/API later) |
| `requirements.txt` | Python dependencies (`gradio>=5.0.0`) |
| `netlify.toml` | Netlify configuration (publish dir, redirects, security headers) |
| `public/index.html` | Static showcase page served by Netlify for team review |
