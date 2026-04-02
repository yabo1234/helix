from __future__ import annotations

import os

import gradio as gr

from triple_helix_engine import generate_reply


APP_TITLE = "Triple-Helix Chatbot"


def get_app_description() -> str:
    """Generate app description based on configured LLM provider."""
    provider = os.environ.get("LLM_PROVIDER", "rule-based").lower()
    
    base_description = (
        "A lightweight UI that helps you think through innovation using the "
        "Academia × Industry × Government (Triple Helix) framework."
    )
    
    if provider == "deepseek":
        return f"{base_description}\n\n**Powered by DeepSeek AI** 🤖"
    elif provider == "openai":
        return f"{base_description}\n\n**Powered by OpenAI** 🤖"
    else:
        return f"{base_description}\n\n**Using rule-based responses** (configure LLM_PROVIDER for AI-powered responses)"


APP_DESCRIPTION = get_app_description()


def chat_fn(message: str, history: list[dict[str, str]]):
    # Gradio ChatInterface passes history as a list of {"role": "...", "content": "..."}
    # in newer versions; we keep it generic and only use it for metadata.
    reply = generate_reply(message=message, history=history)
    # If you want to surface metadata in the UI later, you can append it here.
    return reply.answer


def build_ui() -> gr.Blocks:
    with gr.Blocks(title=APP_TITLE) as demo:
        gr.Markdown(f"## {APP_TITLE}\n\n{APP_DESCRIPTION}")

        gr.ChatInterface(
            fn=chat_fn,
            chatbot=gr.Chatbot(height=420),
            textbox=gr.Textbox(
                placeholder="Describe your innovation challenge or idea…",
                lines=2,
            ),
            examples=[
                "Help me design a university–startup–government pilot for renewable energy forecasting.",
                "How do I structure a consortium for an AI healthcare product while staying compliant?",
                "I want funding for a smart agriculture prototype. What should the proposal include?",
            ],
        )

        gr.Markdown(
            "### Configuration\n"
            "- Set `LLM_PROVIDER=deepseek` (or `openai`) in a `.env` file to use AI-powered responses.\n"
            "- For DeepSeek: Set `DEEPSEEK_API_KEY` with your API key from https://platform.deepseek.com/\n"
            "- For OpenAI: Set `OPENAI_API_KEY` with your OpenAI API key.\n"
            "- See `.env.example` for all configuration options."
        )

    return demo


if __name__ == "__main__":
    demo = build_ui()
    port = int(os.environ.get("PORT", "7860"))
    demo.launch(
        server_name="0.0.0.0",
        server_port=port
    )

