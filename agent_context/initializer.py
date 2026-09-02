import json
from pathlib import Path

from agent_context.git_reader import (
    check_git_repository,
    get_git_branch,
)


def create_default_context(project_dir):
    """
    根据目标项目自动生成一份最基础的 Context。
    """

    project_name = project_dir.name

    try:
        branch = get_git_branch(project_dir)
    except Exception:
        branch = ""

    context = {
        "version": "0.5",

        "project": {
            "name": project_name,
            "path": project_dir.as_posix(),
            "branch": branch
        },

        "task": {
            "title": "请填写当前任务",
            "description": "请描述当前需要 AI Agent 完成的工作"
        },

        "progress": {
            "completed": [],
            "current": "尚未开始",
            "problems": []
        },

        "decisions": [],

        "next_steps": []
    }

    return context


def create_example_context():
    """
    创建可以提交到 Git 仓库的 Context 示例文件。
    """

    return {
        "version": "0.5",

        "project": {
            "name": "example-project",
            "path": "",
            "branch": "main"
        },

        "task": {
            "title": "Example task",
            "description": "Describe the current task here."
        },

        "progress": {
            "completed": [],
            "current": "",
            "problems": []
        },

        "decisions": [],

        "next_steps": []
    }


def save_json(file_path, data):
    """
    将 Python 字典保存成 JSON 文件。
    """

    with open(
        file_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=2
        )


def update_gitignore(project_dir):
    """
    自动更新目标项目的 .gitignore。

    防止本地上下文和生成结果被意外提交。
    """

    gitignore_file = (
        project_dir
        / ".gitignore"
    )

    required_rules = [
        ".agent-context/",
        "context/context.json"
    ]

    # 如果原项目已经有 .gitignore，
    # 先读取原来的内容
    if gitignore_file.exists():

        content = gitignore_file.read_text(
            encoding="utf-8"
        )

    else:

        content = ""

    lines_to_add = []

    for rule in required_rules:

        if rule not in content:
            lines_to_add.append(rule)

    # 如果所有规则本来就存在，
    # 就不用修改
    if not lines_to_add:
        return

    block = "\n# Agent Context Bridge\n"

    for rule in lines_to_add:
        block += rule + "\n"

    with open(
        gitignore_file,
        "a",
        encoding="utf-8"
    ) as file:

        file.write(block)


def initialize_project(project_dir):
    """
    将普通 Git 项目初始化成
    Agent Context Bridge 项目。
    """

    project_dir = Path(
        project_dir
    ).resolve()

    print()
    print("=" * 60)
    print("Initializing Agent Context Project")
    print("=" * 60)

    print()
    print("目标项目：")
    print(project_dir)

    # ------------------------------------------------
    # 1. 检查目录是否存在
    # ------------------------------------------------

    if not project_dir.exists():

        raise FileNotFoundError(
            f"项目目录不存在：{project_dir}"
        )

    if not project_dir.is_dir():

        raise NotADirectoryError(
            f"目标路径不是目录：{project_dir}"
        )

    # ------------------------------------------------
    # 2. 检查是不是 Git 仓库
    # ------------------------------------------------

    try:

        check_git_repository(
            project_dir
        )

    except Exception as error:

        raise RuntimeError(
            "目标目录不是有效 Git 仓库。\n"
            "请先在目标项目中执行 git init。"
        ) from error

    # ------------------------------------------------
    # 3. 创建 context 目录
    # ------------------------------------------------

    context_dir = (
        project_dir
        / "context"
    )

    context_dir.mkdir(
        exist_ok=True
    )

    # ------------------------------------------------
    # 4. 定义文件路径
    # ------------------------------------------------

    context_file = (
        context_dir
        / "context.json"
    )

    example_file = (
        context_dir
        / "context.example.json"
    )

    # ------------------------------------------------
    # 5. 不覆盖用户已经存在的 Context
    # ------------------------------------------------

    if context_file.exists():

        print()
        print(
            "context/context.json 已存在，"
            "不会覆盖。"
        )

    else:

        context = create_default_context(
            project_dir
        )

        save_json(
            context_file,
            context
        )

        print()
        print(
            "已创建：",
            context_file
        )

    # ------------------------------------------------
    # 6. 创建 example
    # ------------------------------------------------

    if not example_file.exists():

        save_json(
            example_file,
            create_example_context()
        )

        print(
            "已创建：",
            example_file
        )

    # ------------------------------------------------
    # 7. 更新 gitignore
    # ------------------------------------------------

    update_gitignore(
        project_dir
    )

    print(
        "已检查：",
        project_dir / ".gitignore"
    )

    print()
    print("=" * 60)
    print("初始化完成")
    print("=" * 60)

    print()
    print(
        "下一步请编辑："
    )

    print(
        context_file
    )