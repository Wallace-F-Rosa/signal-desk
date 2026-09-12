---
name: ARCHITECTURE.md
description: "Evaluate Signal Desk architecture against DevOps study guide. Triggered when ARCHITECTURE.md is opened or edited."
applyTo: "**/ARCHITECTURE.md"
---

# Architecture File Instructions

When evaluating ARCHITECTURE.md, apply the `evaluate-milestone` skill.

## Quick checks (before saving):

1. **Three components named?** Signal Desk (frontend), Message Service (backend), PostgreSQL (data)
2. **Responsibilities clear?** Each section explains what the component does
3. **Security boundary explained?** Why doesn't the browser connect to PostgreSQL?
4. **Milestone appropriate?** Does the scope match your current study milestone?

## How to get feedback

Ask the Copilot chat:
- *"Evaluate my architecture against Milestone 0"*
- *"Check if my ARCHITECTURE.md matches the study guide"*
- *"Show me what's missing for Milestone X"*

The agent will apply the `evaluate-milestone` skill and give you a structured pass/fail assessment.
