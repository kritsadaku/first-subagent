# Agent Studio

Minimal FastAPI project.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/` for the welcome response.

## Test

```bash
pytest
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
- Add requirements.txt or pyproject.toml.
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
- Implementer: only edit app/, tests/, README.md, requirements.txt, and .gitignore.
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
- Include explicit verification steps, such as `pytest` or a health-check request.
- If a task is simple, subagents may be unnecessary; they are most useful when inspection, planning, implementation, and review can be separated cleanly.
