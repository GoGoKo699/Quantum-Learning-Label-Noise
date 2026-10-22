"""Check documentation integrity and the fixed public learning-map requirements."""

from __future__ import annotations

from collections import Counter
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
MILESTONE_IDS = [f"M{j:02}" for j in range(1, 31)]
REQUIRED_FIELDS = (
    "Central question",
    "Understanding target",
    "Dependencies and story role",
    "Conceptual connection",
    "Source pointers",
)
LEARNING_FILES = (
    "learning/README.md",
    "learning/ANCHOR_BRIDGE.md",
    "learning/TUTORIAL.md",
    "learning/MILESTONES.md",
)


def prose_lines(text):
    """Omit fenced blocks; require a matching closing character and length."""
    fence = None
    result = []
    for line in text.splitlines():
        match = re.match(r"^\s*(`{3,}|~{3,})", line)
        if match:
            marker = match.group(1)
            if fence is None:
                fence = (marker[0], len(marker))
            elif (
                marker[0] == fence[0]
                and len(marker) >= fence[1]
                and not line[match.end():].strip()
            ):
                fence = None
            result.append("")
        elif fence is None:
            result.append(line)
        else:
            result.append("")
    if fence is not None:
        raise AssertionError("Unclosed fenced block")
    return result


def explicit_anchors(text):
    prose = "\n".join(prose_lines(text))
    return [
        match.group(2)
        for match in re.finditer(
            r"""<a\b[^>]*?\b(?:id|name)\s*=\s*(["'])(.*?)\1""", prose, re.I
        )
    ]


def anchors(text):
    """GitHub-style slugs for this repository's plain-text headings."""
    found = set(explicit_anchors(text))
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


def validate_math(prose):
    """Check delimiters and concrete GitHub math/table compatibility defects."""
    errors = []
    opened = False
    expressions = 0
    for match in re.finditer(r"\$`|`\$", prose):
        token = match.group()
        line = prose.count("\n", 0, match.start()) + 1
        if token == "$`":
            if opened:
                errors.append(f"nested inline-math opener at line {line}")
            opened = True
        else:
            if not opened:
                errors.append(f"inline-math closer without opener at line {line}")
            else:
                expressions += 1
            opened = False
    if opened:
        errors.append("unclosed inline-math expression")
    if re.search(r"(?<!\\)\\[()[\]]", prose) or "$$" in prose:
        errors.append("noncanonical prose math delimiter")
    for number, line in enumerate(prose.splitlines(), 1):
        if not line.lstrip().startswith("|"):
            continue
        for expression in re.findall(r"\$`(.*?)`\$", line):
            # An odd number of preceding backslashes escapes a Markdown pipe.
            if any(
                len(match.group(1)) % 2 == 0
                for match in re.finditer(r"(\\*)\|", expression)
            ):
                errors.append(f"unescaped pipe inside table-cell math at line {number}")
    return expressions, errors


def math_expressions(text):
    """Extract actual math, excluding literal macro examples in ordinary code."""
    expressions = re.findall(r"\$`(.*?)`\$", "\n".join(prose_lines(text)), re.S)
    fence = None
    is_math = False
    collected = []
    for line in text.splitlines():
        match = re.match(r"^\s*(`{3,}|~{3,})(.*)$", line)
        if fence is None:
            if match:
                marker, information = match.groups()
                fence = (marker[0], len(marker))
                is_math = information.strip().lower() == "math"
                collected = []
        elif (
            match
            and match.group(1)[0] == fence[0]
            and len(match.group(1)) >= fence[1]
            and not match.group(2).strip()
        ):
            if is_math:
                expressions.append("\n".join(collected))
            fence = None
        elif is_math:
            collected.append(line)
    return expressions


def validate_milestones(text):
    """Validate fixed fields and earlier-only references in Dependencies lines."""
    headings = list(re.finditer(r"^#{2,4}\s+(M\d+)\b[^\n]*", text, re.MULTILINE))
    ids = [match.group(1) for match in headings]
    phases = list(re.finditer(r"^##\s+Phase\s+([IVXLCDM]+)\b", text, re.MULTILINE))
    errors = []
    if ids != MILESTONE_IDS:
        errors.append(f"headings are not exactly M01–M30 in order: {ids}")
    if [match.group(1) for match in phases] != ["I", "II"]:
        errors.append("phase headings must be Phase I followed by Phase II")
    phase_counts = Counter()
    dependencies_checked = 0
    map_anchors = anchors(text)
    for index, heading in enumerate(headings):
        milestone = heading.group(1)
        preceding = [phase for phase in phases if phase.start() < heading.start()]
        phase = preceding[-1].group(1) if preceding else None
        phase_counts[phase] += 1
        if milestone in MILESTONE_IDS:
            expected_phase = "I" if int(milestone[1:]) <= 14 else "II"
            if phase != expected_phase:
                errors.append(f"{milestone}: must belong to Phase {expected_phase}")
            if milestone.lower() not in map_anchors:
                errors.append(f"{milestone}: missing stable anchor #{milestone.lower()}")
        end = headings[index + 1].start() if index + 1 < len(headings) else len(text)
        block = text[heading.end():end]
        fields = {}
        for field in REQUIRED_FIELDS:
            pattern = r"^\*\*" + re.escape(field) + r"\.\*\*[ \t]*([^\n]*)$"
            values = re.findall(pattern, block, re.MULTILINE)
            if len(values) != 1 or not values[0].strip():
                errors.append(f"{milestone}: requires one nonempty '{field}' field")
            else:
                fields[field] = values[0]
        dependency_line = fields.get("Dependencies and story role", "")
        references = sorted(
            {value.upper() for value in re.findall(r"\bM\d+\b", dependency_line, re.I)}
        )
        for reference in references:
            dependencies_checked += 1
            if reference not in MILESTONE_IDS:
                errors.append(f"{milestone}: unknown dependency {reference}")
            elif milestone in MILESTONE_IDS and int(reference[1:]) >= int(milestone[1:]):
                errors.append(f"{milestone}: dependency {reference} is not earlier")
    if phase_counts != Counter({"I": 14, "II": 16}):
        errors.append(f"expected 14 Phase-I and 16 Phase-II milestones: {dict(phase_counts)}")
    return {
        "milestone_count": len(ids),
        "milestone_ids_in_order": ids == MILESTONE_IDS,
        "milestone_phase_membership": dict(phase_counts),
        "required_fields_per_milestone": list(REQUIRED_FIELDS),
        "dependency_references_checked": dependencies_checked,
    }, errors


def reachable(graph, start):
    seen = set()
    pending = [start]
    while pending:
        current = pending.pop()
        if current not in seen:
            seen.add(current)
            pending.extend(graph.get(current, set()) - seen)
    return seen


def run_checks() -> dict:
    required = [ROOT / name for name in (*LEARNING_FILES, "README.md", "llms.txt")]
    missing = [path.relative_to(ROOT).as_posix() for path in required if not path.is_file()]
    if missing:
        raise AssertionError(f"Missing required documentation: {missing}")
    docs = sorted(ROOT.rglob("*.md")) + [ROOT / "llms.txt"]
    texts = {path: path.read_text(encoding="utf-8") for path in docs}
    anchor_cache = {path: anchors(text) for path, text in texts.items()}
    checked_links = 0
    checked_fragments = 0
    errors = []
    graph = {path: set() for path in texts}
    inline_math_count = 0
    explicit_anchor_count = 0
    for path, text in texts.items():
        relative = path.relative_to(ROOT).as_posix()
        controls = sorted({ord(ch) for ch in text if ord(ch) < 32 and ch not in "\n\t\r"})
        if controls:
            errors.append(f"{relative}: unexpected control characters {controls}")
        if any(r"\operatorname" in expression for expression in math_expressions(text)):
            errors.append(f"{relative}: unsupported GitHub math macro \\operatorname")
        prose = "\n".join(prose_lines(text))
        if path in required and not text.strip():
            errors.append(f"{relative}: required document is empty")
        explicit = explicit_anchors(text)
        explicit_anchor_count += len(explicit)
        duplicates = sorted(key for key, count in Counter(explicit).items() if count > 1)
        if duplicates:
            errors.append(f"{relative}: duplicate explicit anchors {duplicates}")
        count, math_errors = validate_math(prose)
        inline_math_count += count
        errors.extend(f"{relative}: {error}" for error in math_errors)
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
            if destination in texts:
                graph[path].add(destination)
            if parsed.fragment and destination in anchor_cache:
                checked_fragments += 1
                if unquote(parsed.fragment) not in anchor_cache[destination]:
                    errors.append(f"{relative}: missing heading/anchor: {target}")

    milestone_path = ROOT / "learning" / "MILESTONES.md"
    milestone_text = milestone_path.read_text(encoding="utf-8")
    milestone_summary, milestone_errors = validate_milestones(milestone_text)
    errors.extend(f"learning/MILESTONES.md: {error}" for error in milestone_errors)
    learning_readme = texts[ROOT / "learning" / "README.md"]
    if not re.search(r"\bWatrous\b", learning_readme, re.I) or not re.search(r"\b2018\b", learning_readme):
        errors.append("learning/README.md: selected Watrous (2018) anchor is not recorded")
    if "watrous2018" not in anchor_cache[ROOT / "learning" / "ANCHOR_BRIDGE.md"]:
        errors.append("learning/ANCHOR_BRIDGE.md: selected-source anchor #watrous2018 is missing")
    navigation = {}
    for entry in ("README.md", "llms.txt", "learning/README.md"):
        accessible = reachable(graph, ROOT / entry)
        navigation[entry] = []
        for name in LEARNING_FILES:
            if ROOT / name in accessible:
                navigation[entry].append(name)
            else:
                errors.append(f"{entry}: no local-link route to {name}")
    if errors:
        raise AssertionError("\n".join(errors))
    return {
        "status": "passed",
        "passed": True,
        "documents_checked": len(docs),
        "relative_links_checked": checked_links,
        "heading_fragments_checked": checked_fragments,
        **milestone_summary,
        "explicit_anchors_checked": explicit_anchor_count,
        "duplicate_explicit_anchors": 0,
        "inline_math_expressions_checked": inline_math_count,
        "selected_educational_anchor": "watrous2018",
        "learning_navigation": navigation,
        "unclosed_fences": 0,
        "unexpected_control_characters": 0,
        "unsupported_math_macros": 0,
        "unescaped_table_math_pipes": 0,
        "scope": "Learning-map requirements, local links and plain-text heading slugs, explicit anchors, and math delimiters; not a hosted-rendering or semantic proof test.",
    }


if __name__ == "__main__":
    try:
        report = run_checks()
    except Exception as error:
        report = {
            "status": "failed",
            "passed": False,
            "error_type": type(error).__name__,
            "error": str(error),
        }
    print(json.dumps(report, indent=2, sort_keys=True))
    sys.exit(0 if report["passed"] else 1)
