# 🤖 AI Agent 学习项目

从零开始学习 AI Agent 开发的个人学习项目。

## 目标

熟悉 LLM 以及 Agent 基本机制及其技术原理，包括 LLM API、KV Cache、Agent Loop、Tool Use、Reasoning、Planning、Skills、MCP、Memory、Subagent、Multi-Agent 等相关知识。对 Prompt Engineering、Context Engineering、Harness Engineering 等课题有深入的理解。

## 📚 学习路径

### 阶段 1：基础入门 ✅

> 目标：跑通 API 调用、工具调用、第一个 ReAct Agent。建立感性认识。

- [x] **Python 环境搭建** — venv、pip、环境变量配置
- [x] **API 调用基础** — 单轮对话 → 多轮对话（手动拼接 history）
- [x] **Function Calling** — 工具定义、参数解析、结果回传
- [x] **模块化重构** — 将单文件拆分为 client / executor / tools / main
- [x] **ReAct 模式 Agent** — `04_hello_agent`（旅行助手）+ `06_ReAct`（搜索引擎 Agent）

**对应代码：** `examples/01_hello/` → `02_chatbot/` → `03_function_calling/` → `04_hello_agent/` → `06_ReAct/`

**这个阶段你学到了：**

- LLM 是无状态函数，上下文靠手动拼接 history 模拟
- Function Calling 的本质：描述工具 → LLM 决定调用 → 你执行 → 结果传回
- ReAct 不是魔法，只是一个提示词格式约定（`Thought: ... Action: ... Observation: ...`）
- Agent = LLM + 工具 + 循环

---

### 阶段 2：Agent 核心机制 🔄

> 目标：深入理解 Agent 的运行时行为和控制逻辑。

- [ ] **Agent Loop 详解** — 感知→思考→行动的循环本质；停止条件、步数限制、异常处理
  - 已有材料：[docs/agent/第一章/智能体的感知与行动.md](docs/agent/第一章/智能体的感知与行动.md)
  - 对应代码：`04_hello_agent/main.py` 的 for 循环、`06_ReAct/agent.py` 的 while 循环
- [ ] **Tool Use 深入** — 工具注册模式、工具描述工程、错误处理与重试
  - 对应代码：`06_ReAct/tools.py` 的 `ToolExecutor` 类
- [ ] **Context 管理** — 上下文窗口限制、信息密度、什么时候该裁剪
- [ ] **Memory 管理** — 摘要压缩、滑动窗口、向量记忆的基本思路
- [ ] **Reasoning & Planning** — LLM 如何"分步思考"；ReAct 本身就是一种推理框架
  - 延伸：CoT（思维链）、ToT（思维树）的基本概念

**关键理解：** Agent Loop 不是神秘的"智能"，而是一个确定性的 while 循环——LLM 负责"想"，代码负责"执行"和"拼上下文"。你已经在 `06_ReAct/agent.py` 里写过完整的 Agent Loop 了。

---

### 阶段 3：知识增强

> 目标：让 Agent 能基于外部知识回答问题，而不只是靠模型参数里的记忆。

- [ ] **Embedding 理解** — 文字→向量的原理，语义相近=向量相近
- [ ] **向量数据库** — FAISS / Chroma 的基本使用
- [ ] **RAG 实战** — 文档切片 → 向量化 → 检索 → 拼入 Prompt → LLM 回答
- [ ] **KV Cache** — 理解 LLM 推理时的缓存机制（偏底层，了解即可）

**对应材料：** `docs/notes/transformer-intro.md`（Transformer 基础）、`examples/05_transformer/`（位置编码等组件实现）

---

### 阶段 4：工程化实践

> 目标：理解 Agent 在生产环境中的工程化思路。

- [ ] **MCP（模型上下文协议）** — 把工具从 Agent 主程序解耦，标准化 tool/resource/prompt 接口
  - 项目里已有 `.mcp.json`，Claude Code 本身就是 MCP 的最佳参考实现
- [ ] **Workflow 编排** — 确定性流程固化，减少 LLM 调用次数
- [ ] **Skill 系统** — 将 提示词 + 脚本 + 文档 打包为可复用能力
- [ ] **SubAgent 协作** — 上下文隔离，子任务独立执行
- [ ] **Multi-Agent** — 多 Agent 间的通信、分工与协作模式
- [ ] **Prompt Engineering** — 系统化地设计和优化提示词
  - 已有材料：[docs/提示工程/提示工程Prompt Engineering.md](docs/提示工程/提示工程Prompt Engineering.md)
- [ ] **Context Engineering** — 不只是写 prompt，而是设计整个上下文结构
- [ ] **Harness Engineering** — Agent 运行时框架的设计（循环控制、错误恢复、日志、可观测性）

---

## 📁 项目结构

```text
myAgent/
├── examples/                          # 代码示例
│   ├── 01_hello/                      # 入门：最简输入输出
│   │   └── echo.py
│   ├── 02_chatbot/                    # 聊天机器人系列
│   │   ├── chatbot.py                 #   单次 API 调用
│   │   ├── chatbot_while.py           #   多轮对话（手动拼上下文）
│   │   └── chatbot_with_tools.py      #   带工具调用的聊天
│   ├── 03_function_calling/           # Function Calling 系列
│   │   ├── function_calling_basic.py  #   基础示例（计算器+天气）
│   │   ├── function_calling_terminal.py # 终端命令执行
│   │   └── modular/                   #   模块化重构版
│   │       ├── main.py                #     主程序入口
│   │       ├── client.py              #     LLM 客户端
│   │       ├── executor.py            #     工具执行器
│   │       └── tools.py               #     工具函数注册
│   ├── 04_hello_agent/                # 第一个 ReAct Agent（旅行助手）
│   │   ├── main.py                    #   Agent 主循环
│   │   ├── client.py                  #   OpenAI 兼容客户端
│   │   ├── config.py                  #   配置管理
│   │   ├── prompts/agent.md           #   System Prompt
│   │   └── tools/                     #   工具模块
│   │       ├── weather.py             #     天气查询
│   │       └── search.py              #     景点搜索
│   ├── 05_transformer/                # Transformer 架构学习
│   │   └── transformerDemo.py         #   位置编码等组件实现（PyTorch）
│   └── 06_ReAct/                      # 更干净的 ReAct 实现（搜索引擎 Agent）
│       ├── agent.py                   #   ReActAgent 类（标准 while 循环）
│       ├── llm.py                     #   流式 LLM 客户端
│       └── tools.py                   #   ToolExecutor + SerpApi 搜索
│
├── docs/                              # 学习文档
│   ├── README.md                      # 文档目录索引
│   ├── learning-path.md               # 学习路径规划
│   ├── python/                        # Python 速查手册（Java 程序员视角）
│   │   ├── python与java对比.md
│   │   ├── python新手指南.md
│   │   ├── 数据结构与类型.md
│   │   ├── 控制流与函数.md
│   │   ├── 模块与导入.md
│   │   ├── 依赖管理.md
│   │   └── 全局python与虚拟环境.md
│   ├── agent/                         # Agent 核心概念
│   │   ├── README.md
│   │   ├── 第一章/                    # Agent 基础理论
│   │   │   ├── 智能体的感知与行动.md  # Agent Loop：感知→思考→行动
│   │   │   ├── 第一章习题.md
│   │   │   ├── 习题练习.md
│   │   │   └── 习题解析.md
│   │   └── 提问的AI回复/             # 概念问答
│   │       ├── 系统提示词与上下文.md
│   │       ├── ReAct模式与输出格式.md
│   │       └── SubAgent与多Agent编排.md
│   ├── 提示工程/                      # Prompt Engineering
│   │   └── 提示工程Prompt Engineering.md
│   ├── notes/                         # 学习笔记
│   │   ├── day01-setup.md             #   环境搭建记录
│   │   ├── day01-api-params.md        #   API 入参/出参结构
│   │   ├── day01-function-calling.md  #   Function Calling 详解
│   │   ├── day01-function-calling-summary.md  # Function Calling 速查
│   │   ├── transformer-intro.md       #   Transformer 入门
│   │   └── 前端技术体系概览.md
│   ├── me/                            # 个人资料
│   └── 部门AI规划/                    # 工作相关
│
├── memory/                            # 项目记忆（git 管理，多设备同步）
│   ├── MEMORY.md                      #   记忆索引
│   ├── user-profile.md                #   用户背景与学习进度
│   ├── learning-path-design.md        #   学习路径设计理念
│   ├── python-comment-style.md        #   Python 注释风格偏好
│   ├── python-learning-style.md       #   Python 学习方式
│   ├── react-pattern-insight.md       #   ReAct 模式理解
│   ├── subagent-concept-intro.md      #   SubAgent 概念
│   └── honesty-over-sycophancy.md     #   诚实优于迎合
│
├── CLAUDE.md                          # Claude Code 项目配置
├── requirements.txt                   # Python 依赖
├── .mcp.json                          # MCP 服务器配置
└── .gitignore
```

## 🚀 快速开始

```bash
# 1. 创建虚拟环境
python -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows

# 2. 安装依赖
pip install -r requirements.txt

# 3. 配置环境变量
cp .env.example .env
# 编辑 .env 填入 API Key

# 4. 运行示例
python examples/01_hello/echo.py                # 最简程序
python examples/06_ReAct/agent.py               # ReAct Agent（搜索）
python examples/04_hello_agent/main.py          # ReAct Agent（旅行助手）
```

## 🛠️ 技术栈

| 类别 | 技术 | 用途 |
| ---- | ---- | ---- |
| **语言** | Python 3.10+ | 主要开发语言 |
| **AI SDK** | Anthropic SDK / OpenAI SDK | LLM API 调用 |
| **API** | MiMo（小米大模型） | 兼容 OpenAI 接口的大模型服务 |
| **搜索** | SerpAPI（Google 搜索） | Agent 的联网搜索工具 |
| **深度学习** | PyTorch | Transformer 学习（`05_transformer`） |
| **Agent 框架** | Claude Code | 日常使用的 AI 编程助手 |

## 🎯 核心概念速查

### Agent 是什么？

```text
用户 ──"今天有哪些新闻"──> Agent ──> LLM
                            LLM ──"需要上网查"──> Agent
                                      Agent ──上网搜索──> 拿到结果
                            Agent ──搜索结果──> LLM
                            LLM ──整理好的新闻──> Agent
用户 <──"今天的新闻是……"── Agent
```

本质：**Agent = LLM（思考）+ 工具（执行）+ 循环（持续行动直到完成）**

### Agent Loop（智能体循环）

```text
感知 (Perception)  →  思考 (Thought)  →  行动 (Action)
       ↑                                      |
       |                                      ↓
       +———— 观察 (Observation) ←—————————————+
```

你已经实现过的循环：

- `04_hello_agent/main.py` — for 循环，手动拼接 Thought/Action/Observation
- `06_ReAct/agent.py` — while 循环，`ReActAgent` 类封装，解析 → 执行 → 记录历史

### 概念全景

| 概念 | 一句话解释 | 你在哪里见过 |
| ---- | ---------- | ------------- |
| **LLM** | 无状态的函数：输入文字 → 输出文字 | `02_chatbot/chatbot.py` — 单次 API 调用 |
| **Prompt** | 发给 LLM 的那段文字 | 每个示例的 messages 参数 |
| **System Prompt** | 给 LLM 的"岗位说明书"，全程不变 | `04_hello_agent/prompts/agent.md` |
| **Context** | 对话历史拼成的完整输入 | `02_chatbot/chatbot_while.py` — history 列表 |
| **Token** | LLM 计费单位，≈1 个汉字 ≈1-2 token | API 返回的 `usage` 字段 |
| **Function Calling** | LLM 和外部工具的调用约定 | `03_function_calling/` 全部示例 |
| **ReAct** | Thought → Action → Observation 的提示词格式 | `04_hello_agent/` + `06_ReAct/` |
| **Agent Loop** | 感知→思考→行动→观察的 while 循环 | `06_ReAct/agent.py` — `run()` 方法 |
| **Tool Use** | Agent 选择并调用外部工具的能力 | `06_ReAct/tools.py` — `ToolExecutor` |
| **Context Engineering** | 设计上下文结构（不只是写 prompt） | System Prompt + history 拼接策略 |
| **Memory** | 对长上下文的压缩和总结 | 尚未实现，阶段 2 目标 |
| **Reasoning** | LLM 的分步推理能力 | ReAct 的 `Thought:` 字段 |
| **Planning** | 将复杂任务分解为子任务 | Agent 自动规划工具调用顺序 |
| **RAG** | 检索外部文档 → 拼入 Prompt → 回答 | 阶段 3 目标 |
| **Embedding** | 把文字变成向量，语义相近=向量相近 | RAG 的前置知识 |
| **KV Cache** | LLM 推理时缓存的 key-value 矩阵 | 偏底层，了解即可 |
| **MCP** | 模型上下文协议，工具/资源/Prompt 标准化 | `.mcp.json`，Claude Code 实践 |
| **Workflow** | 确定性流程，不需要 Agent 自主决策 | 阶段 4 目标 |
| **Skill** | 提示词 + 脚本 + 说明文档的打包 | 阶段 4 目标 |
| **SubAgent** | 上下文隔离的子任务执行单元 | 阶段 4 目标 |
| **Multi-Agent** | 多 Agent 分工协作 | 阶段 4 目标 |
| **Prompt Engineering** | 系统化设计提示词的方法论 | `docs/提示工程/` |
| **Harness Engineering** | Agent 运行时框架的设计 | 循环控制、错误恢复、可观测性 |

## 📖 阅读指南

**想快速了解 Agent？** 读：

1. [学习路径规划](docs/learning-path.md)
2. [系统提示词与上下文](docs/agent/提问的AI回复/系统提示词与上下文.md)
3. [ReAct 模式](docs/agent/提问的AI回复/ReAct模式与输出格式.md)
4. [Agent Loop（感知与行动）](docs/agent/第一章/智能体的感知与行动.md)

**想跟着代码学？** 按顺序跑：

1. `01_hello/echo.py` → 感受"调用 API 就是函数调用"
2. `02_chatbot/chatbot_while.py` → 理解 context 是手动拼接的
3. `03_function_calling/modular/main.py` → 理解工具调用的完整链路
4. `06_ReAct/agent.py` → 理解 Agent Loop 的完整实现

**想查 Python 语法？** → [docs/python/](docs/python/)（Java 程序员视角，按需查阅）

---

> 💡 这是一个学习项目，代码中包含大量注释，方便回顾和理解。
> 学习理念：**概念够用就行 → 跑通 Agent → 玩起来 → 加功能 → RAG → 工程化**
