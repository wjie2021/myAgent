---
name: learning-path-design
description: 学习路径设计理念——平滑、概念够用就行、每个阶段都要动手
metadata: 
  node_type: memory
  type: project
  originSessionId: b93ce847-74e9-4d60-bc5a-959af864f29a
---

用户对学习路径的要求：

1. **平滑推进**：不要跳跃，每个阶段都要有动手环节
2. **概念够用就行**：知道"是什么"就够了，不需要深入底层原理
   - 例：知道大模型是无状态函数即可，不需要了解底层原理
   - 例：知道 ReAct 是提示词格式约定即可，不需要读论文
3. **兴趣驱动**：纯兴趣学习，没有强制要求
4. **Python 穿插学习**：不单独学 Python，在 Agent 开发中自然学习

当前学习路径：
- 第零阶段：基本概念（大模型、Prompt、System Prompt、Context、Token、Function Calling、ReAct、Agent）
- 第一阶段：跑通第一个 Agent（调 API → Function Calling → ReAct Agent）
- 第二阶段：玩转 Agent（加工具、故意失败、改 System Prompt）
- 第三阶段：RAG
- 第四阶段：工程化

**Why:** 用户是 Java 程序员，对 AI/Python 有畏惧感，需要降低门槛

**How to apply:** 讲解新概念时，先说"本质是什么"，再给类比，最后才是技术细节。避免一上来就讲底层原理。
