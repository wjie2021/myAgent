"""
智能旅行助手 - ReAct 模式 Agent 示例

学习要点：
- ReAct 模式：Thought -> Action -> Observation 循环
- 工具调用：Agent 根据 LLM 输出调用外部工具
- 结果解析：从 LLM 输出中提取结构化信息
"""

import re

from config import API_KEY, BASE_URL, MODEL_ID, MAX_LOOP_COUNT
from client import OpenAICompatibleClient
from tools import get_weather, get_attraction

# --- 1. 加载系统提示词 ---
with open("prompts/agent.md", "r", encoding="utf-8") as f:
    AGENT_SYSTEM_PROMPT = f.read()

# --- 2. 配置 LLM 客户端 ---
llm = OpenAICompatibleClient(
    model=MODEL_ID,
    api_key=API_KEY,
    base_url=BASE_URL
)

# --- 3. 注册可用工具 ---
available_tools = {
    "get_weather": get_weather,
    "get_attraction": get_attraction,
}

# --- 4. 初始化 ---
user_prompt = "你好，请帮我查询一下今天南京的天气，然后根据天气推荐一个合适的旅游景点。"
prompt_history = [f"用户请求: {user_prompt}"]

print(f"用户输入: {user_prompt}\n" + "="*40)

# --- 5. 运行主循环 ---
for i in range(MAX_LOOP_COUNT):
    print(f"--- 循环 {i+1} ---\n")

    # 5.1. 构建 Prompt
    full_prompt = "\n".join(prompt_history)

    # 5.2. 调用 LLM 进行思考
    llm_output = llm.generate(full_prompt, system_prompt=AGENT_SYSTEM_PROMPT)

    # 模型可能会输出多余的 Thought-Action，需要截断
    match = re.search(r'(Thought:.*?Action:.*?)(?=\n\s*(?:Thought:|Action:|Observation:)|\Z)', llm_output, re.DOTALL)
    if match:
        truncated = match.group(1).strip()
        if truncated != llm_output.strip():
            llm_output = truncated
            print("已截断多余的 Thought-Action 对")

    print(f"模型输出:\n{llm_output}\n")
    prompt_history.append(llm_output)

    # 5.3. 解析并执行行动
    action_match = re.search(r"Action: (.*)", llm_output, re.DOTALL)
    if not action_match:
        observation = "错误: 未能解析到 Action 字段。请确保你的回复严格遵循 'Thought: ... Action: ...' 的格式。"
        observation_str = f"Observation: {observation}"
        print(f"{observation_str}\n" + "="*40)
        prompt_history.append(observation_str)
        continue

    action_str = action_match.group(1).strip()

    # 检查是否完成任务
    if action_str.startswith("Finish"):
        final_answer = re.match(r"Finish\[(.*)\]", action_str).group(1)
        print(f"任务完成，最终答案: {final_answer}")
        break

    # 解析工具调用
    tool_name = re.search(r"(\w+)\(", action_str).group(1)
    args_str = re.search(r"\((.*)\)", action_str).group(1)
    kwargs = dict(re.findall(r'(\w+)="([^"]*)"', args_str))

    # 执行工具调用
    if tool_name in available_tools:
        observation = available_tools[tool_name](**kwargs)
    else:
        observation = f"错误:未定义的工具 '{tool_name}'"

    # 5.4. 记录观察结果
    observation_str = f"Observation: {observation}"
    print(f"{observation_str}\n" + "="*40)
    prompt_history.append(observation_str)
else:
    print("达到最大循环次数，任务未完成。")
