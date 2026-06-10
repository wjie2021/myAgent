"""
Function Calling 基础 demo
========================
这个 demo 演示了 Function Calling 的完整流程：
1. 定义工具（告诉 AI 有哪些工具可用）
2. AI 决定是否调用工具，并返回调用参数
3. 你执行工具，把结果返回给 AI
4. AI 根据工具结果生成最终回复


- tools = 接口定义
- tool_use = AI 调用接口，传参
- tool_result = 你实现接口，返回结果
"""

from anthropic import Anthropic

# ============================================================
# 第 1 部分：创建客户端
# ============================================================
client = Anthropic(
    api_key="tp-ci6a2b51kji3da55zqnlvh7x6pqs9ebezverd7hjrnppgc8g",
    base_url="https://token-plan-cn.xiaomimimo.com/anthropic"
)

# ============================================================
# 第 2 部分：定义工具（告诉 AI 有哪些工具可用）
# ============================================================
# 这就像 Java 里定义接口：名称、描述、参数类型
tools = [
    {
        "name": "calculator",           # 工具名称（AI 调用时用这个名字）
        "description": "一个简单的计算器，支持加减乘除运算。当用户需要计算数学题时使用这个工具。",
        "input_schema": {               # 参数定义（JSON Schema 格式）
            "type": "object",
            "properties": {
                "operation": {
                    "type": "string",
                    "description": "运算类型",
                    "enum": ["add", "subtract", "multiply", "divide"]  # 限定可选值
                },
                "a": {
                    "type": "number",
                    "description": "第一个操作数"
                },
                "b": {
                    "type": "number",
                    "description": "第二个操作数"
                }
            },
            "required": ["operation", "a", "b"]  # 必填参数
        }
    },
    {
        "name": "get_weather",
        "description": "查询指定城市的天气信息。当用户问天气时使用这个工具。",
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "城市名称，如：北京、上海、广州"
                }
            },
            "required": ["city"]
        }
    }
]

# ============================================================
# 第 3 部分：定义工具的执行逻辑（你实现接口）
# ============================================================
# 这就是 Java 里接口的实现类
def execute_tool(tool_name, tool_input):
    """
    根据工具名称和参数，执行对应的逻辑
    :param tool_name: 工具名称（如 "calculator"）
    :param tool_input: AI 传来的参数字典（如 {"operation": "add", "a": 1, "b": 2}）
    :return: 工具执行结果（字符串）
    """
    if tool_name == "calculator":
        op = tool_input["operation"]
        a = tool_input["a"]
        b = tool_input["b"]

        if op == "add":
            result = a + b
        elif op == "subtract":
            result = a - b
        elif op == "multiply":
            result = a * b
        elif op == "divide":
            if b == 0:
                return "错误：除数不能为零"
            result = a / b
        else:
            return f"错误：未知运算类型 {op}"

        return f"{a} {op} {b} = {result}"

    elif tool_name == "get_weather":
        city = tool_input["city"]
        # 模拟天气数据（实际项目中这里会调用真实的天气 API）
        fake_weather = {
            "北京": "晴天，25°C",
            "上海": "多云，22°C",
            "广州": "小雨，28°C",
        }
        weather = fake_weather.get(city, f"暂无 {city} 的天气数据")
        return f"{city} 的天气：{weather}"

    else:
        return f"错误：未知工具 {tool_name}"

# ============================================================
# 第 4 部分：对话循环（带 Function Calling）
# ============================================================
history = []

print("=== Function Calling Demo ===")
print("试试问我：'帮我算一下 123 + 456' 或 '北京天气怎么样'")
print("输入 quit/exit/退出 结束\n")

while True:
    user_input = input("你: ")

    if user_input.lower() in ["quit", "exit", "退出"]:
        print("再见！")
        break

    # 把用户消息加到历史
    history.append({"role": "user", "content": user_input})

    # --- 第一次调用 API：AI 决定是否需要调用工具 ---
    print("[调试-发给AI] 第一次调用 API（AI 决定是否调用工具）...")
    try:
        response = client.messages.create(
            model="mimo-v2.5-pro",
            max_tokens=1024,
            tools=tools,        # 关键：传入工具定义
            messages=history
        )
    except Exception as e:
        print(f"出错了: {e}")
        history.pop()  # 移除失败的用户消息
        continue

    print(f"[调试-AI返回] AI 返回了 {len(response.content)} 个内容块，stop_reason={response.stop_reason}")

    # --- 处理 AI 的回复 ---
    # AI 的回复可能包含多种类型的 content block：
    #   - type="text"     → 普通文本回复
    #   - type="tool_use" → AI 想调用工具

    tool_uses = []   # 收集 AI 想调用的工具
    text_parts = []  # 收集文本回复

    for block in response.content:
        if block.type == "text":
            text_parts.append(block.text)
            print(f"[调试-AI返回] 文本块: {block.text}")
        elif block.type == "tool_use":
            tool_uses.append(block)
            print(f"[调试-AI返回] 工具调用: {block.name}({block.input})")

    # --- 如果 AI 没有调用工具，直接输出文本 ---
    if not tool_uses:
        # 把 AI 的回复加到历史
        assistant_content = response.content
        history.append({"role": "assistant", "content": assistant_content})

        if text_parts:
            print("AI：" + "\n".join(text_parts))
        else:
            print("AI：（无回复）")
        continue

    # --- 如果 AI 调用了工具 ---
    # 步骤 1：先把 AI 的回复（包含 tool_use）加到历史
    history.append({"role": "assistant", "content": response.content})

    # 步骤 2：执行每个工具，收集结果
    tool_results = []
    for tool_use in tool_uses:
        print(f"[调试-执行工具] 执行工具: {tool_use.name}")
        print(f"[调试-执行工具] 参数: {tool_use.input}")

        # 调用你实现的工具函数
        result = execute_tool(tool_use.name, tool_use.input)
        print(f"[调试-执行工具] 工具结果: {result}")

        # 构造 tool_result 格式（必须包含 tool_use_id）
        tool_results.append({
            "type": "tool_result",
            "tool_use_id": tool_use.id,   # 关联到 AI 的那次 tool_use
            "content": result
        })

    # 步骤 3：把工具结果加到历史
    history.append({"role": "user", "content": tool_results})

    # 步骤 4：再次调用 API，让 AI 根据工具结果生成最终回复
    print("[调试] 第二次调用 API（AI 根据工具结果生成回复）...")
    try:
        response2 = client.messages.create(
            model="mimo-v2.5-pro",
            max_tokens=1024,
            tools=tools,        # 工具定义也要传
            messages=history
        )
    except Exception as e:
        print(f"出错了: {e}")
        continue

    # 步骤 5：输出最终回复
    final_text = ""
    for block in response2.content:
        if block.type == "text":
            final_text += block.text

    # 把最终回复加到历史
    history.append({"role": "assistant", "content": response2.content})

    if final_text:
        print("AI：" + final_text)
    else:
        print("AI：（工具已执行，但无额外回复）")

    print(f"[调试] 历史记录: {len(history)} 条\n")
