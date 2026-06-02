import subprocess
from pathlib import Path
from typing import NamedTuple


class Commit(NamedTuple):
    hash: str
    subject: str
    author: str
    date: str
    repo: str


def get_commits(repo_path: str = ".", since: str = "yesterday", author: str | None = None) -> list[Commit]:
    cmd = [
        "git", "-C", repo_path, "log",
        f"--since={since}",
        "--format=%h\t%s\t%an\t%ai",
        "--no-merges",
    ]
    if author:
        cmd += [f"--author={author}"]

    result = subprocess.run(cmd, capture_output=True, text=True)
    repo_name = Path(repo_path).resolve().name
    commits = []

    for line in result.stdout.splitlines():
        parts = line.split("\t", 3)
        if len(parts) == 4:
            hash_, subject, author_name, date = parts
            commits.append(Commit(
                hash=hash_,
                subject=subject.strip(),
                author=author_name.strip(),
                date=date[:10],
                repo=repo_name,
            ))
    return commits


def categorize(subject: str) -> str:
    lower = subject.lower()
    if any(lower.startswith(p) for p in ("feat:", "feature:", "add ", "added ")):
        return "Features"
    if any(lower.startswith(p) for p in ("fix:", "bug:", "fixed ", "hotfix:")):
        return "Fixes"
    if any(lower.startswith(p) for p in ("docs:", "doc:", "readme", "changelog")):
        return "Docs"
    if any(lower.startswith(p) for p in ("refactor:", "cleanup", "clean up")):
        return "Refactors"
    if any(lower.startswith(p) for p in ("test:", "tests:", "spec:")):
        return "Tests"
    if any(lower.startswith(p) for p in ("chore:", "ci:", "build:", "deps:", "bump ")):
        return "Chores"
    return "Other"
