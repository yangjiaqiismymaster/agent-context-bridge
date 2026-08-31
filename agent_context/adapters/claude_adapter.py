def generate_claude_md(context, git_context):
    """
    根据通用 Context，
    生成专门给 Claude Code 阅读的 CLAUDE.md。
    """

    project = context["project"]
    task = context["task"]
    progress = context["progress"]

    # 获取当前正在进行的工作
    current_work = progress.get(
        "current",
        "暂无"
    )

    # 获取下一步任务
    next_steps = context.get(
        "next_steps",
        []
    )

    # 把 Python 列表转换成 Markdown 列表
    next_steps_text = "\n".join(
        f"- {step}"
        for step in next_steps
    )

    # 如果 next_steps 是空列表
    if not next_steps_text:
        next_steps_text = "- 暂无"

    # 生成 CLAUDE.md 内容
    content = f"""# Claude Code Project Instructions

You are continuing work from another AI coding agent.

## Project

Project name: {project["name"]}

Current branch: {git_context["branch"]}

Current commit: {git_context["current_commit"]}

## Current Task

{task["title"]}

{task["description"]}

## Current Work

{current_work}

## Recommended Next Steps

{next_steps_text}

## Required Context Reading

Before modifying code, read:

1. `HANDOFF.md`
2. `TASK.md`
3. `PROGRESS.md`
4. `DECISIONS.md`
5. `git-status.txt`
6. `git-diff.patch`
7. `git-staged-diff.patch`

## Working Rules

- Continue from the current repository state.
- Do not redo completed work unnecessarily.
- Treat Git state as factual evidence.
- Preserve existing decisions unless there is evidence they are wrong.
- Inspect existing modifications before editing the same files.
- Keep changes focused on the current task.
"""

    return content