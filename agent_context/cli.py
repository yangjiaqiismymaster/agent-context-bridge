import argparse
from pathlib import Path

from agent_context.context_builder import (
    build_context_pack,
    load_context,
)

from agent_context.git_reader import (
    collect_git_context,
)

from agent_context.initializer import (
    initialize_project,
)


# ============================================================
# 1. 统一解析项目路径
# ============================================================

def get_project_paths(project_path=None):
    """
    根据用户提供的 --project 参数，
    得到 Agent Context Bridge 工作需要的几个路径。

    如果用户没有提供 --project，
    就使用当前终端所在目录。

    返回：

    project_dir
    context_file
    output_dir
    """

    # --------------------------------------------------------
    # 确定目标项目
    # --------------------------------------------------------

    if project_path:

        project_dir = Path(
            project_path
        ).resolve()

    else:

        project_dir = Path.cwd()

    # --------------------------------------------------------
    # 人工上下文文件
    # --------------------------------------------------------

    context_file = (
        project_dir
        / "context"
        / "context.json"
    )

    # --------------------------------------------------------
    # 自动生成的 Context Pack
    # --------------------------------------------------------

    output_dir = (
        project_dir
        / ".agent-context"
    )

    return (
        project_dir,
        context_file,
        output_dir,
    )


# ============================================================
# 2. init 命令
# ============================================================

def command_init(args):
    """
    初始化一个 Git 项目。

    示例：

    python main.py init

    python main.py init --project D:\\MyProject
    """

    (
        project_dir,
        _,
        _,
    ) = get_project_paths(
        args.project
    )

    initialize_project(
        project_dir
    )


# ============================================================
# 3. pack 命令
# ============================================================

def command_pack(args):
    """
    生成完整 Agent Context Pack。
    """

    (
        project_dir,
        context_file,
        output_dir,
    ) = get_project_paths(
        args.project
    )

    print()
    print("目标项目：")
    print(project_dir)

    build_context_pack(
        project_dir=project_dir,
        context_file=context_file,
        output_dir=output_dir,
    )


# ============================================================
# 4. show 命令
# ============================================================

def command_show(args):
    """
    在终端显示当前项目的重要 Agent Context。
    """

    (
        project_dir,
        context_file,
        _,
    ) = get_project_paths(
        args.project
    )

    # 读取人工维护的上下文
    context = load_context(
        context_file
    )

    # 读取 Git 事实
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
    print("项目路径：")
    print(
        project_dir
    )

    print()
    print("当前分支：")
    print(
        git_context["branch"]
    )

    print()
    print("当前 Commit：")
    print(
        git_context["current_commit"]
    )

    print()
    print("当前任务：")
    print(
        context["task"]["title"]
    )

    print()
    print("任务说明：")
    print(
        context["task"]["description"]
    )

    print()
    print("当前工作：")
    print(
        context["progress"]["current"]
    )

    # --------------------------------------------------------
    # 已完成工作
    # --------------------------------------------------------

    print()
    print("已完成：")

    completed = context[
        "progress"
    ].get(
        "completed",
        []
    )

    if completed:

        for item in completed:
            print("-", item)

    else:

        print("- 暂无")

    # --------------------------------------------------------
    # 当前问题
    # --------------------------------------------------------

    print()
    print("当前问题：")

    problems = context[
        "progress"
    ].get(
        "problems",
        []
    )

    if problems:

        for problem in problems:
            print("-", problem)

    else:

        print("- 暂无")

    # --------------------------------------------------------
    # 下一步
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # Git 状态
    # --------------------------------------------------------

    print()
    print("Git 状态：")

    status = git_context["status"]

    if status:

        print(status)

    else:

        print(
            "当前工作区干净。"
        )


# ============================================================
# 5. handoff 命令
# ============================================================

def command_handoff(args):
    """
    为另一个 AI Agent 准备最新上下文。

    示例：

    python main.py handoff claude

    python main.py handoff codex
    """

    (
        project_dir,
        context_file,
        output_dir,
    ) = get_project_paths(
        args.project
    )

    print()
    print("=" * 60)
    print("Preparing Agent Handoff")
    print("=" * 60)

    print()
    print("目标项目：")
    print(project_dir)

    print()
    print("目标 Agent：")
    print(args.agent)

    # --------------------------------------------------------
    # 非常重要：
    #
    # 交接之前重新生成一次 Context Pack，
    # 防止另一个 Agent 读取旧数据。
    # --------------------------------------------------------

    build_context_pack(
        project_dir=project_dir,
        context_file=context_file,
        output_dir=output_dir,
    )

    print()

    # --------------------------------------------------------
    # Claude
    # --------------------------------------------------------

    if args.agent == "claude":

        print(
            "Claude Code 上下文准备完成。"
        )

        print()
        print(
            "建议首先读取："
        )

        print(
            output_dir
            / "CLAUDE.md"
        )

        print(
            output_dir
            / "HANDOFF.md"
        )

    # --------------------------------------------------------
    # Codex
    # --------------------------------------------------------

    elif args.agent == "codex":

        print(
            "Codex 上下文准备完成。"
        )

        print()
        print(
            "建议首先读取："
        )

        print(
            output_dir
            / "AGENTS.md"
        )

        print(
            output_dir
            / "HANDOFF.md"
        )


# ============================================================
# 6. 给子命令增加公共 --project 参数
# ============================================================

def add_project_argument(parser):
    """
    给不同子命令统一添加 --project。

    这样就不需要：

    init_parser.add_argument(...)
    pack_parser.add_argument(...)
    show_parser.add_argument(...)

    每次重复写完整配置。
    """

    parser.add_argument(
        "--project",
        help=(
            "Target Git project directory. "
            "Defaults to the current directory."
        ),
    )


# ============================================================
# 7. 创建 argparse Parser
# ============================================================

def create_parser():
    """
    定义 Agent Context Bridge CLI。
    """

    parser = argparse.ArgumentParser(
        prog="agent-context",
        description=(
            "Universal context bridge "
            "for AI coding agents."
        ),
    )

    # --------------------------------------------------------
    # 创建子命令系统
    # --------------------------------------------------------

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    # ========================================================
    # init
    # ========================================================

    init_parser = subparsers.add_parser(
        "init",
        help=(
            "Initialize Agent Context "
            "in a Git project."
        ),
    )

    add_project_argument(
        init_parser
    )

    init_parser.set_defaults(
        func=command_init
    )

    # ========================================================
    # pack
    # ========================================================

    pack_parser = subparsers.add_parser(
        "pack",
        help=(
            "Build an Agent Context Pack."
        ),
    )

    add_project_argument(
        pack_parser
    )

    pack_parser.set_defaults(
        func=command_pack
    )

    # ========================================================
    # show
    # ========================================================

    show_parser = subparsers.add_parser(
        "show",
        help=(
            "Show current Agent Context."
        ),
    )

    add_project_argument(
        show_parser
    )

    show_parser.set_defaults(
        func=command_show
    )

    # ========================================================
    # handoff
    # ========================================================

    handoff_parser = subparsers.add_parser(
        "handoff",
        help=(
            "Prepare context for "
            "another AI agent."
        ),
    )

    handoff_parser.add_argument(
        "agent",
        choices=[
            "claude",
            "codex",
        ],
        help="Target AI agent.",
    )

    add_project_argument(
        handoff_parser
    )

    handoff_parser.set_defaults(
        func=command_handoff
    )

    return parser


# ============================================================
# 8. CLI 主入口
# ============================================================

def main():
    """
    Agent Context Bridge CLI 主入口。
    """

    parser = create_parser()

    args = parser.parse_args()

    try:

        args.func(args)

    except Exception as error:

        print()
        print("=" * 60)
        print(
            "Agent Context Bridge 执行失败"
        )
        print("=" * 60)

        print()
        print(error)