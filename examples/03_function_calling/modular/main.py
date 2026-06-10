"""
Function Calling 模块化 Demo
============================
把原来的单文件拆成了 4 个模块：

  client.py   → 初始化 AI 客户端
  tools.py    → 定义有哪些工具（接口）
  executor.py → 实现工具怎么执行（实现）
  main.py     → 对话循环（本文件，主入口）

运行方式：python3 main.py
"""

from client import client
from tools import tools
from executor import execute_tool


def chat_loop():
    """主对话循环"""
    history = []

    print("=== Function Calling 终端工具 Demo（模块化版） ===")
    print("我能帮你执行终端命令！试试：")
    print("  - '帮我看看当前目录有什么文件'")
    print("  - '读一下 README.md 的内容'")
    print("  - '运行 python3 --version'")
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
            print(f"[调试] 结果:\n{result[:200]}...")

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


# Python 的惯例：直接运行此文件时才执行 chat_loop()
# 如果是被 import 导入的，则不自动执行
if __name__ == "__main__":
    chat_loop()
