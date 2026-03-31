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

---

## Business Analysis Agent

A structured AI assistant that applies proven business frameworks—SWOT, PESTLE, Porter's Five Forces, Business Model Canvas, and more—to help make better-informed decisions.

### Run locally

```bash
python business_analysis_app.py
```

Then open the Gradio link printed in the terminal (default port: `7861`).

### Files

- `business_analysis_app.py`: Gradio chat UI for the business analysis agent
- `business_analysis_engine.py`: rule-based reply engine with intent detection for eight frameworks (swap `generate_reply()` with an LLM/API when ready)

### Supported frameworks

| Framework | Trigger keywords |
|-----------|------------------|
| SWOT | swot, strength, weakness, opportunity, threat |
| PESTLE | pestle, political, economic, social, technological, legal, environmental |
| Porter's Five Forces | porter, five forces, competitive, rivalry, supplier, buyer |
| Business Model Canvas | business model, canvas, value proposition, revenue, channel |
| Market Analysis | market, segment, TAM/SAM/SOM, sizing |
| Financial Analysis | financial, profit, margin, cash flow, break-even, ROI |
| Risk Analysis | risk, mitigation, contingency, scenario |
| Strategy & Roadmap | strategy, roadmap, plan, goal, KPI, OKR |
