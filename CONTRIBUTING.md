# Contributing to standup-gen

Thanks for your interest in contributing!

## Getting started

```bash
git clone https://github.com/mamatta-jpg/standup-gen
cd standup-gen
pip install -e ".[dev]"
pytest tests/ -v
```

## Adding a new commit category

Categories and their detection logic live in `standup_gen/git_reader.py` inside `categorize()`. The function checks subject line prefixes in order — first match wins.

## Adding a new output format

Formatters live in `standup_gen/formatter.py`. Add a new `_format_<name>()` function and wire it into `format_standup()`.

## Running against your own repo

```bash
standup-gen --since "1 week ago"
```

## Pull requests

- Keep PRs focused — one feature or fix per PR
- All tests must pass: `pytest tests/ -v`
- Add tests for new categories or formatters

## Reporting a missing commit convention

Open an issue with examples of commit messages that aren't being categorized correctly.
