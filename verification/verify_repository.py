"""Check documentation integrity without network access or external packages."""

from __future__ import annotations

from collections import Counter
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]


def prose_lines(text):
    """Omit fenced blocks when looking for headings and Markdown links."""
    fence = None
    result = []
    for line in text.splitlines():
        match = re.match(r"^\s*(`{3,}|~{3,})", line)
        if match:
            marker = match.group(1)
            if fence is None:
                fence = marker[0]
            elif marker[0] == fence:
                fence = None
            result.append("")
        elif fence is None:
            result.append(line)
        else:
            result.append("")
    if fence is not None:
        raise AssertionError("Unclosed fenced block")
    return result


def anchors(text):
    """GitHub-style slugs for this repository's plain-text headings."""
    found = set(re.findall(r'<a\s+id="([^"]+)"\s*>', text))
    used = Counter()
    for line in prose_lines(text):
        heading = re.match(r"^#{1,6}\s+(.+?)\s*#*\s*$", line)
        if not heading:
            continue
        title = heading.group(1).lower()
        title = re.sub(r"[^\w\- ]", "", title, flags=re.UNICODE)
        slug = title.replace(" ", "-")
        suffix = f"-{used[slug]}" if used[slug] else ""
        found.add(slug + suffix)
        used[slug] += 1
    return found


def run_checks() -> dict:
    docs = sorted(ROOT.rglob("*.md")) + [ROOT / "llms.txt"]
    texts = {path: path.read_text(encoding="utf-8") for path in docs}
    anchor_cache = {path: anchors(text) for path, text in texts.items()}
    checked_links = 0
    checked_fragments = 0
    errors = []
    for path, text in texts.items():
        relative = path.relative_to(ROOT).as_posix()
        controls = sorted({ord(ch) for ch in text if ord(ch) < 32 and ch not in "\n\t\r"})
        if controls:
            errors.append(f"{relative}: unexpected control characters {controls}")
        if "\\(" in text or "\\[" in text:
            errors.append(f"{relative}: noncanonical math delimiter")
        prose = "\n".join(prose_lines(text))
        for target in re.findall(r"!?\[[^\]]*\]\(([^\s)]+)\)", prose):
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc:
                continue
            checked_links += 1
            destination = (path.parent / unquote(parsed.path)).resolve() if parsed.path else path
            if not destination.is_relative_to(ROOT):
                errors.append(f"{relative}: link escapes repository: {target}")
                continue
            if not destination.exists():
                errors.append(f"{relative}: missing link target: {target}")
                continue
            if parsed.fragment and destination in anchor_cache:
                checked_fragments += 1
                if unquote(parsed.fragment) not in anchor_cache[destination]:
                    errors.append(f"{relative}: missing heading/anchor: {target}")

    milestone_path = ROOT / "learning" / "MILESTONES.md"
    milestone_text = milestone_path.read_text(encoding="utf-8")
    ids = re.findall(r"^#{2,4}\s+(M\d{2})\b", milestone_text, flags=re.MULTILINE)
    expected_ids = [f"M{j:02}" for j in range(1, 31)]
    if ids != expected_ids:
        errors.append(f"Milestone headings are not exactly M01–M30 in order: {ids}")
    if errors:
        raise AssertionError("\n".join(errors))
    return {
        "status": "passed",
        "documents_checked": len(docs),
        "relative_links_checked": checked_links,
        "heading_fragments_checked": checked_fragments,
        "milestone_count": len(ids),
        "milestone_ids_in_order": True,
        "unclosed_fences": 0,
        "unexpected_control_characters": 0,
        "scope": "Local links and plain-text heading slugs; not a hosted-rendering test.",
    }


if __name__ == "__main__":
    print(json.dumps(run_checks(), indent=2, sort_keys=True))
