---
name: subagent-concept-intro
description: SubAgent 概念了解——暂不深入，先学好单 Agent
metadata: 
  type: project
---

2026-06-16 学习了 SubAgent 概念：

- 本质是"派小弟干活"，主 Agent 把任务拆分给多个 SubAgent 并行执行
- 用途：并行加速、突破上下文限制、独立视角避免干扰
- 管理方式：任务分解 + 并行调度 + 结果汇总
- 技术实现：asyncio.gather() 并行调用

**当前决策：** 先不深入多 Agent 编排，优先把单 Agent 基础打牢（MCP、RAG）。

**Why:** 用户认为单 Agent 理解还不够深刻，多 Agent 是建立在单 Agent 基础上的。

**How to apply:** 等用户完成 MCP 和 RAG 学习后，再引导实践多 Agent 编排。

相关文档：[[learning-path-design]]，[SubAgent与多Agent编排.md](../docs/agent/提问的AI回复/SubAgent与多Agent编排.md)
