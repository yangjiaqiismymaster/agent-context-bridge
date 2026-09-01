import argparse
from pathlib import Path

from agent_context.context_builder import build_context_pack
from agent_context.context_builder import (
    build_context_pack,
    load_context
)

from agent_context.git_reader import (
    collect_git_context
)

def command_pack(args):
    """
    生成 Agent Context Pack。
    """

    project_dir = Path.cwd()

    context_file = (
        project_dir
        / "context"
        / "context.json"
    )

    output_dir = (
        project_dir
        / ".agent-context"
    )

    build_context_pack(
        project_dir=project_dir,
        context_file=context_file,
        output_dir=output_dir
    )

    

def create_parser():
    """
    创建 CLI 命令解析器。
    """

    parser = argparse.ArgumentParser(
        prog="agent-context",
        description="Universal context bridge for AI coding agents."
    )

    # 创建子命令系统
    subparsers = parser.add_subparsers(
        dest="command",
        required=True
    )

    # ------------------------------------------------
    # pack
    # ------------------------------------------------

    pack_parser = subparsers.add_parser(
        "pack",
        help="Build an Agent Context Pack."
    )

    pack_parser.set_defaults(
        func=command_pack
    )

    show_parser = subparsers.add_parser(
            "show",
            help="Show current Agent Context."
    )
    
    show_parser.set_defaults(
            func=command_show
        )

        # ------------------------------------------------
    # handoff
    # ------------------------------------------------

    handoff_parser = subparsers.add_parser(
        "handoff",
        help="Prepare context for another AI agent."
    )

    handoff_parser.add_argument(
        "agent",
        choices=[
            "claude",
            "codex"
        ],
        help="Target AI agent."
    )

    handoff_parser.set_defaults(
        func=command_handoff
    )
    
    return parser

def command_show(args):
    """
    显示当前 Agent Context。
    """

    project_dir = Path.cwd()

    context_file = (
        project_dir
        / "context"
        / "context.json"
    )

    context = load_context(
        context_file
    )

    git_context = collect_git_context(
        project_dir
    )

    print()
    print("=" * 60)
    print("Agent Context Summary")
    print("=" * 60)

    print()
    print("项目：")
    print(
        context["project"]["name"]
    )

    print()
    print("当前分支：")
    print(
        git_context["branch"]
    )

    print()
    print("当前任务：")
    print(
        context["task"]["title"]
    )

    print()
    print("当前工作：")
    print(
        context["progress"]["current"]
    )

    print()
    print("下一步：")

    next_steps = context.get(
        "next_steps",
        []
    )

    if next_steps:

        for step in next_steps:
            print("-", step)

    else:
        print("- 暂无")

    print()
    print("Git 状态：")

    if git_context["status"]:
        print(
            git_context["status"]
        )

    else:
        print(
            "当前工作区干净。"
        )

def command_handoff(args):
    """
    为指定 Agent 准备交接上下文。
    """

    project_dir = Path.cwd()

    context_file = (
        project_dir
        / "context"
        / "context.json"
    )

    output_dir = (
        project_dir
        / ".agent-context"
    )

    print()
    print("=" * 60)
    print("Preparing Agent Handoff")
    print("=" * 60)

    print()
    print("目标 Agent：")
    print(args.agent)

    # 每次交接之前，
    # 都重新生成最新 Context Pack
    build_context_pack(
        project_dir=project_dir,
        context_file=context_file,
        output_dir=output_dir
    )

    print()

    if args.agent == "claude":

        print("Claude 上下文准备完成。")

        print()
        print("首先读取：")

        print(
            output_dir / "CLAUDE.md"
        )

        print(
            output_dir / "HANDOFF.md"
        )

    elif args.agent == "codex":

        print("Codex 上下文准备完成。")

        print()
        print("首先读取：")

        print(
            output_dir / "AGENTS.md"
        )

        print(
            output_dir / "HANDOFF.md"
        )

def main():
    """
    CLI 主入口。
    """

    parser = create_parser()

    args = parser.parse_args()

    args.func(args)