# docs — 学习文档目录

## 目录结构

```text
docs/
├── README.md                    ← 本文件：目录索引
├── learning-path.md             ← 学习路径规划
│
├── python/                      ← Python 速查
│   ├── python与java对比.md      ← 程序结构对比
│   ├── 依赖管理.md              ← pip 与 requirements.txt
│   ├── 全局python与虚拟环境.md  ← venv 使用
│   ├── 数据结构速查.md          ← list/dict/json
│   └── 常见语法速查.md          ← if/for/try/import
│
├── agent/                       ← Agent 核心概念
│   ├── ReAct模式与输出格式.md   ← ReAct 范式详解
│   └── 系统提示词与上下文.md    ← LLM 输入的三层结构
│
├── notes/                       ← 学习笔记
│   ├── day01-api-params.md      ← API 入参与出参
│   ├── day01-setup.md           ← 环境搭建
│   ├── day01-function-calling.md          ← Function Calling 详解
│   └── day01-function-calling-summary.md  ← Function Calling 速查
│
└── me/                          ← 个人资料
    └── me.md
```

## 阅读建议

**Agent 入门路线：**

1. [学习路径规划](learning-path.md) — 整体方向
2. [系统提示词与上下文](agent/系统提示词与上下文.md) — 理解 LLM 输入结构
3. [ReAct 模式与输出格式](agent/ReAct模式与输出格式.md) — 理解 Agent 核心范式
4. [Function Calling 详解](notes/day01-function-calling.md) — 理解工具调用机制

**Python 速查（遇到不懂的来查）：**

1. [Python 与 Java 对比](python/python与java对比.md) — 刚接触时看
2. [数据结构速查](python/数据结构速查.md) — 解析 API 返回值时
3. [常见语法速查](python/常见语法速查.md) — 看不懂语法时
4. [依赖管理](python/依赖管理.md) — 安装包报错时
