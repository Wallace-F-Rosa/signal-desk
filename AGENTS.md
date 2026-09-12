# Signal Desk Agent Guidelines

This file is the repository's canonical agent context. It is intentionally model-agnostic and applies whether the agent is local, cloud-hosted, or running via an IDE integration.

## System overview

```text
Browser -> Angular client -> HTTP/REST -> FastAPI message service -> PostgreSQL
```

Responsibilities:
- Angular app: user interface and transient client-side state
- FastAPI service: API contract, business logic, and database access
- PostgreSQL: persistent storage

## Required testing policy

Any code change, fix, refactor, or feature added to this repository must include a corresponding automated test unless the change is purely documentation-only.

This applies to both:
- unit tests for isolated logic and configuration
- integration tests for API or database behavior

Rules:
1. Do not merge or accept a code change without a relevant test.
2. If a bug is fixed, add or update a regression test that would fail without the fix.
3. If a new behavior is introduced, add a test covering that behavior.
4. Prefer the smallest real test that checks the behavior.
5. If a change affects database or environment configuration, validate the env-driven behavior explicitly.

Validation examples:
```bash
cd messages
source .venv/bin/activate
PYTHONPATH=src pytest tests -q
```

or:
```bash
cd messages
source .venv/bin/activate
PYTHONPATH=src uv run pytest tests -q
```

## Working rules

- Use the DevOps study guide in [docs/devops-study-guide.md](docs/devops-study-guide.md) as the source of truth for milestone goals.
- Keep work grounded in the current milestone; do not add scope beyond it.
- Prefer evidence-based answers over generic engineering advice.
- If the current agent supports the optional files in [.github/skills](.github/skills) and [.github/instructions](.github/instructions), use them as guidance; otherwise follow this file.
- Do not suggest patterns beyond the milestone scope unless the user explicitly asks for them.

## Canonical source of truth

The authoritative project instructions live in [.github/AGENTS.md](.github/AGENTS.md). This root file exists as a convenience for agents that read repo-root AGENTS files.
