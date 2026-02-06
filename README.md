## Triple-Helix Chatbot UI

This repo contains a simple web UI for a **Triple-Helix chatbot** (Academia × Industry × Government).

### About the Triple Helix Model

The Triple Helix model of innovation describes the interaction between universities, industry, and government in knowledge-based economies. To learn about the evolution of this concept from metaphor to theory to movement, see [TRIPLE_HELIX_EVOLUTION.md](TRIPLE_HELIX_EVOLUTION.md).

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
- `TRIPLE_HELIX_EVOLUTION.md`: comprehensive documentation on the evolution of Triple Helix innovation from metaphor to theory to movement
