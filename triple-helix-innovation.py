#!/usr/bin/env python3
"""
Triple Helix Innovation Chatbot (CLI)

Text-only command-line chatbot that:
- Starts with: "welcome to the triple helix  innovation chatbot"
- Asks for a directory containing up to 2 PDFs to include as context
- Calls OpenAI Chat Completions API with model "triplehelix"
- Instructs the model to keep answers consistent with Triple Helix innovation research
  and to provide citations to facts/papers/reports.
- Logs a timestamped transcript file.

Environment:
- OPENAI_API_KEY must be set unless HELIX_DRY_RUN=true.
- Optional: OPENAI_BASE_URL (defaults to https://api.openai.com/v1)
- Optional: HELIX_DRY_RUN=true to run without OpenAI calls (useful for quick testing)

PDF extraction:
- Uses `pypdf` if available. If not installed, PDFs will be skipped with a warning.
"""

from __future__ import annotations

import datetime as _dt
import json
import os
import sys
import textwrap
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional


WELCOME = "welcome to the triple helix  innovation chatbot"
MODEL = os.getenv("HELIX_MODEL", "gpt-5.2").strip() or "gpt-5.2"
DRY_RUN = os.getenv("HELIX_DRY_RUN", "false").lower() in {"1", "true", "yes"}

# Keep PDF context bounded (characters) to avoid huge prompts.
MAX_PDF_CHARS_PER_FILE = 30_000
MAX_PDF_TOTAL_CHARS = 60_000


def _utc_now() -> _dt.datetime:
    return _dt.datetime.now(tz=_dt.timezone.utc)


def _ts() -> str:
    return _utc_now().strftime("%Y-%m-%d %H:%M:%S UTC")


def _safe_input(prompt: str) -> str:
    try:
        return input(prompt)
    except (EOFError, KeyboardInterrupt):
        print()
        return "exit"


def _ensure_openai_key() -> str:
    key = os.getenv("OPENAI_API_KEY", "").strip()
    if not key:
        raise RuntimeError(
            "Missing OPENAI_API_KEY. Set it, e.g.\n"
            "  export OPENAI_API_KEY='...'\n"
        )
    return key


def _base_url() -> str:
    return os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/")


def _dry_run_answer(user_text: str, pdf_context: List[Dict[str, str]]) -> str:
    """Offline answer used when HELIX_DRY_RUN=true (no OpenAI calls)."""
    docs_note = ""
    if pdf_context:
        docs_note = (
            "\n\n"
            f"Context: {len(pdf_context)} PDF(s) were loaded, but dry-run mode does not do full document reasoning. "
            "If you paste a relevant excerpt, I can respond more precisely."
        )

    question = user_text.strip()
    if not question:
        return "(No input.)"

    # Keep responses predictable and research-consistent, with canonical citations.
    return (
        f"Here’s a Triple Helix lens on your question: “{question}”\n\n"
        "A practical way to analyze it is to separate roles and interfaces:\n"
        "- University (academia): knowledge creation, skills, research infrastructure, tech transfer pathways.\n"
        "- Industry (business): problem-pull, scaling/commercialization, complementary assets, demand signals.\n"
        "- Government (public sector): rules/standards, mission setting, funding, procurement, convening.\n"
        "- Interfaces: joint labs, incubators, public–private partnerships, science parks, challenge programs.\n\n"
        "If you tell me the geography/sector and the outcome you want (e.g., startups, patents, productivity, jobs), "
        "I can translate this into concrete interventions and metrics."
        f"{docs_note}\n\n"
        "Sources: [Leydesdorff & Etzkowitz, 1998]; [Etzkowitz & Leydesdorff, 2000]; [Etzkowitz, 2008]."
    )


def _read_pdf_texts(pdf_dir: Path, max_pdfs: int = 2) -> List[Dict[str, str]]:
    """
    Returns: list of {"filename": str, "text": str}
    """
    if not pdf_dir.exists() or not pdf_dir.is_dir():
        return []

    pdf_paths = sorted([p for p in pdf_dir.iterdir() if p.is_file() and p.suffix.lower() == ".pdf"])
    pdf_paths = pdf_paths[:max_pdfs]
    if not pdf_paths:
        return []

    try:
        # pypdf is the modern replacement for PyPDF2
        from pypdf import PdfReader  # type: ignore
    except Exception:
        print(
            "Note: PDF support requires 'pypdf'. PDFs will be skipped.\n"
            "Install with: pip install pypdf",
            file=sys.stderr,
        )
        return []

    results: List[Dict[str, str]] = []
    total_chars = 0
    for path in pdf_paths:
        try:
            reader = PdfReader(str(path))
            parts: List[str] = []
            for page in reader.pages:
                try:
                    parts.append(page.extract_text() or "")
                except Exception:
                    parts.append("")
            text = "\n".join(parts).strip()
        except Exception as e:
            text = f"[PDF read error: {e}]"

        if len(text) > MAX_PDF_CHARS_PER_FILE:
            text = text[:MAX_PDF_CHARS_PER_FILE] + "\n...[truncated]..."

        remaining = MAX_PDF_TOTAL_CHARS - total_chars
        if remaining <= 0:
            break
        if len(text) > remaining:
            text = text[:remaining] + "\n...[truncated total]..."

        total_chars += len(text)
        results.append({"filename": path.name, "text": text})

    return results


def _build_system_prompt(pdf_context: List[Dict[str, str]]) -> str:
    base = textwrap.dedent(
        """
        You are the Triple Helix Innovation Chatbot.

        Constraints:
        - All answers must be consistent with Triple Helix innovation research (university–industry–government interactions; innovation systems; knowledge/technology transfer).
        - Provide citations for factual claims (papers, reports, or credible sources). Use inline citations like:
          [Author, Year] or [Report Name, Year] and include a short "Sources" section when appropriate.
        - If a claim is uncertain or not supported by the provided context, say so and ask clarifying questions.
        - Prefer evidence-based, specific, and actionable answers.
        """
    ).strip()

    if not pdf_context:
        return base

    docs = []
    for i, item in enumerate(pdf_context, start=1):
        docs.append(
            textwrap.dedent(
                f"""
                --- Document {i}: {item['filename']} ---
                {item['text']}
                --- End Document {i} ---
                """
            ).strip()
        )

    return base + "\n\nReference documents (use these when relevant):\n\n" + "\n\n".join(docs)


@dataclass
class OpenAIChatClient:
    api_key: str
    base_url: str

    def chat_completions(self, messages: List[Dict[str, str]], model: str = MODEL) -> str:
        # Prefer the official OpenAI SDK (Responses API), but keep a legacy HTTP fallback.
        try:
            from openai import OpenAI  # type: ignore

            system_prompt = ""
            history = messages
            if messages and messages[0].get("role") == "system":
                system_prompt = messages[0].get("content", "")
                history = messages[1:]

            def _render(hist: List[Dict[str, str]]) -> str:
                parts: List[str] = []
                for m in hist:
                    role = (m.get("role") or "").lower()
                    content = m.get("content") or ""
                    if not content:
                        continue
                    if role == "user":
                        parts.append(f"User: {content}")
                    elif role == "assistant":
                        parts.append(f"Assistant: {content}")
                    else:
                        parts.append(f"{role.capitalize() or 'Message'}: {content}")
                return "\n".join(parts).strip()

            client = OpenAI(api_key=self.api_key, base_url=self.base_url)
            resp = client.responses.create(
                model=model,
                instructions=system_prompt,
                input=_render(history),
                temperature=0.2,
            )
            text = getattr(resp, "output_text", None)
            return (text or "").strip() or "(No response.)"
        except Exception:
            # Legacy HTTP fallback: Chat Completions endpoint.
            url = f"{self.base_url}/chat/completions"
            payload: Dict[str, Any] = {
                "model": model,
                "messages": messages,
                "temperature": 0.2,
            }
            req = urllib.request.Request(
                url=url,
                data=json.dumps(payload).encode("utf-8"),
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                method="POST",
            )
            try:
                with urllib.request.urlopen(req, timeout=120) as resp:
                    raw = resp.read().decode("utf-8")
            except urllib.error.HTTPError as e:
                body = ""
                try:
                    body = e.read().decode("utf-8")
                except Exception:
                    body = ""
                raise RuntimeError(f"OpenAI HTTP error {e.code}: {body or e.reason}") from e
            except urllib.error.URLError as e:
                raise RuntimeError(f"OpenAI connection error: {e}") from e

            data = json.loads(raw)
            try:
                return data["choices"][0]["message"]["content"]
            except Exception:
                raise RuntimeError(f"Unexpected OpenAI response: {data}")


def _transcript_path() -> Path:
    logs_dir = Path.cwd() / "transcripts"
    logs_dir.mkdir(parents=True, exist_ok=True)
    stamp = _utc_now().strftime("%Y%m%d_%H%M%S_UTC")
    return logs_dir / f"triple_helix_chat_{stamp}.txt"


def _log_line(fp, who: str, text: str) -> None:
    fp.write(f"[{_ts()}] {who}: {text}\n")
    fp.flush()


def main() -> int:
    print(WELCOME)

    pdf_dir_str = _safe_input("Enter a directory path containing up to 2 PDFs (or press Enter to skip): ").strip()
    pdf_context: List[Dict[str, str]] = []
    if pdf_dir_str:
        pdf_context = _read_pdf_texts(Path(pdf_dir_str).expanduser())
        if pdf_context:
            print(f"Loaded {len(pdf_context)} PDF(s) for context.")
        else:
            print("No PDFs loaded (directory missing/empty, or PDF parsing not available).")

    system_prompt = _build_system_prompt(pdf_context)
    messages: List[Dict[str, str]] = [{"role": "system", "content": system_prompt}]

    transcript_file = _transcript_path()
    with transcript_file.open("w", encoding="utf-8") as fp:
        _log_line(fp, "SYSTEM", WELCOME)
        if pdf_dir_str:
            _log_line(fp, "SYSTEM", f"PDF directory: {pdf_dir_str}")
            _log_line(fp, "SYSTEM", f"PDFs loaded: {[d['filename'] for d in pdf_context]}")

        if DRY_RUN:
            _log_line(fp, "SYSTEM", "HELIX_DRY_RUN=true (no OpenAI calls)")
            client: OpenAIChatClient | None = None
            print("Dry-run mode enabled (HELIX_DRY_RUN=true). No OpenAI calls will be made.")
        else:
            try:
                client = OpenAIChatClient(api_key=_ensure_openai_key(), base_url=_base_url())
            except Exception as e:
                _log_line(fp, "ERROR", str(e))
                print(str(e), file=sys.stderr)
                return 2

        print("Type your message and press Enter. Type 'exit' to quit.")

        while True:
            user_text = _safe_input("> ").strip()
            if not user_text:
                continue
            if user_text.lower() in {"exit", "quit"}:
                _log_line(fp, "USER", user_text)
                _log_line(fp, "SYSTEM", "Session ended.")
                break

            _log_line(fp, "USER", user_text)
            messages.append({"role": "user", "content": user_text})

            if DRY_RUN:
                assistant_text = _dry_run_answer(user_text, pdf_context).strip()
            else:
                assert client is not None
                try:
                    assistant_text = client.chat_completions(messages=messages, model=MODEL).strip()
                except Exception as e:
                    err = f"Error calling OpenAI: {e}"
                    print(err, file=sys.stderr)
                    _log_line(fp, "ERROR", err)
                    continue

            if not assistant_text:
                assistant_text = "(No response.)"

            print(assistant_text)
            _log_line(fp, "ASSISTANT", assistant_text)
            messages.append({"role": "assistant", "content": assistant_text})

    print(f"Transcript saved to: {transcript_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
