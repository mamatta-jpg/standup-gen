import pytest

from standup_gen.git_reader import Commit, categorize
from standup_gen.formatter import format_standup


def commit(subject: str, repo: str = "myrepo") -> Commit:
    return Commit(hash="abc1234", subject=subject, author="Mansour", date="2026-06-02", repo=repo)


# --- categorize() ---

@pytest.mark.parametrize("subject,expected", [
    ("feat: add login button", "Features"),
    ("feature: dark mode", "Features"),
    ("add new endpoint", "Features"),
    ("fix: null pointer on startup", "Fixes"),
    ("bug: crash on iOS", "Fixes"),
    ("fixed broken redirect", "Fixes"),
    ("docs: update README", "Docs"),
    ("refactor: extract auth middleware", "Refactors"),
    ("test: add unit tests for parser", "Tests"),
    ("chore: bump dependencies", "Chores"),
    ("ci: fix flaky workflow", "Chores"),
    ("bump anthropic to 0.30", "Chores"),
    ("random change with no prefix", "Other"),
    ("wip: half done thing", "Other"),
])
def test_categorize(subject, expected):
    assert categorize(subject) == expected


# --- format_standup() ---

def test_empty_commits_returns_message():
    result = format_standup([])
    assert "No commits" in result


def test_plain_contains_category_headers():
    commits = [commit("feat: add search"), commit("fix: broken import")]
    result = format_standup(commits, fmt="plain")
    assert "Features" in result
    assert "Fixes" in result


def test_plain_strips_conventional_prefix():
    result = format_standup([commit("feat: add dark mode")], fmt="plain", show_repo=False)
    assert "add dark mode" in result
    assert "feat:" not in result


def test_plain_shows_repo_prefix_by_default():
    result = format_standup([commit("fix: crash", repo="api")], fmt="plain")
    assert "[api]" in result


def test_plain_hides_repo_when_disabled():
    result = format_standup([commit("fix: crash", repo="api")], fmt="plain", show_repo=False)
    assert "[api]" not in result


def test_markdown_starts_with_header():
    result = format_standup([commit("feat: x")], fmt="md")
    assert result.startswith("## Standup")


def test_markdown_uses_h3_categories():
    result = format_standup([commit("feat: add export")], fmt="md")
    assert "### Features" in result


def test_markdown_uses_bullet_points():
    result = format_standup([commit("fix: crash")], fmt="md")
    assert "- " in result


def test_slack_has_calendar_emoji():
    result = format_standup([commit("feat: add search")], fmt="slack")
    assert ":calendar:" in result


def test_slack_has_category_emoji():
    result = format_standup([commit("fix: crash")], fmt="slack")
    assert ":bug:" in result


def test_slack_feat_emoji():
    result = format_standup([commit("feat: new thing")], fmt="slack")
    assert ":sparkles:" in result


def test_only_present_categories_shown():
    result = format_standup([commit("feat: add thing")], fmt="plain")
    assert "Fixes" not in result
    assert "Features" in result


def test_multiple_repos():
    commits = [
        commit("feat: add api", repo="backend"),
        commit("feat: add ui", repo="frontend"),
    ]
    result = format_standup(commits, fmt="plain")
    assert "[backend]" in result
    assert "[frontend]" in result
