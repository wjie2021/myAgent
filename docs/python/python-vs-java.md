# Python vs Java：程序结构对比

> 背景：作为 Java 程序员，看到 Python 文件没有类声明、没有方法声明，直接写代码就能运行，感到困惑。

## 核心区别

### Java — 必须有类和方法

```java
public class Chatbot {
    public static void main(String[] args) {
        // 代码必须写在方法里，方法必须在类里
        System.out.println("Hello");
    }
}
```

### Python — 文件本身就是执行单元

```python
# 文件从上到下直接执行，不需要类，不需要 main 方法
print("Hello")  # 直接写，直接跑
```

## 对比表

| 特性 | Java | Python |
|------|------|--------|
| 代码必须放在 | 类 → 方法 → 代码块 | 文件里直接写 |
| 程序入口 | `public static void main` | 文件第一行开始执行 |
| 类声明 | 必须 | 可选，需要时才写 |
| 方法声明 | 必须 | 可选，需要时才写 |

## 实际例子

### 当前项目的 chatbot_while.py

```python
import os
from anthropic import Anthropic

# 直接创建客户端，不需要包在类里
client = Anthropic(
    api_key="xxx",
    base_url="https://api.xiaomimimo.com/anthropic"
)

# 直接调用 API，不需要 main 方法
message = client.messages.create(
    model="mimo-v2.5-pro",
    max_tokens=1024,
    messages=[{"role": "user", "content": "你好"}]
)

# 直接打印结果
print(message.content)
```

这段代码从上到下执行，完全正确，就是 Python 的标准写法。

## 什么时候用类？

当逻辑变复杂时自然会用，比如多轮对话：

```python
class Chatbot:
    def __init__(self):
        self.client = Anthropic(...)
        self.history = []  # 保存对话历史

    def chat(self, user_input):
        self.history.append({"role": "user", "content": user_input})
        response = self.client.messages.create(
            model="mimo-v2.5-pro",
            messages=self.history
        )
        self.history.append({"role": "assistant", "content": response.content[0].text})
        return response.content[0].text
```

**原则：需要时才用，不需要就不写。**

## 总结

- **Java**：一切皆类，代码必须放在类的方法里
- **Python**：文件即程序，从上到下直接执行，类和方法是可选的组织方式

Python 的哲学是"能简单就简单"，写 demo 或脚本时不需要强制包装类。
