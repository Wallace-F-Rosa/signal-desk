# Signal Desk

Signal Desk is a learning project for studying DevOps through a small communication platform.

The planned system contains:

- Angular frontend (`signal-interface`)
- FastAPI backend (`message-service`)
- PostgreSQL database
- Docker for packaging and local environments
- Kubernetes for orchestration
- GitHub Actions for CI/CD

This repository currently contains the study material. The application can be built incrementally as each milestone is completed.

## Study guide

Read [the DevOps study guide](docs/devops-study-guide.md) for the learning path, minimal examples, exercises, and checkpoints.

## Current scope

The first communication path is a synchronous REST request:

```text
Browser -> Angular -> HTTP/REST -> FastAPI -> PostgreSQL
```

Later milestones can add asynchronous messaging and streaming after the REST path is understood.
