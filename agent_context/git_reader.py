import subprocess


def run_git_command(project_dir, arguments):
    """
    在指定项目目录中执行 Git 命令。

    例如：

    run_git_command(
        project_dir,
        ["status", "--short"]
    )

    相当于：

    git status --short
    """

    result = subprocess.run(
        ["git"] + arguments,
        cwd=project_dir,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace"
    )

    # returncode == 0
    # 表示 Git 命令执行成功
    if result.returncode == 0:
        return result.stdout.strip()

    # 如果执行失败，就主动抛出错误
    raise RuntimeError(
        "Git 命令执行失败：git "
        + " ".join(arguments)
        + "\n"
        + result.stderr
    )


def check_git_repository(project_dir):
    """
    检查当前目录是不是 Git 仓库。

    git rev-parse --is-inside-work-tree

    正常情况下返回：
    true
    """

    result = run_git_command(
        project_dir,
        [
            "rev-parse",
            "--is-inside-work-tree"
        ]
    )

    return result == "true"


def get_git_branch(project_dir):
    """
    获取当前所在 Git 分支。
    """

    return run_git_command(
        project_dir,
        [
            "branch",
            "--show-current"
        ]
    )


def get_git_status(project_dir):
    """
    获取当前文件修改状态。
    """

    return run_git_command(
        project_dir,
        [
            "status",
            "--short"
        ]
    )


def get_git_diff(project_dir):
    """
    获取还没有 git add 的代码修改。
    """

    return run_git_command(
        project_dir,
        [
            "diff"
        ]
    )


def get_git_staged_diff(project_dir):
    """
    获取已经 git add，
    但还没有 commit 的修改。
    """

    return run_git_command(
        project_dir,
        [
            "diff",
            "--cached"
        ]
    )


def get_git_log(project_dir):
    """
    获取最近 5 次提交。
    """

    return run_git_command(
        project_dir,
        [
            "log",
            "-5",
            "--oneline"
        ]
    )


def get_current_commit(project_dir):
    """
    获取当前 HEAD 所在 commit 的完整哈希值。
    """

    return run_git_command(
        project_dir,
        [
            "rev-parse",
            "HEAD"
        ]
    )


def collect_git_context(project_dir):
    """
    一次性收集全部 Git 上下文。

    最终返回 Python 字典。
    """

    if not check_git_repository(project_dir):
        raise RuntimeError(
            "当前目录不是 Git 仓库。"
        )

    git_context = {
        "branch": get_git_branch(project_dir),
        "status": get_git_status(project_dir),
        "diff": get_git_diff(project_dir),
        "staged_diff": get_git_staged_diff(project_dir),
        "log": get_git_log(project_dir),
        "current_commit": get_current_commit(project_dir)
    }

    return git_context