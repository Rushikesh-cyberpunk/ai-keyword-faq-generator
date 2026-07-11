"""
generator.py
------------
Builds the prompt sent to Gemini and parses the structured JSON
response into plain Python objects (keywords list + FAQ list).

See PROMPTS.md in the project root for an explanation of why the
prompt is written the way it is.
"""

import json
import re

from .gemini_client import GeminiClient, GeminiClientError


class GenerationError(Exception):
    """Raised when input is invalid or the model's output can't be parsed."""


PROMPT_TEMPLATE = """You are an expert content analyst. Read the TEXT below and produce:
1. Exactly {num_keywords} of the most important keywords or key phrases from the text.
2. Exactly {num_faqs} frequently asked questions a reader might have about the text, each with a clear, accurate answer based only on the text.

Respond with ONLY valid JSON (no markdown code fences, no commentary, no extra text
before or after). Use exactly this structure:

{{
  "keywords": ["keyword 1", "keyword 2", "..."],
  "faqs": [
    {{"question": "...", "answer": "..."}},
    {{"question": "...", "answer": "..."}}
  ]
}}

TEXT:
\"\"\"
{text}
\"\"\"
"""


def build_prompt(text: str, num_keywords: int, num_faqs: int) -> str:
    return PROMPT_TEMPLATE.format(
        num_keywords=num_keywords, num_faqs=num_faqs, text=text.strip()
    )


def _extract_json(raw_text: str) -> dict:
    """
    Gemini is instructed to return raw JSON, but models sometimes wrap
    it in ```json ... ``` fences anyway. This strips those if present,
    then parses. Falls back to grabbing the first {...} block found.
    """
    cleaned = raw_text.strip()
    cleaned = re.sub(r"^```(json)?", "", cleaned).strip()
    cleaned = re.sub(r"```$", "", cleaned).strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass

    # Fallback: find the outermost { ... } block
    match = re.search(r"\{.*\}", cleaned, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass

    raise GenerationError(
        "Could not parse a valid JSON response from the model. "
        "Raw response was:\n" + raw_text[:500]
    )


def validate_input_text(text: str) -> None:
    if text is None or not text.strip():
        raise GenerationError("Input text is empty. Please provide some text to analyze.")
    if len(text.strip()) < 50:
        raise GenerationError(
            "Input text is too short to generate meaningful keywords and FAQs "
            "(minimum ~50 characters)."
        )


def generate_keywords_and_faqs(
    client: GeminiClient, text: str, num_keywords: int = 12, num_faqs: int = 7
) -> dict:
    """
    Main entry point used by the CLI.
    Returns: {"keywords": [...], "faqs": [{"question": ..., "answer": ...}, ...]}
    """
    validate_input_text(text)

    if not (1 <= num_keywords <= 30):
        raise GenerationError("num_keywords must be between 1 and 30.")
    if not (1 <= num_faqs <= 20):
        raise GenerationError("num_faqs must be between 1 and 20.")

    prompt = build_prompt(text, num_keywords, num_faqs)

    try:
        raw_response = client.generate(prompt)
    except GeminiClientError as e:
        raise GenerationError(f"API error while generating results: {e}")

    result = _extract_json(raw_response)

    if "keywords" not in result or "faqs" not in result:
        raise GenerationError(
            "Model response was valid JSON but missing 'keywords' or 'faqs' keys."
        )

    return result