from __future__ import annotations

import os

import gradio as gr

from business_analysis_engine import generate_reply


APP_TITLE = "Business Analysis Agent"
APP_DESCRIPTION = (
    "A structured AI assistant that applies proven business analysis frameworks—"
    "SWOT, PESTLE, Porter's Five Forces, Business Model Canvas, and more—"
    "to help you make better-informed decisions."
)


def chat_fn(message: str, history: list[dict[str, str]]):
    reply = generate_reply(message=message, history=history)
    return reply.answer


def build_ui() -> gr.Blocks:
    with gr.Blocks(title=APP_TITLE, theme=gr.themes.Soft()) as demo:
        gr.Markdown(f"## {APP_TITLE}\n\n{APP_DESCRIPTION}")

        gr.ChatInterface(
            fn=chat_fn,
            type="messages",
            chatbot=gr.Chatbot(height=460, show_copy_button=True),
            textbox=gr.Textbox(
                placeholder="Describe your business challenge or ask for a framework analysis…",
                lines=2,
            ),
            submit_btn="Analyse",
            retry_btn="Retry",
            undo_btn="Undo",
            clear_btn="Clear",
            examples=[
                "Run a SWOT analysis for a B2B SaaS startup entering the healthcare market.",
                "Apply Porter's Five Forces to the electric-vehicle battery industry.",
                "Help me build a PESTLE analysis for expanding into Southeast Asia.",
                "What financial metrics should I track for a subscription business?",
                "Identify and prioritise the top risks for a new fintech product launch.",
            ],
        )

        gr.Markdown(
            "### Supported Frameworks\n"
            "| Framework | Trigger keywords |\n"
            "|-----------|------------------|\n"
            "| SWOT | swot, strength, weakness, opportunity, threat |\n"
            "| PESTLE | pestle, political, economic, social, technological, legal, environmental |\n"
            "| Porter's Five Forces | porter, five forces, competitive, rivalry, supplier, buyer |\n"
            "| Business Model Canvas | business model, canvas, value proposition, revenue, channel |\n"
            "| Market Analysis | market, segment, TAM/SAM/SOM, sizing |\n"
            "| Financial Analysis | financial, profit, margin, cash flow, break-even, ROI |\n"
            "| Risk Analysis | risk, mitigation, contingency, scenario |\n"
            "| Strategy & Roadmap | strategy, roadmap, plan, goal, KPI, OKR |\n\n"
            "_Swap `generate_reply()` in `business_analysis_engine.py` for an LLM/API when ready._"
        )

    return demo


if __name__ == "__main__":
    demo = build_ui()
    port = int(os.environ.get("PORT", "7861"))
    demo.launch(server_name="0.0.0.0", server_port=port, show_api=False)
