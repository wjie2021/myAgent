# ReAct 模式与输出格式

> Agent 开发中最经典的范式：让模型"说出"思考过程，而不是只输出结果。
Reasoning + Acting = ReAct

论文标题：ReAct: Synergizing Reasoning and Acting in Language Models（2022）

核心思想：让模型先想（Thought）再做（Action），而不是直接输出答案。
## 核心概念

### 大模型的两种"思考"

```text
1. 原生思考（黑盒，你看不到）
   输入 → [模型内部推理] → 输出

2. ReAct 的 Thought（输出文本，你能看到）
   输入 → [模型] → 输出 "Thought: 我需要查天气"  ← 这只是普通文本
```

**ReAct 中的 Thought 不是模型的内部推理**，而是我们强迫模型按照格式输出的一段文字。模型并不真的在"思考"，它只是把推理过程以文本形式"说出来"。

## 为什么要强制输出 Thought？

不强制输出 Thought：

```text
用户：查北京天气
模型：get_weather(city="北京")    ← 直接输出 Action，你不知道它为什么这么选
```

强制输出 Thought：

```text
用户：查北京天气
模型：Thought: 用户想查天气，我需要调用天气工具    ← 能看到推理过程
      Action: get_weather(city="北京")
```

好处：**可观察、可调试**，你能理解 Agent 每一步的决策逻辑。

## ReAct 解决了什么问题？

2022 年之前，LLM 有两个主流用法：

```text
方式一：纯推理（Chain of Thought）
  问：北京今天天气怎么样？
  答：我不知道，因为我的知识截止到2023年...  ← 只能"想"，不能"做"

方式二：纯行动（直接调工具）
  问：北京今天天气怎么样？
  答：get_weather(city="北京")               ← 只能"做"，不会"想"
```

**ReAct 的创新：把"想"和"做"交替进行。**

```text
Thought: 用户问实时天气，我的知识里没有，需要调工具  ← 想
Action: get_weather(city="北京")                      ← 做
Observation: 晴天 31°C                               ← 看结果
Thought: 拿到天气了，可以回答用户了                    ← 再想
Action: Finish[北京今天晴天31°C]                      ← 做
```

## 论文的核心发现

论文《ReAct: Synergizing Reasoning and Acting in Language Models》（2022）做了对比实验：

| 方法 | HotpotQA（多跳问答） | 说明 |
|------|---------------------|------|
| 纯推理 | 29.4% | 只想不做，幻觉严重 |
| 纯行动 | 25.4% | 只做不想，盲目调工具 |
| **ReAct** | **40.7%** | 想做交替，效果最好 |

> ⚠️ 以上数据来自论文原文，建议查阅原论文核实具体数字。

## 为什么叫 ReAct？

```text
Re  = Reasoning（推理）  → Thought
Act = Acting（行动）     → Action

ReAct = 推理和行动的交替循环
```

## ReAct 的完整流程

```text
┌──────────────────────────────────────────────┐
│                  用户输入                      │
└──────────────────┬───────────────────────────┘
                   ▼
┌──────────────────────────────────────────────┐
│  Thought: 分析当前状态，决定下一步             │  ← 推理
└──────────────────┬───────────────────────────┘
                   ▼
┌──────────────────────────────────────────────┐
│  Action: 执行具体操作（调工具/给出答案）        │  ← 行动
└──────────────────┬───────────────────────────┘
                   ▼
┌──────────────────────────────────────────────┐
│  Observation: 获取行动结果                     │  ← 观察
└──────────────────┬───────────────────────────┘
                   ▼
              是否完成？──否──→ 回到 Thought
                   │
                  是
                   ▼
┌──────────────────────────────────────────────┐
│  Action: Finish[最终答案]                     │
└──────────────────────────────────────────────┘
```

## ReAct 的本质

说白了，ReAct 就是**一套提示词模板**：

```markdown
# 系统提示词

你是一个智能助手，请按以下格式回答：

Thought: [分析当前情况，决定下一步]
Action: [调用工具或给出最终答案]

可用工具：
- get_weather(city): 查询天气
- get_attraction(city, weather): 查询景点
```

模型看到这个提示词，就会按照 Thought → Action 的格式输出。然后你的程序解析输出，执行工具，把结果追加到上下文，再让模型继续。

**没有任何魔法，就是提示词工程。**

## 系统提示词中的格式要求

```markdown
# 输出格式要求:
你的每次回复必须严格遵循以下格式：

Thought: [你的思考过程和下一步计划]
Action: [你要执行的具体行动]
```

这不是行业规范（没有官方标准），而是**约定俗成的工程实践**。不同框架的格式略有差异，但核心思想一致：让模型输出结构化的推理过程。

## ReAct 的局限性

```text
1. 依赖文本解析（早期实现）
   早期实现用正则提取 "Thought: ... Action: ..."
   如果模型输出格式不对，解析就失败
   现代实现已改用 Function Calling，解决了这个问题

2. 模型可能"不听话"
   模型可能输出多余的 Thought-Action，或格式不规范
   本项目的 main.py 第50行就是在处理这个问题

3. 效率问题
   每次循环都要调用一次 LLM，慢且贵

4. 规划能力有限
   ReAct 是"走一步看一步"，不会提前规划多步
   复杂任务可能需要 Plan-and-Execute 等模式辅助
```

## 市面主流 Agent 范式对比

| 范式 | 核心思想 | 特点 | 代表 |
|------|----------|------|------|
| ReAct | Thought → Action → Observation 循环 | 最经典，可调试 | LangChain、本项目 |
| Chain of Thought | 只输出推理，不调工具 | 适合纯推理任务 | o1、Claude Extended Thinking |
| Plan-and-Execute | 先规划步骤，再逐步执行 | 适合复杂任务 | BabyAGI |

## 重要概念：ReAct 与 Function Calling 的关系

**这是两个不同层次的概念，不是并列关系：**

```text
ReAct = 设计范式（Agent 如何组织思考和行动）
         ↓
         Action 用什么格式输出？
         ├─ 早期方式：正则解析文本（本项目用的）
         └─ 现代方式：Function Calling（结构化 JSON）
```

| 概念 | 层次 | 解决什么问题 |
|------|------|-------------|
| ReAct | 设计范式 | Agent **如何组织**思考和行动的循环 |
| Function Calling | 协议/机制 | 模型**如何格式化**工具调用的输出 |

**它们是组合关系，不是竞争关系：**

```text
# ReAct + 正则解析（早期方式）
模型输出: "Thought: 需要查天气 Action: get_weather(北京)"
程序用正则提取 Action → 执行

# ReAct + Function Calling（现代方式）
模型输出: { "thought": "需要查天气", "function_call": {"name": "get_weather", "args": {"city": "北京"}} }
程序直接解析 JSON → 执行
```

现代 Agent 框架通常是 **ReAct 范式 + Function Calling 实现**，两者结合使用。

## ReAct vs 原生思考

| | ReAct 的 Thought | 原生思考（Extended Thinking） |
|--|------------------|------------------------------|
| 本质 | 输出的文本 | 模型内部的推理过程 |
| 可见性 | 完全可见 | 通常不可见（或部分可见） |
| 目的 | 让 Agent 决策可调试 | 提升模型推理能力 |
| 控制 | 通过系统提示词控制格式 | 模型自主决定 |
| 例子 | 本项目的 agent.md | Claude Extended Thinking、o1 |

## ReAct 的演进

```text
2022  ReAct 论文发表，提出 Thought-Action-Observation 循环
  ↓
2023  LangChain 等框架内置 ReAct，普及 Agent 开发
  ↓
2023  Function Calling 出现（OpenAI）
  ↓     模型直接输出 JSON，替代正则解析
  ↓
2024  Claude Tool Use / GPT Function Calling 成熟
  ↓     ReAct 范式 + Function Calling 成为主流组合
  ↓
2025  现代 Agent 框架
      ReAct 范式依然广泛使用
      实现方式从正则解析迁移到 Function Calling
      但 ReAct 正则解析仍是学习 Agent 的最佳入门
```

## 总结

- ReAct 中的 Thought 是**输出文本**，不是模型内部推理
- 强制输出 Thought 的目的是**可观察、可调试**
- ReAct 的本质就是**一套提示词模板**，没有魔法
- ReAct 是行业标准 Agent **范式**，但不是唯一选择
- Function Calling 是工具调用的**协议**，不是 ReAct 的替代品
- 现代 Agent 通常是 **ReAct 范式 + Function Calling 实现**的组合
