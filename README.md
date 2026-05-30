# Agent Studio

Minimal FastAPI project.

## Setup

Install `uv` if it is not already available:

```bash
brew install uv
```

Create and sync the project environment:

```bash
uv sync
```

## Run

```bash
uv run uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/` for the welcome response.

## Test

```bash
uv run pytest
```

## Dependency Management

This project uses `uv` with [pyproject.toml](pyproject.toml).

Add a runtime dependency:

```bash
uv add package-name
```

Add a test or development dependency:

```bash
uv add --dev package-name
```

Refresh the local environment after dependency changes:

```bash
uv sync
```

## Using Subagents With Codex

You can ask Codex to split project work across subagents. A good pattern is to use separate agents for discovery, planning, implementation, and review while the main agent coordinates the result.

Example prompt:

```text
Create a new simple Python FastAPI project from scratch in this empty directory.

Use subagents:
1. Spawn explorer to inspect the current directory and confirm it is safe to initialize.
2. Spawn planner to design the smallest clean FastAPI project structure.
3. Spawn implementer to create the files.
4. Spawn reviewer to check correctness, README, and runnable commands.

Requirements:
- Do not compare with main branch.
- Do not assume any existing Git branch.
- Create a basic API with:
  - GET / returning a welcome message
  - GET /health returning {"status": "ok"}
- Add pyproject.toml for uv.
- Add README.md with setup and run instructions.
- Add a basic test if appropriate.
- Run tests if possible.
- Summarize files created and how to run the server.
```

How it works:

- The explorer checks the workspace first and reports whether it is safe to edit.
- The planner proposes the smallest clean structure before files are created.
- The implementer owns the file changes and should be given an exact write scope.
- The reviewer checks the result for bugs, missing instructions, and runnable commands.
- The main Codex agent integrates the work, runs verification, and summarizes the final result.

### Adding Subagent Instructions

Add role-specific instructions directly in your prompt when you want tighter control:

```text
Subagent instructions:
- Explorer: inspect only; do not edit files.
- Planner: prefer the simplest structure that satisfies the requirements.
- Implementer: only edit app/, tests/, README.md, pyproject.toml, uv.lock, and .gitignore.
- Reviewer: report findings first with file and line references.
```

You can also add constraints that apply to every subagent:

```text
Global constraints:
- Do not compare with main branch.
- Do not assume a Git branch exists.
- Do not overwrite hidden tool or editor configuration.
- Run tests if dependencies are available.
```

Tips:

- Keep each subagent task small and specific.
- Give implementers clear file ownership to avoid conflicting edits.
- Ask reviewers to focus on correctness, missing tests, and unclear commands.
- Include explicit verification steps, such as `uv run pytest` or a health-check request.
- For uv projects, ask implementers to use `uv add` for dependency changes and `uv run` for commands.
- If a task is simple, subagents may be unnecessary; they are most useful when inspection, planning, implementation, and review can be separated cleanly.
