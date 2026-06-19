from __future__ import annotations

import os
import gradio as gr


def chat_fn(message, history):
    return f"You said: {message}"


def build_ui():
    with gr.Blocks(title="Triple-Helix Chatbot") as demo:
        gr.Markdown("## Triple-Helix Chatbot")
        gr.ChatInterface(
            fn=chat_fn,
            chatbot=gr.Chatbot(height=420),
        )
    return demo

if __name__ == "__main__":
    demo = build_ui()
    port = int(os.environ.get("PORT", "7860"))
    demo.launch(server_name="127.0.0.1", server_port=port)