from __future__ import annotations

import os
import gradio as gr
from openai import AzureOpenAI

# Azure OpenAI Client
client = AzureOpenAI(
    api_key=os.environ.get("AZURE_OPENAI_API_KEY"),
    azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
    api_version="2024-08-01-preview"
)

def chat_fn(message, history):
    try:
        # Build conversation history
        messages = [
            {
                "role": "system",
                "content": "You are Triple Helix Engine, a helpful AI assistant."
            }
        ]
        
        # Add chat history
        for human, assistant in history:
            messages.append({"role": "user", "content": human})
            messages.append({"role": "assistant", "content": assistant})
        
        # Add current message
        messages.append({"role": "user", "content": message})
        
        # Call Azure OpenAI
        response = client.chat.completions.create(
            model=os.environ.get("AZURE_OPENAI_DEPLOYMENT", "gpt-4o-mini"),
            messages=messages,
            max_tokens=800,
            temperature=0.7
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"Error: {str(e)}"


def build_ui():
    with gr.Blocks(title="Triple-Helix Chatbot") as demo:
        gr.Markdown("## 🤖 Triple-Helix Chatbot")
        gr.Markdown("Powered by Azure OpenAI")
        gr.ChatInterface(
            fn=chat_fn,
            chatbot=gr.Chatbot(height=420),
        )
    return demo


# Required for gunicorn
demo = build_ui()
app = demo.app          # ✅ Exposes Gradio as WSGI app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    demo.launch(
        server_name="0.0.0.0",    # ✅ Fixed from 127.0.0.1
        server_port=port
    )
