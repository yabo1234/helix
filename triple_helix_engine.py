import os
import requests

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
API_URL = "https://models.inference.ai.azure.com/chat/completions"
MODEL_NAME = "mistral-nemo-instruct"


def _call_model(messages, model: str = MODEL_NAME) -> str:
    if not GITHUB_TOKEN:
        raise RuntimeError("GITHUB_TOKEN is not set in environment variables.")

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": model,
        "messages": messages,
    }

    resp = requests.post(API_URL, headers=headers, json=payload, timeout=60)
    resp.raise_for_status()
    data = resp.json()
    return data["choices"][0]["message"]["content"]


def analyze_policy(topic: str) -> str:
    messages = [
        {
            "role": "system",
            "content": (
                "You are a policy analyst specializing in innovation systems, "
                "Triple Helix models, and digital governance. Provide structured, "
                "evidence-based analysis with clear sections."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Analyze the following topic using the Triple Helix framework "
                f"(Government–Industry–Academia):\n\n{topic}\n\n"
                "Include:\n"
                "1. Executive summary\n"
                "2. Triple Helix actor map\n"
                "3. Constraints and opportunities\n"
                "4. Policy recommendations\n"
                "5. Risks and mitigation\n"
                "6. Short Amharic summary"
            ),
        },
    ]
    return _call_model(messages)


def triple_helix_map(sector: str) -> str:
    messages = [
        {
            "role": "system",
            "content": (
                "You generate structured Triple Helix innovation maps. "
                "Output must be valid JSON."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Create a Triple Helix innovation map for:\n\n{sector}\n\n"
                "Output JSON:\n"
                "{\n"
                '  "government": [...],\n'
                '  "industry": [...],\n'
                '  "academia": [...],\n'
                '  "interactions": [...],\n'
                '  "gaps": [...],\n'
                '  "opportunities": [...]\n'
                "}"
            ),
        },
    ]
    return _call_model(messages)


def translate_to_amharic(text: str) -> str:
    messages = [
        {
            "role": "system",
            "content": (
                "You translate between English and Amharic with high fidelity. "
                "Preserve meaning, tone, and technical terminology."
            ),
        },
        {
            "role": "user",
            "content": f"Translate this into Amharic:\n\n{text}",
        },
    ]
    return _call_model(messages)


def write_research_paper(topic: str) -> str:
    messages = [
        {
            "role": "system",
            "content": (
                "You write long-form research papers with academic structure. "
                "Use headings, citations, and analytical depth."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Write a research paper on:\n\n{topic}\n\n"
                "Include:\n"
                "- Abstract\n"
                "- Background\n"
                "- Literature review\n"
                "- Analysis\n"
                "- Case studies\n"
                "- Policy implications\n"
                "- Conclusion\n"
                "- Harvard-style references"
            ),
        },
    ]
    return _call_model(messages)
