from __future__ import annotations
import os
import gradio as gr
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=os.environ.get("AZURE_OPENAI_API_KEY", ""),
    azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT", ""),
    api_version="2024-08-01-preview"
)

def chat_fn(message, history):
    try:
        messages = [{"role": "system", "content": "You are Triple Helix Engine assistant."}]
        for h, a in history:
            messages.append({"role": "user", "content": h})
            messages.append({"role": "assistant", "content": a})
        messages.append({"role": "user", "content": message})
        response = client.chat.completions.create(
            model=os.environ.get("AZURE_OPENAI_DEPLOYMENT", "gpt-4o-mini"),
            messages=messages,
            max_tokens=800
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

demo = gr.ChatInterface(
    fn=chat_fn,
    title="🤖 Triple Helix Engine",
    description="Powered by Azure OpenAI"
)

app = demo.app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    demo.launch(
        server_name="0.0.0.0",
        server_port=port,
        show_error=True
    )
