# AI Agent 学习路径

兴趣驱动，由浅入深。每个阶段都有动手环节，遇到不懂的 Python 语法查 `docs/python/`。

---

## 第零阶段：先搞懂基本概念 ✅

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

## 第一阶段：跑通第一个 Agent ✅

> 目标：亲手跑通一个完整的 Agent，建立感性认识。
> 你已完成全部子任务，这里做回顾总结。

### 1.1 直接调 API

用 SDK 写一个最简单的对话程序：

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

📖 代码：[examples/01_hello/echo.py](../examples/01_hello/echo.py) | [examples/02_chatbot/chatbot.py](../examples/02_chatbot/chatbot.py)
📖 Python 查阅：[依赖管理](python/依赖管理.md)、[模块与导入](python/模块与导入.md)

### 1.2 多轮对话

给 chatbot 加上 while 循环，手动维护一个 `history` 列表——每次调用 API 前把历史拼回去。

📖 代码：[examples/02_chatbot/chatbot_while.py](../examples/02_chatbot/chatbot_while.py)
📖 Python 查阅：[数据结构与类型](python/数据结构与类型.md)（list 的 append、字符串拼接）

### 1.3 加上工具调用

让 AI 能调用你写的函数（计算器、天气查询、终端命令）。

📖 代码：[examples/03_function_calling/function_calling_basic.py](../examples/03_function_calling/function_calling_basic.py) | [function_calling_terminal.py](../examples/03_function_calling/function_calling_terminal.py)

### 1.4 模块化重构

把散落在一块的代码拆成清晰的模块：`client.py`（LLM 通信）、`executor.py`（工具调度）、`tools.py`（工具定义）、`main.py`（主流程）。

📖 代码：[examples/03_function_calling/modular/](../examples/03_function_calling/modular/)

### 1.5 跑通 ReAct Agent（两个版本）

#### 版本 A — 04_hello_agent（旅行助手）

- 用 OpenAI 兼容客户端，System Prompt 从文件加载
- for 循环控制，手动用正则解析 `Thought:` 和 `Action:`
- 工具有：天气查询、景点推荐

📖 代码：[examples/04_hello_agent/main.py](../examples/04_hello_agent/main.py)
📖 文档：[系统提示词与上下文](agent/提问的AI回复/系统提示词与上下文.md) | [ReAct 模式](agent/提问的AI回复/ReAct模式与输出格式.md)

#### 版本 B — 06_ReAct（搜索引擎 Agent）

- 用 OpenAI SDK（流式输出），封装成 `ReActAgent` 类
- while 循环 + 最大步数限制，更干净的解析逻辑
- 工具有：SerpAPI Google 搜索

📖 代码：[examples/06_ReAct/agent.py](../examples/06_ReAct/agent.py)

**两个版本对比学习：** 同一个 ReAct 模式，不同的实现方式——体会 Agent Loop 的本质是语言模型 + while 循环，封装形式可以多样。

### 1.6 Transformer 基础（可选）

用 PyTorch 实现了 Transformer 的核心组件（位置编码等），理解 LLM 底层架构的基本构件。

📖 代码：[examples/05_transformer/transformerDemo.py](../examples/05_transformer/transformerDemo.py)
📖 文档：[docs/notes/transformer-intro.md](notes/transformer-intro.md)

---

## 第二阶段：Agent 核心机制 🔄

> 目标：不再只是"跑通"，而是深入理解 Agent 的运行时行为和控制逻辑。

### 2.1 Agent Loop 详解

你已经写过两个 Agent Loop 了。现在退一步，系统理解：

```text
感知 (Perception)  →  思考 (Thought)  →  行动 (Action)
       ↑                                      |
       |                                      ↓
       +———— 观察 (Observation) ←—————————————+
```

关键问题：

- **停止条件**：怎么判断任务完成了？（Finish、最大步数、异常退出）
- **错误恢复**：工具调用失败了怎么办？LLM 返回格式不对怎么办？
- **上下文膨胀**：每一步都往 history 里追加内容，越来越长怎么处理？
- **与 Workflow 的区别**：什么时候用 Agent Loop，什么时候用固定的 Workflow？

📖 已有文档：[docs/agent/第一章/智能体的感知与行动.md](agent/第一章/智能体的感知与行动.md)
📖 动手：给 `06_ReAct/agent.py` 加上"工具失败后自动重试一次"的逻辑

### 2.2 Tool Use 深入

你已经会定义和注册工具了。进一步：

- **工具描述工程**：怎么描述工具能让 LLM 更准确地选择？描述太简单 → 用错工具；描述太啰嗦 → 浪费 token
- **工具返回值设计**：返回字符串？JSON？错误信息怎么格式化？
- **工具粒度**：一个工具做一件事，还是一个工具做一组事？

📖 动手：在 `06_ReAct` 里加两个功能相近的工具（比如 `search_news` 和 `search_wiki`），看 LLM 怎么区分调用

### 2.3 Context 管理

上下文不是越长越好：

- **上下文窗口限制**：每个模型有最大 token 限制，超过了就截断或报错
- **信息密度**：拼进上下文的内容要精简，不要塞废话
- **裁剪策略**：保留最近的？保留最重要的？两者的权衡

📖 动手：在 Agent 循环里打印每一步的上下文长度，感受增长速度

### 2.4 Memory 管理

当上下文太长放不下怎么办？这就是 Memory 解决的问题：

| 策略 | 做法 | 效果 |
| ---- | ---- | ---- |
| **滑动窗口** | 只保留最近 N 轮对话 | 简单，丢失早期信息 |
| **摘要压缩** | 用 LLM 把历史对话总结成一段话 | 保留要点，损失细节 |
| **向量记忆** | 把所有历史存向量库，检索相关部分 | 灵活，实现复杂 |

📖 动手：给 Agent 加上滑动窗口（只保留最近 5 轮 Observation）

### 2.5 Reasoning & Planning

Agent 的"智能"来自 LLM 的推理和规划能力：

- **Reasoning（推理）**：LLM 如何通过 Thought 一步步推导答案
- **Planning（规划）**：LLM 如何把复杂任务拆成子任务——你在用 ReAct 时已经见到雏形了
- **延伸概念**：
  - CoT（Chain of Thought）：让 LLM "逐步思考"，提升推理质量
  - ToT（Tree of Thoughts）：多条推理路径并行探索，选最优

---

## 第三阶段：知识增强

> 目标：让 Agent 能基于外部知识回答问题，而不只是靠模型参数里的记忆。

### 核心思路

```text
你有很多文档 → 切片 → 向量化 → 存起来
用户问问题 → 搜索相关片段 → 拼进 Prompt → AI 回答
```

### 3.1 理解 Embedding

把文字变成向量（一串数字），语义相近的文字，向量也相近。

```text
"今天天气真好"  → [0.12, -0.34, 0.56, ...]
"天气非常不错"  → [0.13, -0.32, 0.54, ...]  ← 向量相近！
"编程语言有哪些" → [0.78, 0.21, -0.45, ...] ← 向量差很多
```

### 3.2 搭一个简单的 RAG

不用框架，纯 API 手写：

1. 把几篇文档切片
2. 用 Embedding 模型转成向量
3. 用户提问时，搜索最相关的片段
4. 把片段拼进 Prompt，让 AI 回答

📖 Python：学会文件读写（`open()` 读文档）

### 3.3 KV Cache（了解即可）

这是 LLM 推理引擎层面的优化——缓存已计算的 key-value 矩阵，避免重复计算。对使用者来说不需要操作，但知道它的存在能帮你理解"为什么长对话越来越慢"。

---

## 第四阶段：工程化

> 目标：理解 Agent 在生产环境中的工程化思路。

### 4.1 MCP（模型上下文协议）

把工具从 Agent 主程序解耦出来，变成标准的 MCP Server：

```text
之前：Agent 代码里直接定义工具函数
之后：Agent 代码 → MCP Client → MCP Server（独立的工具进程）
```

好处：工具可以用任何语言写、可以独立部署、可以复用。

📖 你已经在用 MCP 了——你的 `.mcp.json` 里配置了麦当劳 MCP Server，Claude Code 就是 MCP Client。

### 4.2 Workflow（工作流）

```text
Workflow ≠ Agent Loop

Agent Loop：LLM 自主决策 → 适合开放性任务
Workflow：固定流程图 → 适合确定性流程，省 token
```

把确定性流程固化成代码，减少 LLM 调用。适合：数据清洗流水线、固定格式的报表生成。

### 4.3 Skill（技能）

把常用能力（提示词 + 脚本 + 说明文档）打包，按需加载：

- 本质是"一个提示词模板 + 配套工具 + 使用说明"
- 你在 Claude Code 里用的 `/code-review`、`/deep-research` 就是 Skill

### 4.4 SubAgent 与 Multi-Agent

```text
SubAgent（子智能体）：
主 Agent 拆任务 → 分给子 Agent → 子 Agent 在自己的上下文里执行 → 只返回结果

Multi-Agent（多智能体）：
多个 Agent 并发运行 → 彼此通信/竞争/投票 → 协作完成复杂任务
```

**关键价值：上下文隔离** — 子 Agent 的中间过程不会污染主 Agent 的上下文。

📖 已有文档：[docs/agent/提问的AI回复/SubAgent与多Agent编排.md](agent/提问的AI回复/SubAgent与多Agent编排.md)

### 4.5 Prompt Engineering

系统化地设计和优化提示词，你的 `docs/提示工程/` 目录已经整理了六大原则：

1. 写出清晰的指令
2. 提供参考文本
3. 拆分复杂任务
4. 给模型时间"思考"
5. 使用外部工具
6. 系统地测试变更

📖 文档：[docs/提示工程/提示工程Prompt Engineering.md](提示工程/提示工程Prompt Engineering.md)

### 4.6 Context Engineering

比 Prompt Engineering 更高一层的视角——不只是写 prompt 文本，而是设计整个上下文的结构：

- System Prompt 放什么？User Message 放什么？
- 工具定义怎么格式化？Observation 用什么格式回传？
- 什么时候裁剪？什么时候总结？

这其实就是你在 `04_hello_agent` 和 `06_ReAct` 里一直在做的事——设计 Agent 的输入结构。

### 4.7 Harness Engineering

Agent 运行时框架的设计——这是最深的一层：

- Agent Loop 的实现（你已经做了）
- 错误处理和恢复机制
- 日志和可观测性
- 速率限制和 token 预算管理

当你从"写一个 Agent"变成"写一个 Agent 框架"时，这些就是核心问题。

---

## Python 学习（穿插在各阶段）

不用系统学，遇到不懂的查速查手册：

| 文档 | 什么时候看 |
| ---- | ---------- |
| [python与java对比](python/python与java对比.md) | 刚接触 Python 时 |
| [python新手指南](python/python新手指南.md) | 第一周 |
| [数据结构与类型](python/数据结构与类型.md) | 解析 API 返回值时 |
| [控制流与函数](python/控制流与函数.md) | 写 Agent 逻辑时 |
| [模块与导入](python/模块与导入.md) | 组织代码文件时 |
| [依赖管理](python/依赖管理.md) | 安装包报错时 |
| [全局python与虚拟环境](python/全局python与虚拟环境.md) | 环境搞混时 |

---

## 学习资源

| 资源 | 说明 |
| ---- | ---- |
| [modelcontextprotocol.io](https://modelcontextprotocol.io) | MCP 协议官方文档 |
| Anthropic "Building effective agents" | Agent 设计思路 |
| OpenAI / Anthropic 官方 quickstart | API 入门 |
| Claude Code | 你日常使用的 Agent 本身就是最好的学习对象 |

---

## 一句话总结

> 概念够用就行 → 跑通 Agent → 玩起来 → 深入机制 → RAG → 工程化

你现在在「第二阶段」——Agent 核心机制。你已经跑通了两个 ReAct Agent，接下来不是学新东西，而是**把已经跑通的东西理解透**：Agent Loop 为什么这样设计？Context 怎么管理？Memory 怎么加？这些问题的答案，就藏在你已经写过的代码里。
