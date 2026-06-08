# AI Agent 学习路径

由浅入深，从概念理解到动手实战。

---

## 第一阶段：动手跑通一个最小 Agent

> 目标：亲手从零搭一个能搜索+回答的 Agent，不依赖框架。

停留在"概念理解"层面不是长久之计，最重要的下一步是 **写代码跑通一个完整循环**。

### 1. 直接调 API

用 OpenAI 或 Anthropic 的 SDK，写一个最简单的对话程序，体会无状态调用 + 手动拼上下文的过程。

### 2. 加上 Function Calling

让 LLM 能调用一个你自己写的函数（比如查天气），理解 tool_use 的请求/响应格式。

### 3. 接一个 MCP Server

用现成的 MCP Server（比如文件系统、搜索），用 MCP Client 调用它，感受协议解耦的效果。

---

## 第二阶段：理解 Agent Loop

> 目标：搞清楚 Agent 的决策循环是怎么运作的。

```text
用户输入 → LLM 思考 → 需要工具？→ 调用工具 → 结果返回 LLM → 继续思考 → …→ 最终回答
```

这个循环里有几个关键问题值得深入：

| 问题 | 说明 |
|------|------|
| 什么时候停下来？ | 终止条件的设计 |
| 工具调用失败了怎么办？ | 错误处理与重试策略 |
| 循环太多次怎么限制？ | 最大轮次保护 |
| 多个工具怎么选？ | 工具描述的质量直接影响 LLM 的选择 |

### 推荐阅读

直接读一个轻量 Agent 框架的源码：

- **Claude Agent SDK**（Anthropic 官方）
- **OpenAI Agents SDK**
- 或者干脆自己用纯 API 写一个

---

## 第三阶段：RAG 实战

> 目标：让 LLM 能基于私有知识回答问题。

### 核心流程

```text
文档 → 切片 → 向量化 → 存储
                        ↓
用户问题 → 向量检索 → 相关片段 → 拼入 Prompt → LLM 生成回答
```

### 四个关键环节

| 环节 | 要点 |
|------|------|
| 文档切片 | 怎么切、切多大、有没有重叠 |
| 向量化 | Embedding 模型的选择 |
| 检索 | 语义搜索 vs 混合搜索 |
| 拼入 Prompt | 检索到多少内容、怎么组织 |

### 学习建议

可以用 LangChain 或 LlamaIndex 快速搭一个，但建议先用纯 API 手写一遍，理解每一步在干什么。

---

## 第四阶段：Workflow 与 Skill

> 目标：理解 Agent 的工程化思路。

### Workflow（工作流）

把确定性流程固化，减少 LLM 调用，节省 token。适合流程固定、不需要 Agent 自主决策的场景。

### Skill（技能）

把常用能力（提示词 + 脚本 + 说明文档）打包，按需加载，避免每次重复写提示词。

### 学习建议

可以看看 **Dify**、**Coze（扣子）** 这类平台，理解可视化编排的思路，然后思考：

- 什么场景适合用 Workflow？
- 什么场景必须让 Agent 自主决策？

---

## 学习资源

| 阶段 | 资源 |
|------|------|
| API 入门 | OpenAI / Anthropic 官方文档的 quickstart |
| Function Calling | 官方文档的 tool_use / function_calling 章节 |
| MCP 协议 | [modelcontextprotocol.io](https://modelcontextprotocol.io) |
| Agent 原理 | Anthropic 的 "Building effective agents" 博文 |
| RAG 实战 | LlamaIndex 官方教程 |
| 框架对比 | LangChain vs 自写的优缺点，自己体会 |

---

## 项目结构

```text
myAgent/
├── README.md               # 原始学习笔记
├── README-AI审阅版.md       # AI 核对标注版
├── docs/                    # 学习过程中的概念文档
│   └── learning-path.md     # 本文件：学习路径规划
└── demos/                   # Agent Demo 项目代码
```

---

## 一句话总结

**概念 → 手写最小 Agent → 理解循环 → RAG → 工程化**

最大的瓶颈不是"还缺什么概念"，而是 **还没动手写代码**。从第一阶段开始，写一个能调用工具的最小 Agent，遇到问题再回来查概念，理解会深很多。
