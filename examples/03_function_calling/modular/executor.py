"""
工具执行模块
============
收到 AI 的工具调用请求后，执行真实的外部操作。
这就是 Agent "动手做事" 的地方。
"""

import subprocess
import os

# 项目根目录（作为命令执行的工作目录）
PROJECT_ROOT = "/Users/wangjie/AI/myAgent"


def execute_tool(tool_name, tool_input):
    """根据工具名和参数，执行对应的操作，返回结果字符串。"""

    if tool_name == "run_command":
        return _run_command(tool_input["command"])

    elif tool_name == "read_file":
        return _read_file(tool_input["file_path"])

    else:
        return f"错误：未知工具 {tool_name}"


def _run_command(command):
    """执行 shell 命令"""
    print(f"[执行] $ {command}")

    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=10,
            cwd=PROJECT_ROOT
        )

        output = ""
        if result.stdout:
            output += result.stdout
        if result.stderr:
            output += "\n[stderr]\n" + result.stderr
        if result.returncode != 0:
            output += f"\n[退出码: {result.returncode}]"

        return output.strip() if output.strip() else "命令执行成功（无输出）"

    except subprocess.TimeoutExpired:
        return "错误：命令执行超时（超过 10 秒）"
    except Exception as e:
        return f"错误：{str(e)}"


def _read_file(file_path):
    """读取文件内容"""
    print(f"[执行] 读取文件: {file_path}")

    try:
        max_size = 10000  # 最多读 10KB
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read(max_size)

        if len(content) == max_size:
            content += "\n... [文件过大，已截断]"

        return content if content else "文件为空"

    except FileNotFoundError:
        return f"错误：文件不存在 {file_path}"
    except Exception as e:
        return f"错误：{str(e)}"
