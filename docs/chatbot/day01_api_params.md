# Day 01 — API 入参与出参记录

基于 MiMo API（兼容 Anthropic SDK）的实际调用结果整理。

---

## 入参（client.messages.create）

```python
client.messages.create(
    model="mimo-v2.5-pro",
    max_tokens=1024,
    system="你是MiMo...",
    messages=[...],
    top_p=0.95,
    stream=False,
    temperature=1.0,
    stop_sequences=None
)
```

| 参数 | 类型 | 说明 |
|------|------|------|
| `model` | str | 模型名称，如 `mimo-v2.5-pro` |
| `max_tokens` | int | 回复最大 token 数（1 汉字 ≈ 1-2 token） |
| `system` | str | 系统提示词，设定 AI 角色和行为规则 |
| `messages` | list | 对话消息列表，即**上下文（Context）** |
| `top_p` | float | 采样阈值（0~1），越大回复越随机多样 |
| `temperature` | float | 温度（0~1），0=确定性高，1=更随机 |
| `stream` | bool | 是否流式输出（True=逐字返回，False=等全部生成完） |
| `stop_sequences` | list/None | 遇到指定字符串就停止生成 |

### messages 结构

```python
messages=[
    {
        "role": "user",            # 角色：user / assistant / system
        "content": [
            {
                "type": "text",    # 内容类型
                "text": "请介绍一下你自己"  # 实际文本
            }
        ]
    }
]
```

多轮对话时，往这个列表里不断追加 user 和 assistant 的消息即可。

---

## 出参（message 对象）

实际返回的完整对象结构：

```text
Message(
    id='23f6e905e1ff415cb6b4a8dcb0e3ba36',
    model='mimo-v2.5-pro',
    role='assistant',
    type='message',
    stop_reason='end_turn',
    content=[...],          # 核心：回复内容块列表
    usage=Usage(...)        # token 用量统计
)
```

### 顶层字段

| 字段 | 说明 |
|------|------|
| `id` | 本次请求的唯一标识 |
| `model` | 实际使用的模型名 |
| `role` | 固定为 `assistant`（AI 的回复） |
| `type` | 固定为 `message` |
| `stop_reason` | 停止原因：`end_turn`=正常结束，`max_tokens`=达到上限 |
| `content` | 回复内容列表，包含一个或多个内容块 |

### content 列表（核心）

返回的内容可能包含多种类型的 block：

#### TextBlock — 文本回复

```python
TextBlock(
    type='text',
    text='你好！我是MiMo，由小米公司大模型Core团队开发的大语言模型...',
    citations=None
)
```

这是最终要展示给用户的内容。

#### ThinkingBlock — 思考过程

```python
ThinkingBlock(
    type='thinking',
    thinking='好的，用户让我介绍自己，这是个简单的自我介绍需求...',
    signature=''
)
```

模型的内部推理过程，**不需要展示给用户**，但对调试有用。代码中需要判断 `block.type == "text"` 来过滤。

### usage — Token 用量

```python
Usage(
    input_tokens=60,       # 输入消耗的 token 数
    output_tokens=137      # 输出消耗的 token 数
)
```

用于统计费用和监控用量。

---

## 踩坑记录

| 问题 | 原因 | 解决 |
|------|------|------|
| SSL 连接失败 | `base_url` 多写了 `/v1/messages`，SDK 会自动拼接 | 只填到 `/anthropic` |
| GBK 编码报错 | Windows 终端默认 GBK，emoji 无法显示 | 运行时加 `PYTHONIOENCODING=utf-8` |
| ThinkingBlock 无 text 属性 | 返回内容含思考块，结构不同于 TextBlock | 判断 `block.type == "text"` 再取值 |
