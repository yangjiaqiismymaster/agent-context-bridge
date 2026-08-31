import json
from pathlib import Path

from agent_context.git_reader import collect_git_context
from agent_context.adapters.claude_adapter import generate_claude_md
from agent_context.adapters.codex_adapter import generate_agents_md

def load_context(context_file):
    """
    从 context.json 读取人工维护的任务上下文。
    """

    if not context_file.exists():
        raise FileNotFoundError(
            "找不到上下文文件："
            + str(context_file)
        )

    with open(
        context_file,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def save_text_file(output_dir, filename, content):
    """
    将字符串保存成文本文件。
    """

    file_path = output_dir / filename

    with open(
        file_path,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(content)

    print("已生成：", file_path)


def format_markdown_list(items, empty_text="暂无"):
    """
    把 Python 列表转换成 Markdown 列表。

    例如：

    [
        "完成登录",
        "完成测试"
    ]

    转换成：

    - 完成登录
    - 完成测试
    """

    if not items:
        return "- " + empty_text

    lines = []

    for item in items:
        lines.append("- " + str(item))

    return "\n".join(lines)


def generate_task_markdown(context):
    """
    生成 TASK.md。
    """

    task = context["task"]

    content = f"""# Current Task

## Title

{task["title"]}

## Description

{task["description"]}
"""

    return content


def generate_progress_markdown(context):
    """
    生成 PROGRESS.md。
    """

    progress = context["progress"]

    completed = format_markdown_list(
        progress.get("completed", [])
    )

    problems = format_markdown_list(
        progress.get("problems", [])
    )

    current = progress.get(
        "current",
        "暂无"
    )

    content = f"""# Progress

## Completed

{completed}

## Current Work

{current}

## Known Problems

{problems}
"""

    return content


def generate_decisions_markdown(context):
    """
    生成 DECISIONS.md。
    """

    decisions = format_markdown_list(
        context.get("decisions", [])
    )

    content = f"""# Decisions

这些是当前任务过程中已经做出的重要技术决策。

{decisions}
"""

    return content


def generate_handoff_markdown(
    context,
    git_context
):
    """
    生成最关键的 HANDOFF.md。

    这个文件是给下一个 Agent
    首先阅读的交接说明。
    """

    project = context["project"]
    task = context["task"]
    progress = context["progress"]

    completed = format_markdown_list(
        progress.get("completed", [])
    )

    problems = format_markdown_list(
        progress.get("problems", [])
    )

    decisions = format_markdown_list(
        context.get("decisions", [])
    )

    next_steps = format_markdown_list(
        context.get("next_steps", [])
    )

    content = f"""# Agent Handoff

This file describes the current project state for the next AI agent.

---

## Project

Project name:

{project["name"]}

Current branch:

{git_context["branch"]}

Current commit:

{git_context["current_commit"]}

---

## Current Task

### Title

{task["title"]}

### Description

{task["description"]}

---

## Completed Work

{completed}

---

## Current Work

{progress.get("current", "暂无")}

---

## Known Problems

{problems}

---

## Important Decisions

{decisions}

---

## Recommended Next Steps

{next_steps}

---

## Git Evidence

Before modifying the project, inspect:

- `git-status.txt`
- `git-diff.patch`
- `git-staged-diff.patch`
- `git-log.txt`

These files contain the actual Git state and should be treated as factual evidence.

---

## Instructions For The Next Agent

1. Read this HANDOFF.md first.
2. Read TASK.md and PROGRESS.md.
3. Inspect the Git diff before modifying code.
4. Preserve existing work unless there is evidence that it is incorrect.
5. Do not redo completed work unnecessarily.
6. Continue from the recommended next steps.
"""

    return content


def build_context_pack(
    project_dir,
    context_file,
    output_dir
):
    """
    构建完整 Agent Context Pack。
    """

    print()
    print("=" * 60)
    print("Building Agent Context Pack")
    print("=" * 60)

    # --------------------------------------------------
    # 1. 创建输出目录
    # --------------------------------------------------

    output_dir.mkdir(
        exist_ok=True
    )

    # --------------------------------------------------
    # 2. 读取人工上下文
    # --------------------------------------------------

    print()
    print("正在读取人工上下文...")

    context = load_context(
        context_file
    )

    # --------------------------------------------------
    # 3. 自动读取 Git
    # --------------------------------------------------

    print("正在读取 Git 状态...")

    git_context = collect_git_context(
        project_dir
    )

    # --------------------------------------------------
    # 4. 更新 context.json 中的 Git 信息
    # --------------------------------------------------

    context["project"]["branch"] = (
        git_context["branch"]
    )

    context["git"] = {
        "branch": git_context["branch"],
        "current_commit": git_context["current_commit"]
    }

    # --------------------------------------------------
    # 5. 保存机器可读 context.json
    # --------------------------------------------------

    output_context = (
        output_dir / "context.json"
    )

    with open(
        output_context,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            context,
            file,
            ensure_ascii=False,
            indent=2
        )

    print(
        "已生成：",
        output_context
    )

    # --------------------------------------------------
    # 6. 保存 Git 原始证据
    # --------------------------------------------------

    save_text_file(
        output_dir,
        "git-status.txt",
        git_context["status"]
        or "当前没有未提交修改。"
    )

    save_text_file(
        output_dir,
        "git-diff.patch",
        git_context["diff"]
        or "当前没有未暂存修改。"
    )

    save_text_file(
        output_dir,
        "git-staged-diff.patch",
        git_context["staged_diff"]
        or "当前没有已暂存修改。"
    )

    save_text_file(
        output_dir,
        "git-log.txt",
        git_context["log"]
    )

    # --------------------------------------------------
    # 7. 生成给人和 Agent 阅读的 Markdown
    # --------------------------------------------------

    save_text_file(
        output_dir,
        "TASK.md",
        generate_task_markdown(
            context
        )
    )

    save_text_file(
        output_dir,
        "PROGRESS.md",
        generate_progress_markdown(
            context
        )
    )

    save_text_file(
        output_dir,
        "DECISIONS.md",
        generate_decisions_markdown(
            context
        )
    )

    save_text_file(
        output_dir,
        "HANDOFF.md",
        generate_handoff_markdown(
            context,
            git_context
        )
    )
        # --------------------------------------------------
    # 8. 生成不同 Agent 的专属上下文
    # --------------------------------------------------

    save_text_file(
        output_dir,
        "CLAUDE.md",
        generate_claude_md(
            context,
            git_context
        )
    )

    save_text_file(
        output_dir,
        "AGENTS.md",
        generate_agents_md(
            context,
            git_context
        )
    )
    
    print()
    print("=" * 60)
    print("Agent Context Pack 构建完成")
    print("=" * 60)