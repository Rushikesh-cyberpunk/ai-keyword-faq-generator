"""
cli.py
------
Command-line interface: gathers input from the user, drives the
generation flow, displays results, and offers regenerate/export options.
"""

from . import config
from .gemini_client import GeminiClient, GeminiClientError
from .generator import generate_keywords_and_faqs, GenerationError
from .exporter import export_result


def print_header(title: str) -> None:
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def get_input_text() -> str:
    """
    Lets the user either paste text directly or point to a file.
    """
    print_header("STEP 1: Provide your text")
    print("Choose input method:")
    print("  1. Paste text directly")
    print("  2. Load from a .txt file")
    choice = input("Enter 1 or 2: ").strip()

    if choice == "2":
        path = input("Enter path to .txt file: ").strip()
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            print(f"File not found: {path}")
            return ""
        except OSError as e:
            print(f"Could not read file: {e}")
            return ""
    else:
        print("Paste your text below. Press Enter, then type END on its own line to finish:")
        lines = []
        while True:
            line = input()
            if line.strip() == "END":
                break
            lines.append(line)
        return "\n".join(lines)


def get_int_input(prompt: str, default: int) -> int:
    raw = input(f"{prompt} [default {default}]: ").strip()
    if not raw:
        return default
    try:
        return int(raw)
    except ValueError:
        print(f"Not a valid number, using default ({default}).")
        return default


def display_results(result: dict) -> None:
    print_header("KEYWORDS")
    for i, kw in enumerate(result.get("keywords", []), 1):
        print(f"  {i}. {kw}")

    print_header("FREQUENTLY ASKED QUESTIONS")
    for i, faq in enumerate(result.get("faqs", []), 1):
        print(f"\nQ{i}: {faq.get('question', '')}")
        print(f"A{i}: {faq.get('answer', '')}")


def handle_export(result: dict) -> None:
    choice = input("\nExport results? (json / txt / no): ").strip().lower()
    if choice in ("json", "txt"):
        try:
            path = export_result(result, choice)
            print(f"Saved to {path}")
        except Exception as e:
            print(f"Export failed: {e}")


def run() -> None:
    print_header("AI Keyword & FAQ Generator (powered by Gemini)")

    try:
        config.validate_config()
    except config.ConfigError as e:
        print(f"\nConfiguration error:\n{e}")
        return

    client = GeminiClient()

    text = get_input_text()

    print_header("STEP 2: Customize output")
    num_keywords = get_int_input("How many keywords?", 12)
    num_faqs = get_int_input("How many FAQs?", 7)

    while True:
        try:
            print("\nGenerating results, please wait...")
            result = generate_keywords_and_faqs(client, text, num_keywords, num_faqs)
        except GenerationError as e:
            print(f"\nError: {e}")
            return
        except GeminiClientError as e:
            print(f"\nAPI error: {e}")
            return

        display_results(result)
        handle_export(result)

        again = input("\nRegenerate a new set of results? (y/n): ").strip().lower()
        if again != "y":
            break

    print("\nDone. Thanks for using the AI Keyword & FAQ Generator!")


if __name__ == "__main__":
    run()