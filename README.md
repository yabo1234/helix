## Helix — Afaan Oromoo Site

A polished Afaan Oromoo web portal featuring news links (BBC, VOA, Addis Standard), site overview, help pages, and a fully branded layout using the Helix `brand.webp` logo.

### Preview the site locally

**Option 1 — Python (built-in, no install needed):**
```bash
cd /path/to/helix
python -m http.server 8080
```
Open <http://localhost:8080> in your browser.

**Option 2 — Node.js (npx serve):**
```bash
npx serve .
```

**Option 3 — VS Code Live Server extension:**  
Install the *Live Server* extension, right-click `index.html`, and choose **Open with Live Server**.

### Pages

| File | Description |
|------|-------------|
| `index.html` | Homepage — hero with brand logo, feature highlights, CTA |
| `oromo3.html` | News page — BBC/VOA/Addis Standard links |
| `garaa.html` | Overview / table of contents |
| `waaee.html` | About the site |
| `deeggarsa.html` | Support / contact |
| `qajeelfama.html` | How-to guide |
| `haala1.html` / `haala2.html` | Sample/placeholder pages |

### Python chatbot (separate feature)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Then open the Gradio link printed in the terminal (default port: `7860`).

### Files

- `app.py`: Gradio chat UI
- `triple_helix_engine.py`: lightweight reply engine (swap this with an LLM/API later)
- `brand.webp`: site logo / brand mark used in the header, hero, and footer
- `assets/css/styles.css`: shared stylesheet
- `assets/js/main.js`: navigation dropdown script
