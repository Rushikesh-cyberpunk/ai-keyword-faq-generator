"""
exporter.py
-----------
Handles saving results to disk as .txt or .json.
"""

import json
from datetime import datetime
from pathlib import Path


def export_to_json(result: dict, output_dir: str = "output") -> str:
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    filename = f"result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    filepath = Path(output_dir) / filename

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    return str(filepath)


def export_to_txt(result: dict, output_dir: str = "output") -> str:
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    filename = f"result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    filepath = Path(output_dir) / filename

    lines = ["KEYWORDS", "=" * 40]
    for i, kw in enumerate(result.get("keywords", []), 1):
        lines.append(f"{i}. {kw}")

    lines.append("")
    lines.append("FAQs")
    lines.append("=" * 40)
    for i, faq in enumerate(result.get("faqs", []), 1):
        lines.append(f"Q{i}: {faq.get('question', '')}")
        lines.append(f"A{i}: {faq.get('answer', '')}")
        lines.append("")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    return str(filepath)


def export_result(result: dict, fmt: str, output_dir: str = "output") -> str:
    fmt = fmt.lower().strip()
    if fmt == "json":
        return export_to_json(result, output_dir)
    elif fmt == "txt":
        return export_to_txt(result, output_dir)
    else:
        raise ValueError("Export format must be 'json' or 'txt'.")