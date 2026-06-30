import re
from typing import Callable, Optional
from llm import HelloAgentsLLM
from tools import ToolExecutor, search

# ReAct 提示词模板
REACT_PROMPT_TEMPLATE = """
请注意，你是一个有能力调用外部工具的智能助手。

可用工具如下：
{tools}

请严格按照以下格式进行回应：

Thought: 你的思考过程，用于分析问题、拆解任务和规划下一步行动。
Action: 你决定采取的行动，必须是以下格式之一：
- `{{tool_name}}[{{tool_input}}]`：调用一个可用工具。
- `Finish[最终答案]`：当你认为已经获得最终答案时。
- 当你收集到足够的信息，能够回答用户的最终问题时，你必须在`Action:`字段后使用 `Finish[最终答案]` 来输出最终答案。


现在，请开始解决以下问题：
Question: {question}
History: {history}
"""


class ReActAgent:
    def __init__(
        self,
        llm_client: HelloAgentsLLM,
        tool_executor: ToolExecutor,
        max_steps: int = 5,
    ):
        self.llm_client = llm_client
        self.tool_executor = tool_executor
        self.max_steps = max_steps
        self.history = []

    def _parse_output(self, text: str):
        """解析LLM的输出，提取Thought和Action。"""
        thought_match = re.search(r"Thought:\s*(.*?)(?=\nAction:|$)", text, re.DOTALL)
        action_match = re.search(r"Action:\s*(.*?)$", text, re.DOTALL)
        thought = thought_match.group(1).strip() if thought_match else None
        action = action_match.group(1).strip() if action_match else None
        return thought, action

    def _parse_action(self, action_text: str):
        """解析Action字符串，提取工具名称和输入。"""
        match = re.match(r"(\w+)\[(.*)\]", action_text, re.DOTALL)
        if match:
            return match.group(1), match.group(2)
        return None, None

    def run(
        self,
        question: str,
        on_step: Optional[Callable[[dict], None]] = None,
    ) -> dict:
        """
        运行ReAct智能体来回答一个问题。

        Args:
            question: 用户问题
            on_step: 每一步的回调，用于流式推送思考过程
                     回调参数: {"step": int, "type": "thought"|"action"|"observation"|"finish", "content": str}

        Returns:
            {"answer": str, "steps": list, "success": bool}
        """
        self.history = []
        steps = []
        current_step = 0

        def notify(step_data: dict):
            """通知前端每一步的进展"""
            steps.append(step_data)
            if on_step:
                on_step(step_data)

        while current_step < self.max_steps:
            current_step += 1

            # 1. 格式化提示词
            tools_desc = self.tool_executor.getAvailableTools()
            history_str = "\n".join(self.history)
            prompt = REACT_PROMPT_TEMPLATE.format(
                tools=tools_desc, question=question, history=history_str
            )

            # 2. 调用LLM进行思考
            messages = [{"role": "user", "content": prompt}]
            response_text = self.llm_client.think(messages=messages)

            if not response_text:
                notify({
                    "step": current_step,
                    "type": "error",
                    "content": "LLM未能返回有效响应",
                })
                break

            # 3. 解析LLM的输出
            thought, action = self._parse_output(response_text)

            if thought:
                notify({
                    "step": current_step,
                    "type": "thought",
                    "content": thought,
                })

            if not action:
                notify({
                    "step": current_step,
                    "type": "error",
                    "content": "未能解析出有效的Action",
                })
                break

            # 4. 执行Action
            if action.startswith("Finish"):
                final_match = re.match(r"Finish\[(.*)\]", action, re.DOTALL)
                if final_match:
                    final_answer = final_match.group(1)
                else:
                    final_answer = action.replace("Finish", "").strip("[]:： ")

                notify({
                    "step": current_step,
                    "type": "finish",
                    "content": final_answer,
                })
                return {"answer": final_answer, "steps": steps, "success": True}

            tool_name, tool_input = self._parse_action(action)
            if not tool_name or not tool_input:
                notify({
                    "step": current_step,
                    "type": "error",
                    "content": "无效的Action格式",
                })
                continue

            notify({
                "step": current_step,
                "type": "action",
                "content": f"{tool_name}[{tool_input}]",
            })

            # 5. 执行工具
            tool_function = self.tool_executor.getTool(tool_name)
            if not tool_function:
                observation = f"错误: 未找到名为 '{tool_name}' 的工具。"
            else:
                observation = tool_function(tool_input)

            notify({
                "step": current_step,
                "type": "observation",
                "content": observation,
            })

            # 记录历史
            self.history.append(f"Action: {action}")
            self.history.append(f"Observation: {observation}")

        # 超过最大步数
        notify({
            "step": current_step,
            "type": "error",
            "content": "已达到最大步数，流程终止",
        })
        return {"answer": None, "steps": steps, "success": False}


if __name__ == '__main__':
    llm_client = HelloAgentsLLM()
    tool_executor = ToolExecutor()
    search_description = "一个网页搜索引擎。当你需要回答关于时事、事实以及在你的知识库中找不到的信息时，应使用此工具。"
    tool_executor.registerTool("Search", search_description, search)
    agent = ReActAgent(llm_client=llm_client, tool_executor=tool_executor)
    result = agent.run("英伟达最新的GPU型号是什么？")
    print(result)
