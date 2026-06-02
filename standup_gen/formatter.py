from collections import defaultdict

from .git_reader import Commit, categorize

CATEGORY_ORDER = ["Features", "Fixes", "Refactors", "Docs", "Tests", "Chores", "Other"]

SLACK_EMOJI = {
    "Features": ":sparkles:",
    "Fixes": ":bug:",
    "Docs": ":book:",
    "Refactors": ":recycle:",
    "Tests": ":white_check_mark:",
    "Chores": ":wrench:",
    "Other": ":small_blue_diamond:",
}


def _clean_subject(subject: str) -> str:
    for prefix in ("feat:", "fix:", "docs:", "refactor:", "test:", "chore:", "ci:", "build:"):
        if subject.lower().startswith(prefix):
            return subject[len(prefix):].strip()
    return subject


def _label(commit: Commit, show_repo: bool) -> str:
    prefix = f"[{commit.repo}] " if show_repo else ""
    return prefix + _clean_subject(commit.subject)


def format_standup(commits: list[Commit], fmt: str = "plain", show_repo: bool = True) -> str:
    if not commits:
        return "No commits found for the specified period."

    grouped: dict[str, list[Commit]] = defaultdict(list)
    for c in commits:
        grouped[categorize(c.subject)].append(c)

    if fmt == "slack":
        return _slack(grouped, show_repo)
    if fmt == "md":
        return _markdown(grouped, show_repo)
    return _plain(grouped, show_repo)


def _plain(grouped: dict, show_repo: bool) -> str:
    lines = ["Yesterday I worked on:"]
    for cat in CATEGORY_ORDER:
        if cat not in grouped:
            continue
        lines.append(f"\n{cat}:")
        for c in grouped[cat]:
            lines.append(f"  - {_label(c, show_repo)}")
    return "\n".join(lines)


def _markdown(grouped: dict, show_repo: bool) -> str:
    lines = ["## Standup\n"]
    for cat in CATEGORY_ORDER:
        if cat not in grouped:
            continue
        lines.append(f"### {cat}")
        for c in grouped[cat]:
            lines.append(f"- {_label(c, show_repo)}")
        lines.append("")
    return "\n".join(lines)


def _slack(grouped: dict, show_repo: bool) -> str:
    lines = [":calendar: *Standup*"]
    for cat in CATEGORY_ORDER:
        if cat not in grouped:
            continue
        lines.append(f"\n{SLACK_EMOJI.get(cat, ':small_blue_diamond:')} *{cat}*")
        for c in grouped[cat]:
            lines.append(f"  • {_label(c, show_repo)}")
    return "\n".join(lines)
