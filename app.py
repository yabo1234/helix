from __future__ import annotations

import os

import gradio as gr

from prompt_history_logger import LOG_PATH
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


def get_history_file() -> str | None:
    if LOG_PATH.exists():
        return str(LOG_PATH)
    return None


def clear_history_file() -> str:
    if LOG_PATH.exists():
        LOG_PATH.unlink()
        return "Prompt history cleared."
    return "No prompt history file found."


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
            "### Prompt History\n"
            "Use the buttons below to download or clear the saved prompt and response history."
        )
        with gr.Row():
            download_btn = gr.Button("Download Prompt History")
            clear_history_btn = gr.Button("Clear Prompt History", variant="stop")
        history_file = gr.File(label="Prompt History File")
        clear_status = gr.Textbox(label="History Status", interactive=False)
        download_btn.click(fn=get_history_file, outputs=history_file)
        clear_history_btn.click(fn=clear_history_file, outputs=clear_status)

        gr.Markdown(
            "### Notes\n"
            "- This UI currently uses a built-in, rule-based response engine.\n"
            "- Prompt/response history is saved locally to `prompt_history.jsonl`.\n"
            "- Swap `generate_reply()` in `triple_helix_engine.py` for an LLM/API when ready."
        )

    return demo


if __name__ == "__main__":
    demo = build_ui()
    port = int(os.environ.get("PORT", "7860"))
    demo.launch(server_name="0.0.0.0", server_port=port, show_api=False)
