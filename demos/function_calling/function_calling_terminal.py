"""
Function Calling 连接外部工具 demo
==================================
这个 demo 让 AI 能执行真实的终端命令：
- ls/dir：查看目录内容
- cat/type：查看文件内容
- python：执行 Python 代码
- 任意 shell 命令

关键理解：execute_tool() 就是一个普通函数
         里面调什么完全由你决定
         调本地函数、调外部 API、执行命令 都行
"""

import subprocess  # 用于执行终端命令
import os          # 用于文件/路径操作
from anthropic import Anthropic

# ============================================================
# 客户端
# ============================================================
client = Anthropic(
    api_key="tp-ci6a2b51kji3da55zqnlvh7x6pqs9ebezverd7hjrnppgc8g",
    base_url="https://token-plan-cn.xiaomimimo.com/anthropic"
)

# ============================================================
# 工具定义（告诉 AI 有哪些工具）
# ============================================================
tools = [
    {
        "name": "run_command",
        "description": "在终端执行 shell 命令并返回输出结果。可以用来：查看目录(ls/dir)、读取文件(cat/type)、运行脚本等。",
        "input_schema": {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "要执行的终端命令，如 'ls'、'dir'、'cat file.txt'、'python script.py'"
                }
            },
            "required": ["command"]
        }
    },
    {
        "name": "read_file",
        "description": "读取指定文件的内容。当用户想查看某个文件时使用。",
        "input_schema": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "文件的路径，如 'd:/0my/claude/myAgent/README.md'"
                }
            },
            "required": ["file_path"]
        }
    }
]

# ============================================================
# 工具实现（连接真实外部工具）
# ============================================================
def execute_tool(tool_name, tool_input):
    """
    这里就是连接外部工具的地方
    你可以调用任何东西：shell 命令、API、数据库...
    """

    if tool_name == "run_command":
        command = tool_input["command"]
        print(f"[执行] $ {command}")

        try:
            # subprocess.run() 执行终端命令
            # capture_output=True 捕获输出
            # text=True 以字符串返回（而非 bytes）
            # shell=True 允许使用 shell 语法（如 ls、dir）
            # timeout=10 防止命令卡死
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=10,
                cwd="d:/0my/claude/myAgent"  # 工作目录设为项目根目录
            )

            # 组装输出
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

    elif tool_name == "read_file":
        file_path = tool_input["file_path"]
        print(f"[执行] 读取文件: {file_path}")

        try:
            # 限制读取大小，防止读到超大文件
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

    else:
        return f"错误：未知工具 {tool_name}"

# ============================================================
# 对话循环
# ============================================================
history = []

print("=== Function Calling 终端工具 Demo ===")
print("我能帮你执行终端命令！试试：")
print("  - '帮我看看当前目录有什么文件'")
print("  - '读一下 README.md 的内容'")
print("  - '运行 python --version'")
print("输入 quit/exit/退出 结束\n")

while True:
    user_input = input("你: ")

    if user_input.lower() in ["quit", "exit", "退出"]:
        print("再见！")
        break

    history.append({"role": "user", "content": user_input})

    # --- 第 1 次调用：AI 决定是否调用工具 ---
    try:
        response = client.messages.create(
            model="mimo-v2.5-pro",
            max_tokens=1024,
            tools=tools,
            messages=history
        )
    except Exception as e:
        print(f"出错了: {e}")
        history.pop()
        continue

    # 分析 AI 的回复
    tool_uses = []
    for block in response.content:
        if block.type == "text":
            print(f"[调试] AI 文本: {block.text}")
        elif block.type == "tool_use":
            tool_uses.append(block)
            print(f"[调试] AI 要调用工具: {block.name}")

    # --- 没有工具调用，直接输出 ---
    if not tool_uses:
        history.append({"role": "assistant", "content": response.content})
        for block in response.content:
            if block.type == "text":
                print("AI：" + block.text)
        continue

    # --- 有工具调用：执行工具 ---
    history.append({"role": "assistant", "content": response.content})

    tool_results = []
    for tool_use in tool_uses:
        print(f"[调试] 执行: {tool_use.name}({tool_use.input})")

        # 执行真实的外部工具！
        result = execute_tool(tool_use.name, tool_use.input)
        print(f"[调试] 结果:\n{result[:200]}...")  # 只打印前 200 字符

        tool_results.append({
            "type": "tool_result",
            "tool_use_id": tool_use.id,
            "content": result
        })

    history.append({"role": "user", "content": tool_results})

    # --- 第 2 次调用：AI 根据工具结果回复 ---
    try:
        response2 = client.messages.create(
            model="mimo-v2.5-pro",
            max_tokens=1024,
            tools=tools,
            messages=history
        )
    except Exception as e:
        print(f"出错了: {e}")
        continue

    history.append({"role": "assistant", "content": response2.content})

    for block in response2.content:
        if block.type == "text":
            print("AI：" + block.text)

    print(f"[调试] 历史: {len(history)} 条\n")
