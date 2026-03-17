## Triple-Helix Chatbot UI

This repo contains two AI-style chatbot UIs built with Gradio.

---

### 1 · Triple-Helix Chatbot (Academia × Industry × Government)

A lightweight assistant for thinking through innovation using the Triple-Helix framework.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Then open the Gradio link printed in the terminal (default port: `7860`).

**Files**

- `app.py`: Gradio chat UI
- `triple_helix_engine.py`: lightweight reply engine (swap with an LLM/API later)

---

### 2 · Macroeconomics Analysis Bot

A lightweight assistant for analysing macroeconomic topics: inflation, monetary policy,
fiscal policy, GDP growth, trade, and labour markets.

```bash
python macroeconomics_app.py
```

Opens on port `7861` by default (set `PORT` env-var to override).

**Files**

- `macroeconomics_app.py`: Gradio chat UI
- `macroeconomics_engine.py`: rule-based analysis engine (swap with an LLM/API later)
