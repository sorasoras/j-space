#!/usr/bin/env python3
"""Check package structure and local documentation links, not workflow efficacy."""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MODULES = (
    "introspection", "directed-focus", "deep-reasoning", "broadcast", "capacity",
    "self-monitoring", "shorthand", "markers", "empirics",
)
REFERENCES = ("j-space-science", "induction-playbook", "exemplars")


def check(root):
    findings = []
    entry = root / "SKILL.md"
    if not entry.is_file():
        return ["SKILL.md is missing"]
    text = entry.read_text(encoding="utf-8-sig")
    frontmatter = re.match(r"\A---\n(.*?)\n---(?:\n|$)", text, re.S)
    if not frontmatter:
        findings.append("SKILL.md needs YAML frontmatter")
    else:
        fields = {}
        for line in frontmatter.group(1).splitlines():
            key, sep, value = line.partition(":")
            if not sep or key in fields:
                findings.append("Invalid or duplicate frontmatter field: " + line)
            fields[key] = value.strip().strip('\"').strip("'")
        if fields.get("name") != "j-space":
            findings.append("The installed skill name must remain j-space")
        if not fields.get("description"):
            findings.append("The trigger description is missing")
        if set(fields) - {"name", "description"}:
            findings.append("Unexpected frontmatter fields")
    if len(text.splitlines()) > 150:
        findings.append("Keep the entry under 150 lines; move optional detail into modules")
    for directory, names in (("modules", MODULES), ("references", REFERENCES)):
        for name in names:
            relative = f"{directory}/{name}.md"
            path = root / relative
            if not path.is_file():
                findings.append(relative + " is missing")
            elif relative not in text:
                findings.append(relative + " is not routed from the entry")
    for path in sorted(root.rglob("*.md")):
        if ".jspace" in path.parts:
            continue
        body = path.read_text(encoding="utf-8-sig")
        relative = str(path.relative_to(root))
        if path != entry and body.startswith("---\n"):
            findings.append(relative + " unexpectedly contains skill frontmatter")
        if not body.strip():
            findings.append(relative + " is empty")
        if body.count("```") % 2:
            findings.append(relative + " has an unclosed code fence")
        for target in re.findall(r"\[[^\]]*\]\(([^\s)]+)\)", body):
            if "://" in target or target.startswith("#"):
                continue
            local = target.split("#", 1)[0]
            if local and not (path.parent / local).exists():
                findings.append(relative + ": missing local link " + local)
        for target in re.findall(r"`((?:modules|references|scripts)/[\w./-]+\.(?:md|py))`", body):
            if not (root / target).is_file():
                findings.append(relative + ": missing package resource " + target)
    for name in ("jspace.py", "test_jspace.py"):
        if not (root / "scripts" / name).is_file():
            findings.append("scripts/" + name + " is missing")
    return findings


def main():
    findings = check(ROOT)
    for finding in findings:
        print("FAIL: " + finding)
    if findings:
        return 1
    print("verify_suite: PASS (package structure and local links only)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

