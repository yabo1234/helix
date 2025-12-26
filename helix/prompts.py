from __future__ import annotations

import textwrap
from typing import Iterable


def default_system_prompt(extra_docs: Iterable[str] = ()) -> str:
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

    docs = [d.strip() for d in extra_docs if d and d.strip()]
    if not docs:
        return base

    joined = "\n\n".join(f"--- Context Document {i} ---\n{d}\n--- End Context Document {i} ---" for i, d in enumerate(docs, start=1))
    return base + "\n\nReference documents (use these when relevant):\n\n" + joined
