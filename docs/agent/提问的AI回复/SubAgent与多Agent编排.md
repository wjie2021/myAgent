# SubAgent 与多 Agent 编排

## SubAgent 的本质

**就是"派小弟干活"。**

主 Agent（项目经理）把任务拆分，派给多个 SubAgent（实习生）去并行执行，最后汇总结果。

---

## 为什么要用 SubAgent？

### 1. 并行加速

两个 agent 同时跑，15 秒搞定；串行要 30 秒。

### 2. 上下文窗口限制

单个 agent 的上下文装不下太多内容时，拆成多个 agent 各处理一部分。

### 3. 独立视角（最容易忽略）

即使上下文无限长，多个 agent 仍然比一个好。

- 一个 agent 专注看性能 → 上下文全是性能相关思考
- 一个 agent 专注看安全性 → 上下文全是安全相关思考

**如果只用一个 agent，上下文会混杂两种思考，容易互相干扰。**

类比：自己审查自己的代码容易有盲区，两个人独立审查更容易发现问题。

---

## SubAgent 的管理方式

### 核心流程

```
用户提需求
  ↓
主 Agent 判断：需要拆分吗？
  ↓ (需要)
派 N 个 agent，给每个分配任务
  ↓
它们各自干活，结果返回给主 Agent
  ↓
主 Agent 汇总，给用户最终答案
```

**主 Agent 是"中心调度者"，所有 SubAgent 的结果都回到它这里。**

### 管理的难点

| 问题 | 需要想清楚的 |
|------|-------------|
| 什么时候拆分？ | 任务太简单就不拆，太复杂才拆 |
| 拆成几个？ | 拆太多浪费 token，拆太少没效果 |
| 每个 agent 干什么？ | 任务要独立，不能互相依赖 |
| 怎么汇总？ | 简单拼接？还是让另一个 agent 综合？ |

---

## 自己实现多 Agent 并行

### Python 伪代码（基于 Anthropic SDK）

```python
import asyncio
from anthropic import Anthropic

client = Anthropic()

# 一个 agent 的工作函数
async def run_agent(task: str) -> str:
    response = client.messages.create(
        model="mimo-v2.5-pro",
        messages=[{"role": "user", "content": task}],
        max_tokens=1024
    )
    return response.content[0].text

# 主 agent：并行派活，然后汇总
async def main_agent(user_request: str):
    # 1. 主 agent 自己分析：要不要拆分？拆成几个？
    tasks = analyze_and_split(user_request)  # 你的决策逻辑

    # 2. 并行派活（核心！）
    results = await asyncio.gather(
        *[run_agent(task) for task in tasks]
    )

    # 3. 汇总结果
    final_answer = summarize(results)  # 你的汇总逻辑
    return final_answer
```

**关键：`asyncio.gather()` 让多个 agent 同时跑，等全部完成后再汇总。**

---

## 现成框架

不用自己造轮子，业界已有框架管理多 Agent 编排：

| 框架 | 特点 |
|------|------|
| **LangGraph** | LangChain 出的，用图结构管理 agent 流程 |
| **CrewAI** | 像组建团队一样，定义角色和任务 |
| **AutoGen** | 微软出的，多个 agent 互相对话 |

本质都在做一件事：**帮你管"派活、等待、汇总"这个流程。**

---

## 总结

**SubAgent = 任务分解 + 并行调度 + 结果汇总。**

即使上下文足够长，SubAgent 的并行加速和独立视角优势仍然存在。但任务简单时，单 Agent 直接做更快，不需要拆分。
