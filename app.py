from __future__ import annotations

import os

import gradio as gr

from triple_helix_engine import generate_reply


APP_TITLE = "Triple-Helix Chatbot"
APP_DESCRIPTION = (
    "A lightweight UI that helps you think through innovation using the "
    "Academia × Industry × Government (Triple Helix) framework."
)


def chat_fn(message: str, history: list[dict[str, str]]):
    # Gradio ChatInterface passes history as a list of {"role": "...", "content": "..."}
    # in newer versions; we keep it generic and only use it for metadata.
    reply = generate_reply(message=message, history=history)
    # If you want to surface metadata in the UI later, you can append it here.
    return reply.answer


def build_ui() -> gr.Blocks:
    with gr.Blocks(title=APP_TITLE, theme=gr.themes.Soft()) as demo:
        gr.Markdown(f"## {APP_TITLE}\n\n{APP_DESCRIPTION}")

        gr.ChatInterface(
            fn=chat_fn,
            type="messages",
            chatbot=gr.Chatbot(height=420, show_copy_button=True),
            textbox=gr.Textbox(
                placeholder="Describe your innovation challenge or idea…",
                lines=2,
            ),
            submit_btn="Send",
            retry_btn="Retry",
            undo_btn="Undo",
            clear_btn="Clear",
            examples=[
                "Help me design a university–startup–government pilot for renewable energy forecasting.",
                "How do I structure a consortium for an AI healthcare product while staying compliant?",
                "I want funding for a smart agriculture prototype. What should the proposal include?",
            ],
        )

        gr.Markdown(
            "### Notes\n"
            "- This UI currently uses a built-in, rule-based response engine.\n"
            "- Swap `generate_reply()` in `triple_helix_engine.py` for an LLM/API when ready."
        )

    return demo


if __name__ == "__main__":
    demo = build_ui()
    port = int(os.environ.get("PORT", "7860"))
    demo.launch(server_name="0.0.0.0", server_port=port, show_api=False)

