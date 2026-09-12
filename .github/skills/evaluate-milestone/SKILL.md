---
name: evaluate-milestone
description: "Evaluate architecture and implementation files against Signal Desk DevOps study guide milestones. Use when: checking if you're on track with Milestone 0, 1, 2, or 3; validating ARCHITECTURE.md completeness; ensuring implementation matches study guide checkpoints."
---

# Evaluate Architecture Against Study Guide

This skill evaluates your Signal Desk work against the DevOps study guide checkpoints.

## Usage

Use `/evaluate-milestone [milestone]` where milestone is:
- `0` — Mental model & architecture description
- `1` — Linux, networking, troubleshooting
- `2` — HTTP and REST contract
- `3` — Database and service boundaries
- `auto-detect` — Determine current milestone from ARCHITECTURE.md

## Evaluation Criteria by Milestone

### Milestone 0: Establish Mental Model
**Checkpoint questions:**
1. Can you name the owner of each responsibility?
2. Can you explain why the browser should not connect directly to PostgreSQL?

**Evaluation rubric:**
- ✅ Three components clearly identified (frontend, API service, database)
- ✅ Each component's responsibilities documented
- ✅ Clear explanation of security boundary (why no direct DB access)
- ✅ First REST use case implicit or explicit (submit → persist → retrieve)
- ✅ Data flow marked as transient (UI) vs persistent (DB)

**Pass condition:** All 5 items checked. If not, list which gaps to address.

### Milestone 1: Linux, Networking, Troubleshooting
**Checkpoint questions:**
1. For each symptom (connection refused, timeout, 404, 500), what evidence would you collect?

**Evaluation rubric:**
- ✅ Local API runnable and inspectable (`ps aux`, `curl`, `ss -ltn`)
- ✅ Implementation includes health endpoint (`GET /health`)
- ✅ Docker setup for consistent local environment (if applicable)
- ✅ Documentation on how to diagnose network/process issues

### Milestone 2: HTTP and REST Contract
**Checkpoint questions:**
1. Explain why `/health` and `/ready` should return different results when PostgreSQL is down.

**Evaluation rubric:**
- ✅ `GET /health` endpoint (process health)
- ✅ `GET /ready` endpoint (dependency readiness)
- ✅ `POST /messages` endpoint (create message)
- ✅ `GET /messages` endpoint (list messages)
- ✅ Consistent error responses with status codes
- ✅ Clear API contract documentation

### Milestone 3: Database and Service Boundaries
**Checkpoint questions:**
1. Describe what happens if the API dies before a transaction commits.
2. How would you back up and restore the data?

**Evaluation rubric:**
- ✅ `messages` table schema designed (id, text, created_at, status fields)
- ✅ Indexes identified for queries
- ✅ Migration strategy documented (version control for schema)
- ✅ Transaction boundaries clear in code
- ✅ Backup/restore strategy documented

## How to Use This Skill

1. When you update `ARCHITECTURE.md`, ask: *"Evaluate my architecture against Milestone 0"*
2. When you have implementation, ask: *"Evaluate my implementation against Milestone 2"*
3. Include implementation files (code, database schema, endpoints) in the context
4. Review the pass/fail result and address gaps before moving to the next milestone

## Output Format

The evaluator will return:

```
## Milestone X Evaluation: [PASS | NEEDS WORK]

**Met (✅):**
- [item]
- [item]

**Gaps (⚠️):**
- [item]
- [item]

**Next steps:**
1. [specific action]
2. [specific action]
```
