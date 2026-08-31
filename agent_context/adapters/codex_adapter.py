def generate_agents_md(context, git_context):
    """
    根据通用 Context，
    生成专门给 Codex 阅读的 AGENTS.md。
    """

    project = context["project"]
    task = context["task"]
    progress = context["progress"]

    current_work = progress.get(
        "current",
        "暂无"
    )

    next_steps = context.get(
        "next_steps",
        []
    )

    next_steps_text = "\n".join(
        f"- {step}"
        for step in next_steps
    )

    if not next_steps_text:
        next_steps_text = "- 暂无"

    content = f"""# AGENTS.md

## Project Context

Project: {project["name"]}

Branch: {git_context["branch"]}

Current commit: {git_context["current_commit"]}

## Current Task

{task["title"]}

{task["description"]}

## Current Work

{current_work}

## Recommended Next Steps

{next_steps_text}

## Context Files

Before making changes, inspect:

- `HANDOFF.md`
- `TASK.md`
- `PROGRESS.md`
- `DECISIONS.md`
- `git-status.txt`
- `git-diff.patch`
- `git-staged-diff.patch`

## Instructions

- Continue from the current worktree state.
- Inspect existing changes before editing.
- Do not discard another agent's work without evidence.
- Use Git state as the source of truth for code changes.
- Avoid reimplementing completed tasks.
- Keep changes scoped to the current task.
"""

    return content