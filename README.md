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

[![Deploy to Netlify](https://www.netlify.com/img/deploy/button.svg)](https://app.netlify.com/start/deploy?repository=https://github.com/yabo1234/helix)

The `public/` folder contains a static HTML page with an **interactive chat widget** powered by a Netlify Serverless Function (`netlify/functions/chat.py`). When deployed to Netlify:
- Visitors can chat with the Triple-Helix engine live in the browser.
- No Python server setup is needed — the function runs on demand.
- `netlify.toml` configures the publish directory, functions, redirects, and security headers automatically.

#### Live API endpoint

```
POST /.netlify/functions/chat
Content-Type: application/json

{"message": "Help me get funding for a drone agriculture pilot."}
```

#### Steps

1. **One-click deploy**
   Click the **Deploy to Netlify** button above. Netlify will fork this repo to your account and deploy the showcase page automatically.

2. **Or connect manually**
   Go to [app.netlify.com](https://app.netlify.com) → *Add new site → Import an existing project* → select `yabo1234/helix`. Netlify reads `netlify.toml`; the publish directory is `public/` and no build command is needed.

3. **Find your site URL**
   Your deployed URL appears in **three places**:
   - **Right after deployment** — the success screen shows a highlighted link like `https://random-name-abc123.netlify.app`. Click it to open your site.
   - **In the Netlify dashboard** — go to [app.netlify.com](https://app.netlify.com) → click **Sites** in the left sidebar → click your site's name → the URL is displayed in bold at the top of the *Site Overview* page.
   - **Via the Netlify CLI** — run `netlify open --site` in the repo directory to open the dashboard, or `netlify status` to print the URL to the terminal.

4. **(Optional) Set a memorable URL**
   In the Netlify dashboard go to *Site configuration → General → Site details → Change site name*. Enter a slug like `triple-helix-chatbot` and your site will be available at `https://triple-helix-chatbot.netlify.app`.

5. **Share the URL**
   Copy the URL from the Site Overview and share it with your team. All visitors will see the live interactive chat widget powered by the serverless function.

6. **Enable team commenting**
   In the Netlify dashboard go to *Site settings → Collaboration → Deploy Previews* and enable the **Netlify Drawer**. Team members can open the live URL, click the Netlify icon in the bottom-left corner, and leave inline comments directly on the page.

---

### Files

| File | Purpose |
|------|---------|
| `app.py` | Gradio chat UI (for local use) |
| `triple_helix_engine.py` | Lightweight rule-based reply engine (swap for an LLM/API later) |
| `requirements.txt` | Python dependencies (`gradio>=5.0.0`) for local Gradio UI |
| `netlify.toml` | Netlify configuration (publish dir, functions, redirects, security headers) |
| `netlify/functions/chat.py` | Netlify Serverless Function — powers the live chat widget on the deployed page |
| `public/index.html` | Showcase page with interactive chat widget, served by Netlify |
