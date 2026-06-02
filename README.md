# standup-gen

> Auto-generate your daily standup from git history. Never stare at a blank "what did I do yesterday?" again.

[![CI](https://github.com/mamatta-jpg/standup-gen/actions/workflows/ci.yml/badge.svg)](https://github.com/mamatta-jpg/standup-gen/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/standup-gen)](https://pypi.org/project/standup-gen/)
[![Python](https://img.shields.io/pypi/pyversions/standup-gen)](https://pypi.org/project/standup-gen/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Install

```bash
pip install standup-gen
```

## Usage

```bash
# Generate standup for yesterday (default)
standup-gen

# Last week
standup-gen --since "1 week ago"

# Specific date
standup-gen --since 2026-05-28

# Multiple repos
standup-gen -r ~/projects/api -r ~/projects/frontend

# Slack format
standup-gen --format slack

# Markdown (for Notion, Obsidian, etc.)
standup-gen --format md > standup.md

# Filter by author
standup-gen --author "Mansour"
```

## Example output

```
Yesterday I worked on:

Features:
  - Add OAuth2 token refresh flow
  - Add dark mode toggle to settings

Fixes:
  - Fix race condition in session handler
  - Fix mobile layout on iOS 17

Chores:
  - Bump anthropic SDK to 0.30
```

## Slack output

```
:calendar: *Standup*

:sparkles: *Features*
  • Add OAuth2 token refresh flow

:bug: *Fixes*
  • Fix race condition in session handler
```

## How it works

Reads `git log` for the time range, categorizes each commit by its prefix (`feat:`, `fix:`, `chore:`, etc.), strips the prefix for clean output, and groups everything by category. Works with any git repo — no config required.

## From the same author

- [env-leak](https://github.com/mamatta-jpg/env-leak) — scan your codebase for leaked API keys and secrets
- [git-sage](https://github.com/mamatta-jpg/git-sage) — AI commit message generator for Claude and OpenAI

## License

MIT
