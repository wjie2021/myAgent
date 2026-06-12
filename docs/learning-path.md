# AI Agent 学习路径

兴趣驱动，由浅入深。每个阶段都有动手环节，遇到不懂的 Python 语法查 `docs/python/`。

---

## 第零阶段：先搞懂基本概念

> 目标：建立直觉，知道每个东西是什么、干嘛用的。
> 不需要深入原理，知道"是什么"就够了。

### 大模型（LLM）

```text
就是一个函数：输入文字 → 输出文字

你给它："今天天气怎么样？"
它回你："我不知道，我没有联网。"

关键点：它是无状态的，不记得上一轮说过什么。
你得自己把历史消息拼好传给它，它才能"记住"对话。
```

### Prompt（提示词）

```text
就是你发给大模型的那段文字。

Prompt 分两种：
- 用户提示词：你每次问的问题
- 系统提示词：提前告诉 AI "你是谁、怎么回答"，全程不变
```

### System Prompt（系统提示词）

```text
给 AI 的"岗位说明书"。

比如："你是一个旅行助手，用中文回答，格式要求 Thought: ... Action: ..."

它从头到尾不变，AI 每次回答都会参考它。
```

### Context（上下文）

```text
就是对话历史。你说了什么、AI 说了什么、工具返回了什么，全部拼在一起。

每次调用 API，你都要把上下文传进去，AI 才知道之前发生了什么。
```

### Token

```text
大模型计费的单位。大概 1 个汉字 ≈ 1-2 个 token，1 个英文单词 ≈ 1 个 token。

上下文越长，token 越多，费用越高。
```

### Function Calling / Tool Use

```text
让 AI 能"做事"而不只是"说话"。

你告诉 AI 有哪些工具（比如查天气），AI 决定要不要调用、传什么参数，
你执行工具，把结果告诉 AI，AI 再生成最终回答。
```

### ReAct 模式

```text
让 AI 在输出中交替写"我想做什么"和"我做了什么"。

Thought: 用户想查天气，我需要调用工具
Action: get_weather(city="北京")
Observation: 晴天 31°C
Thought: 拿到天气了，可以回答了
Action: Finish[北京今天晴天31°C]

就是一个提示词格式约定，没有魔法。
```

### Agent

```text
= 大模型 + 工具 + 循环

大模型负责"想"，工具负责"做"，循环让它能反复思考直到完成任务。
```

---

## 第一阶段：跑通第一个 Agent

> 目标：亲手跑通一个完整的 Agent，建立感性认识。
> 你已经完成了 `04_hello_agent`，这个阶段可以回顾总结。

### 1.1 直接调 API

用 Anthropic SDK 写一个最简单的对话程序：

```python
from anthropic import Anthropic

client = Anthropic(api_key="xxx", base_url="xxx")
message = client.messages.create(
    model="mimo-v2.5-pro",
    max_tokens=1024,
    messages=[{"role": "user", "content": "你好"}]
)
print(message.content[0].text)
```

体会：无状态 + 手动拼上下文。

📖 Python 查阅：[依赖管理](python/依赖管理.md)、[模块与导入](python/模块与导入.md)

### 1.2 加上工具调用

让 AI 能调用你写的函数（比如查天气）。

📖 Python 查阅：[数据结构与类型](python/数据结构与类型.md)（解析 API 返回值）

### 1.3 跑通 ReAct Agent

你已经完成了 `04_hello_agent`，回顾一下：

- system prompt 是什么？→ [系统提示词与上下文](agent/系统提示词与上下文.md)
- Thought/Action 格式是什么？→ [ReAct 模式](agent/ReAct模式与输出格式.md)
- 循环是怎么控制的？→ 看 `main.py` 的 for 循环

📖 Python 查阅：[控制流与函数](python/控制流与函数.md)

---

## 第二阶段：玩转 Agent

> 目标：在跑通的基础上，尝试修改和扩展，加深理解。

### 2.1 给 Agent 加一个新工具

在 `tools/` 下加一个新函数，比如：

- 查股票价格
- 翻译文本
- 计算数学表达式

观察 AI 怎么决定调用哪个工具。

### 2.2 故意让工具失败

把工具函数改成会报错的，观察 AI 怎么处理：

- 它会重试吗？
- 它会换一种方式回答吗？
- 它会告诉用户"我做不到"吗？

### 2.3 改 System Prompt

修改 `prompts/agent.md`，看看输出怎么变：

- 把"旅行助手"改成"美食专家"
- 把输出格式改一下
- 加一句"如果不确定就不要回答"

📖 Python：学会 dict 操作（工具返回值都是 dict）

---

## 第三阶段：RAG — 让 AI 读你的文档

> 目标：让 AI 能基于你自己的资料回答问题。

### 核心思路

```text
你有很多文档 → 切片 → 向量化 → 存起来
用户问问题 → 搜索相关片段 → 拼进 Prompt → AI 回答
```

### 3.1 理解 Embedding

把文字变成向量（一串数字），语义相近的文字，向量也相近。

### 3.2 搭一个简单的 RAG

用 LangChain 或 LlamaIndex，或者纯 API 手写：

1. 把几篇文档切片
2. 用 Embedding 模型转成向量
3. 用户提问时，搜索最相关的片段
4. 把片段拼进 Prompt，让 AI 回答

📖 Python：学会文件读写（`open()` 读文档）

---

## 第四阶段：工程化

> 目标：理解 Agent 的工程化思路。

### 4.1 Workflow（工作流）

把确定性流程固化，减少 LLM 调用，节省 token。

适合：流程固定、不需要 AI 自主决策的场景。

### 4.2 Skill（技能）

把常用能力（提示词 + 脚本 + 说明文档）打包，按需加载。

### 4.3 可以看看这些平台

- **Dify** — 可视化 Agent 编排
- **Coze（扣子）** — 字节的 Agent 平台
- **Claude Code** — 你现在用的这个

---

## Python 学习（穿插在各阶段）

不用系统学，遇到不懂的查速查手册：

| 文档 | 什么时候看 |
|------|-----------|
| [python与java对比](python/python与java对比.md) | 刚接触 Python 时 |
| [数据结构与类型](python/数据结构与类型.md) | 解析 API 返回值时 |
| [控制流与函数](python/控制流与函数.md) | 写 Agent 逻辑时 |
| [模块与导入](python/模块与导入.md) | 组织代码文件时 |
| [依赖管理](python/依赖管理.md) | 安装包报错时 |

---

## 学习资源

| 资源 | 说明 |
|------|------|
| [modelcontextprotocol.io](https://modelcontextprotocol.io) | MCP 协议官方文档 |
| Anthropic "Building effective agents" | Agent 设计思路 |
| OpenAI / Anthropic 官方 quickstart | API 入门 |

---

## 一句话总结

**概念够用就行 → 跑通 Agent → 玩起来 → 加功能 → RAG → 工程化**

不用急，每个阶段都动手试试，遇到问题再回来查概念。
