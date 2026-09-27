# Second Brain

Decision support for a CodePath AI Practice Lead. It reads fellows' work, starting with GitHub pull requests, prepares review notes with Claude, and will keep follow-ups, weekly patterns, and escalation drafts current in Notion. It never posts, messages, or escalates on the lead's behalf: it drafts, and the lead decides and sends.

Status: early build. Review prep works on demand; everything else is on the [roadmap](docs/ROADMAP.md).

## Setup

Requires [uv](https://docs.astral.sh/uv/).

```bash
uv sync
cp .env.example .env
```

Fill in `.env` with a Claude API key and a read-only GitHub token. `.env` is never committed.

## Use

```bash
uv run second-brain review https://github.com/owner/repo/pull/123 --first-artifact
```

## Develop

```bash
uv run pytest
uv run ruff check
uv run ruff format --check
uv run mypy src tests
```

## Docs

The running record lives in [docs/](docs/): [DOMAIN](docs/DOMAIN.md) for the project's language, [SYSTEM](docs/SYSTEM.md) for how it works, [DECISIONS](docs/DECISIONS.md) for why, [ROADMAP](docs/ROADMAP.md) for what's next, and [CHANGELOG](docs/CHANGELOG.md) for what shipped.
