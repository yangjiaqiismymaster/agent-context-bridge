import json


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


def main():

    context = load_context()

    show_context(context)


if __name__ == "__main__":
    main()