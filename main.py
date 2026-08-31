print("Agent Context Bridge starting...")
import json
import os
import subprocess

def load_context():
    """
    从 context/context.json 中读取上下文
    """

    with open(
        "context/context.json",
        "r",
        encoding="utf-8"
    ) as file:

        context = json.load(file)

    return context


def show_context(context):
    """
    将上下文中的主要信息显示到终端
    """

    print("=" * 50)

    print("Agent Context Bridge")

    print("=" * 50)

    print()

    print("项目名称：")
    print(context["project"]["name"])

    print()

    print("当前任务：")
    print(context["task"]["title"])

    print()

    print("任务说明：")
    print(context["task"]["description"])

    print()

    print("当前进度：")
    print(context["progress"]["current"])

    print()

    print("下一步：")

    for step in context["next_steps"]:
        print("-", step)

def run_git_command(command):
    """
    执行 Git 命令，并返回执行结果。
    """

    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True,
        encoding="utf-8"
    )

    return result.stdout

def get_git_status():

    print()
    print("正在读取 Git 状态...")

    status = run_git_command("git status --short")

    return status

def main():

    print("程序启动成功！")

    context = load_context()

    if context is None:
        return

    show_context(context)

    git_status = get_git_status()

    print()
    print("=" * 50)
    print("Git 当前状态")
    print("=" * 50)

    if git_status.strip():
        print(git_status)
    else:
        print("当前没有未提交修改。")


if __name__ == "__main__":
    main()