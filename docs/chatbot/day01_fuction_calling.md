# Function Calling 学习笔记

## 一句话理解

> 你定义工具 → AI 决定调用哪个工具、传什么参数 → 你执行工具 → 把结果告诉 AI → AI 生成最终回复

用 Java 思维：**定义接口 → AI 填参数调用 → 你实现方法 → 返回结果**

---

## 核心流程图

```
用户: "帮我算一下 123 + 456"
        │
        ▼
┌─────────────────────────────────┐
│  第 1 次 API 调用                │
│  messages: [用户消息]             │
│  tools: [calculator, get_weather]│  ← 告诉 AI 有哪些工具
└─────────────────────────────────┘
        │
        ▼
   AI 返回 tool_use
   {name: "calculator",
    input: {operation:"add", a:123, b:456}}
        │
        ▼
┌─────────────────────────────────┐
│  你本地执行工具                    │
│  calculator(add, 123, 456)       │
│  结果: "123 + 456 = 579"        │
└─────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────┐
│  第 2 次 API 调用                │
│  messages: [                     │
│    用户消息,                      │
│    AI 的 tool_use 回复,          │
│    tool_result (你执行的结果)      │  ← 把结果告诉 AI
│  ]                               │
└─────────────────────────────────┘
        │
        ▼
   AI 返回最终文本
   "123 + 456 等于 579"
```

---

## API 参数对照表

### 请求参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `tools` | list[dict] | 工具定义列表，告诉 AI 有哪些工具可用 |
| `tool_choice` | dict | 可选，控制 AI 的工具调用行为 |

### tools 结构（工具定义）

```python
{
    "name": "calculator",              # 工具名称（AI 调用时用这个名字）
    "description": "计算器",            # 描述（AI 根据这个判断何时使用）
    "input_schema": {                  # 参数定义（JSON Schema 格式）
        "type": "object",
        "properties": {
            "operation": {
                "type": "string",
                "description": "运算类型",
                "enum": ["add", "subtract", "multiply", "divide"]
            },
            "a": {"type": "number", "description": "第一个数"},
            "b": {"type": "number", "description": "第二个数"}
        },
        "required": ["operation", "a", "b"]
    }
}
```

### 响应中的 content block 类型

| type | 说明 | 关键字段 |
|------|------|---------|
| `text` | 普通文本回复 | `block.text` |
| `tool_use` | AI 想调用工具 | `block.id`, `block.name`, `block.input` |

### tool_result 格式（把工具结果告诉 AI）

```python
{
    "type": "tool_result",
    "tool_use_id": "toolu_xxx",   # 必须关联到 AI 的 tool_use.id
    "content": "123 + 456 = 579"  # 工具执行结果
}
```

---

## 关键点总结

1. **tools 是"接口定义"**：你告诉 AI 有哪些工具、每个工具做什么、需要什么参数
2. **tool_use 是"AI 的调用请求"**：AI 返回 `stop_reason="tool_use"`，content 里包含要调用的工具名和参数
3. **tool_result 是"你的实现"**：你本地执行工具，把结果通过 tool_result 传回给 AI
4. **两次 API 调用**：第一次 AI 决定调用工具，第二次 AI 根据工具结果生成最终回复
5. **tool_use_id 是关联键**：tool_result 必须包含 tool_use_id，这样 AI 才知道是哪个调用的结果

---

## 与 Java 的类比

| Function Calling | Java |
|-----------------|------|
| `tools` 定义 | 接口 interface |
| `tool_use` 调用 | 接口方法调用 |
| `tool_result` 结果 | 方法返回值 |
| AI 决定调用哪个工具 | 策略模式，运行时决定 |
