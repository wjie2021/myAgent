# 🤖 AI Agent 学习项目

从零开始学习 AI Agent 开发的个人学习项目。

## 📚 学习路径

### 阶段 1：基础入门 ✅

- [x] Python 环境搭建
- [x] API 调用基础（单轮/多轮对话）
- [x] Function Calling（工具调用）
- [x] 模块化代码重构
- [x] ReAct 模式 Agent

### 阶段 2：Agent 核心机制

- [ ] Agent Loop 详解
- [ ] Context / Memory 管理
- [ ] RAG（检索增强生成）

### 阶段 3：工程化实践

- [ ] Workflow 编排
- [ ] Skill 系统
- [ ] SubAgent 协作

## 📁 项目结构

```text
myAgent/
├── examples/                   # 代码示例（跟着教程写的）
│   ├── 01_hello/              # 入门程序
│   ├── 02_chatbot/            # 聊天机器人系列
│   ├── 03_function_calling/   # Function Calling 系列
│   └── 04_hello_agent/        # 第一个 Agent
│
├── docs/                       # 学习文档
│   ├── learning-path.md       # 学习路线图
│   ├── notes/                 # 学习笔记
│   └── python/                # Python 基础
│
├── requirements.txt            # 依赖包
└── .gitignore                  # Git 忽略规则
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
# 编辑 .env 填入你的 API Key

# 4. 运行示例
python examples/01_hello/echo.py
```

## 🛠️ 技术栈

- **语言**: Python 3.10+
- **AI SDK**: Anthropic SDK / OpenAI SDK
- **API**: MiMo（小米大模型，兼容 OpenAI 接口）
- **搜索**: Tavily API

## 📖 学习笔记

详细的学习笔记和概念理解请查看 [docs/](docs/) 目录。

## 🎯 核心概念理解

### Agent 是什么？

```text
用户 ──"今天有哪些新闻"──> Agent ──> LLM
                            LLM ──"需要上网查"──> Agent
                                      Agent ──上网搜索──> 拿到结果
                            Agent ──搜索结果──> LLM
                            LLM ──整理好的新闻──> Agent
用户 <──"今天的新闻是……"── Agent
```

### 关键组件

| 组件 | 作用 |
| ---- | ---- |
| **LLM** | 大语言模型，无状态的函数调用（输入 → 输出） |
| **Prompt** | 提示词，包含背景信息和最终指示 |
| **Context** | 上下文，多轮对话是把历史消息拼进 prompt 模拟出来的 |
| **Memory** | 记忆，对上下文进行总结压缩 |
| **Function Calling** | Agent 和 LLM 之间关于工具调用约定的格式 |
| **MCP** | 模型上下文协议，把工具从 Agent 主程序里解耦出来 |
| **Workflow** | 固定流程，不需要 Agent 规划 |
| **Skill** | 提示词 + 脚本 + 说明文档 |
| **SubAgent** | 上下文隔离，子任务独立执行 |

---

> 💡 这是一个学习项目，代码中包含大量注释，方便回顾和理解。
