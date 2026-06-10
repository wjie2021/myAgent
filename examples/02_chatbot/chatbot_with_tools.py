import os
from anthropic import Anthropic

# 创建 Anthropic 客户端
client = Anthropic(
    api_key="tp-ci6a2b51kji3da55zqnlvh7x6pqs9ebezverd7hjrnppgc8g",
    base_url="https://token-plan-cn.xiaomimimo.com/anthropic"
)

# 对话历史，用于保存所有消息（用户 + AI）
history = []

# 无限循环，持续对话
while True:
    # 获取用户输入
    user_input = input("你: ")

    # 输入 quit/exit/退出 时结束程序
    if user_input.lower() in ["quit", "exit", "退出"]:
        print("再见！")
        break  # 跳出 while 循环

    # 把用户消息加到历史（简单格式，content 直接用字符串）
    history.append({"role": "user", "content": user_input})

    # 调试信息：打印实际发送给 AI 的内容（包含上下文）
    print(f"[调试] 发送给 AI 的消息 ({len(history)} 条):")
    for msg in history:
        print(f"  {msg['role']}: {msg['content']}")

    # 调用 API，传入完整历史
    try:
        response = client.messages.create(
            model="mimo-v2.5-pro",
            max_tokens=1024,
            messages=history  # 全部历史，AI 能看到之前的对话
        )
    except Exception as e:
        # API 调用失败时打印错误，继续循环
        print(f"出错了: {e}")
        continue

    # 从回复中提取文本（response.content 是列表，第一个元素是文本块）
    assistant_text = response.content[0].text

    # 把 AI 回复加到历史
    history.append({"role": "assistant", "content": assistant_text})

    # 打印 AI 回复
    print("AI：" + assistant_text)

    # 调试信息：显示当前历史条数
    print(f"[调试] 历史记录: {len(history)} 条")
