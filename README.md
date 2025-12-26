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

### Files

- `app.py`: Gradio chat UI
- `triple_helix_engine.py`: lightweight reply engine (swap this with an LLM/API later)
