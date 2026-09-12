# Signal Desk Agent Guidelines

This repository is a DevOps learning project for understanding how a change moves from source code to a running, observable, and recoverable service.

This file is the project-level source of truth for any automated agent, regardless of model or vendor. Use the project context here before offering generic engineering advice.

## System overview

The main request path is:

```text
Browser -> Angular client -> HTTP/REST -> FastAPI message service -> PostgreSQL
```

Responsibilities:
- Angular app: user interface and transient client-side state
- FastAPI service: API contract, business logic, and database access
- PostgreSQL: durable data storage

The browser should not talk directly to PostgreSQL. The application boundary exists to keep the database private, enforce validation, and make the service layer observable and debuggable.

## Project context

Relevant repository files:
- [ARCHITECTURE.md](../ARCHITECTURE.md): architecture summary for the project
- [docs/devops-study-guide.md](../docs/devops-study-guide.md): source of truth for milestone checkpoints
- [.github/skills/evaluate-milestone/SKILL.md](skills/evaluate-milestone/SKILL.md): optional rubric for milestone evaluation
- [.github/instructions/ARCHITECTURE.md.instructions.md](instructions/ARCHITECTURE.md.instructions.md): instructions that trigger when architecture docs are edited

## Milestone-driven evaluation

Use the DevOps study guide as the standard, not generic software advice.

Milestones:
1. Milestone 0: establish the mental model and ownership boundaries
2. Milestone 1: Linux, networking, and troubleshooting
3. Milestone 2: HTTP and REST contract
4. Milestone 3: database and service boundaries

When evaluating work, check whether it satisfies the current milestone's checkpoints and keep scope aligned to that milestone.

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

## Working rules for agents

- Keep edits grounded in the current milestone; do not add scope beyond it.
- Prefer evidence-based feedback over generic advice.
- Refer to the repository architecture and service boundaries before proposing a new pattern.
- If the current model supports the optional rubric files in [.github/skills](skills), use them as guidance; otherwise follow the rules in this file.
- Do not suggest container, Kubernetes, monitoring, or authentication patterns unless the milestone explicitly requires them.

## Output expectations

When asked to review architecture or implementation, produce a milestone-aligned assessment with:
- what is correct
- what is missing
- the next concrete step to satisfy the checkpoint

Keep the answer focused on Signal Desk's study-guide requirements rather than broad engineering best practices.
