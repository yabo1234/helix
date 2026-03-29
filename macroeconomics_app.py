from __future__ import annotations

import os

import gradio as gr

from macroeconomics_engine import generate_reply


APP_TITLE = "Macroeconomics Analysis Bot"
APP_DESCRIPTION = (
    "A lightweight AI-style assistant that helps you analyse macroeconomic topics "
    "including inflation, monetary policy, fiscal policy, GDP growth, trade, and "
    "labour markets."
)


def chat_fn(message: str, history: list[dict[str, str]]) -> str:
    reply = generate_reply(message=message, history=history)
    return reply.answer


def build_ui() -> gr.Blocks:
    with gr.Blocks(title=APP_TITLE, theme=gr.themes.Soft()) as demo:
        gr.Markdown(f"## {APP_TITLE}\n\n{APP_DESCRIPTION}")

        gr.ChatInterface(
            fn=chat_fn,
            type="messages",
            chatbot=gr.Chatbot(height=420, show_copy_button=True),
            textbox=gr.Textbox(
                placeholder="Ask about inflation, GDP growth, central bank policy…",
                lines=2,
            ),
            submit_btn="Analyse",
            retry_btn="Retry",
            undo_btn="Undo",
            clear_btn="Clear",
            examples=[
                "What is driving high inflation in developed economies right now?",
                "How does quantitative tightening affect bond markets and the real economy?",
                "Explain the fiscal multiplier and when it is most effective.",
                "What does a rising output gap tell us about monetary policy stance?",
                "How does a current account deficit interact with exchange rate movements?",
            ],
        )

        gr.Markdown(
            "### Notes\n"
            "- This bot uses a built-in, rule-based analysis engine.\n"
            "- Swap `generate_reply()` in `macroeconomics_engine.py` for an LLM/API when ready."
        )

    return demo


if __name__ == "__main__":
    demo = build_ui()
    port = int(os.environ.get("PORT", "7861"))
    demo.launch(server_name="0.0.0.0", server_port=port, show_api=False)
