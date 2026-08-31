# TODO: 下一阶段加入 Agent Adapter
from pathlib import Path

from agent_context.context_builder import build_context_pack


# 当前项目根目录
BASE_DIR = Path(__file__).resolve().parent


# 人工上下文文件
CONTEXT_FILE = (
    BASE_DIR
    / "context"
    / "context.json"
)


# 自动生成的 Context Pack
OUTPUT_DIR = (
    BASE_DIR
    / ".agent-context"
)


def main():
    """
    Agent Context Bridge 程序入口。
    """

    print("=" * 60)
    print("Agent Context Bridge v0.2")
    print("=" * 60)

    build_context_pack(
        project_dir=BASE_DIR,
        context_file=CONTEXT_FILE,
        output_dir=OUTPUT_DIR
    )


if __name__ == "__main__":
    main()