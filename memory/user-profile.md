---
name: user-profile
description: 用户背景、技术水平和学习进度
metadata: 
  node_type: memory
  type: user
  originSessionId: be9c9988-0f0b-4392-a7d4-864f72cd5c21
---

## 职业背景

- Java 程序员，有后端开发经验
- 不打算系统学习 Python，只要能看懂、能写 demo 就行

## 当前学习进度（2026-06-08）

### 已完成

- [x] 理解了 AI Agent 的核心概念（LLM、Prompt、Context、Memory、RAG、Function Calling、MCP、Skill、Workflow、SubAgent）
- [x] 整理了学习笔记到 README.md，并有 AI 审阅标注版
- [x] 制定了学习路径（docs/learning-path.md）
- [x] 确定了使用 MiMo API（兼容 Anthropic SDK，模型 mimo-v2.5-pro）
- [x] 搭建了第一个单次调用 demo（demos/chatbot/chatbot.py）
- [x] 理解了 API 入参和出参结构（docs/chatbot/day01_api_params.md）
- [x] 实现了多轮对话聊天机器人（demos/chatbot/chatbot_while.py），通过 history 列表保存上下文
- [x] 学习了 Function Calling 概念，跑通了基础 demo 和终端工具 demo

### 进行中

- [ ] 深入理解 Function Calling 细节（官方文档、边界情况）

### 待开始

- [ ] 接入 MCP Server
- [ ] RAG 实战

## 技术栈

- Python（不系统学习，够用就行）
- Anthropic SDK（`pip install anthropic`）
- MiMo API：`https://api.xiaomimimo.com/anthropic`
- API Key 已配置，环境变量 `MIMO_API_KEY`

## 踩过的坑

| 问题 | 原因 | 解决 |
|------|------|------|
| SSL 连接失败 | base_url 多写了 `/v1/messages` | 只填到 `/anthropic` |
| GBK 编码报错 | Windows 终端默认 GBK | 加 `PYTHONIOENCODING=utf-8` |
| ThinkingBlock 无 text 属性 | 返回含思考块 | 判断 `block.type == "text"` |

## 项目结构

```text
myAgent/
├── README.md                 # 学习笔记
├── README-AI审阅版.md         # AI 核对版
├── docs/
│   ├── learning-path.md      # 学习路径规划
│   └── chatbot/
│       └── day01_api_params.md  # API 参数记录
└── demos/
    ├── 01_echo.py            # 最简输入输出
    ├── chatbot/
    │   ├── chatbot.py        # 单次 API 调用 demo
    │   └── chatbot_while.py  # 多轮对话（带上下文）
    └── function_calling/
        ├── function_calling_basic.py    # Function Calling 基础（计算器+天气）
        └── function_calling_terminal.py # Function Calling 终端工具
```
