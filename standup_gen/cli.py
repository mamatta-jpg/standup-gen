import click

from .formatter import format_standup
from .git_reader import get_commits


@click.command()
@click.option("--since", default="yesterday", show_default=True,
              help='Time range: "yesterday", "1 week ago", "2026-05-01"')
@click.option("--repos", "-r", multiple=True, default=["."],
              help="Repo paths to include (default: current directory)")
@click.option("--author", "-a", default=None,
              help="Filter by author name or email substring")
@click.option("--format", "fmt",
              type=click.Choice(["plain", "md", "slack"]), default="plain", show_default=True,
              help="Output format")
@click.option("--no-repo", is_flag=True, help="Hide [repo] prefix on each entry")
def main(since, repos, author, fmt, no_repo):
    """Generate a standup report from your git history.

    \b
    Examples:
      standup-gen
      standup-gen --since "1 week ago" --format slack
      standup-gen -r ~/project1 -r ~/project2
      standup-gen --format md > standup.md
    """
    all_commits = []
    for repo in repos:
        all_commits.extend(get_commits(repo, since=since, author=author))

    all_commits.sort(key=lambda c: c.date, reverse=True)
    click.echo(format_standup(all_commits, fmt=fmt, show_repo=not no_repo))
