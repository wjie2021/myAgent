# Python 新人速查指南

> ⚠️ **本文档由 AI 生成**，供学习参考。如有疑问请结合官方文档验证。
>
> 针对有其他语言经验（前端/后端）的开发者，重点讲 Python 和你熟悉语言的差异。

---

## 1. 语法基础：Python 的"省事儿"哲学

### 缩进代替大括号

Python 用缩进（通常 4 个空格）来表示代码块，而不是 `{}`。缩进错了直接报错。

```python
# ✅ 正确
if age >= 18:
    print("成年")
    print("可以投票")

# ❌ 错误 — 缩进不一致
if age >= 18:
    print("成年")
        print("可以投票")  # IndentationError
```

### 不需要分号和大括号

```python
# Python — 不写分号，不写 {}
name = "王杰"
print(name)

# 对比你可能熟悉的语言
# const name = "王杰";    ← JS
# String name = "王杰";   ← Java
```

### 变量不需要声明类型

```python
# Python 会自动推断类型，直接赋值就行
name = "王杰"        # 字符串
age = 25             # 整数
price = 9.99         # 浮点数
is_student = True    # 布尔值

# 甚至可以中途换类型（不推荐，但合法）
x = 100
x = "现在变成字符串了"  # 合法，但别这么干
```

---

## 2. 数据结构：四种常用的容器

### list（列表）— 最常用，类似 JS 的 Array

```python
fruits = ["苹果", "香蕉", "橘子"]

fruits.append("葡萄")     # 末尾添加
fruits.insert(0, "西瓜")  # 指定位置插入
fruits.remove("香蕉")     # 删除指定元素
first = fruits[0]         # 取第一个
last = fruits[-1]         # 取最后一个（倒数）
slice = fruits[1:3]       # 切片：取第 2~3 个

# 遍历
for fruit in fruits:
    print(fruit)
```

### dict（字典）— 类似 JS 的 Object / Java 的 HashMap

```python
person = {
    "name": "王杰",
    "age": 25,
    "skills": ["Python", "前端"]
}

# 取值
print(person["name"])           # "王杰"
print(person.get("email", ""))  # 不存在时返回默认值，不会报错

# 添加/修改
person["email"] = "test@qq.com"

# 遍历
for key, value in person.items():
    print(f"{key}: {value}")
```

### tuple（元组）— 不可修改的 list

```python
# 一旦创建就不能改，用于函数返回多个值
point = (3, 5)
x, y = point  # 解包：x=3, y=5

# 常见用法：函数返回多个值
def get_user():
    return "王杰", 25  # 实际返回的是 tuple

name, age = get_user()
```

### set（集合）— 去重用

```python
ids = {1, 2, 3, 2, 1}
print(ids)  # {1, 2, 3} — 自动去重

# 常见用途：快速去重
names = ["张三", "李四", "张三", "王五"]
unique = list(set(names))  # ["张三", "李四", "王五"]
```

---

## 3. 函数：用 `def` 定义

```python
# 基本函数
def greet(name):
    return f"你好，{name}"

# 默认参数
def greet(name, greeting="你好"):
    return f"{greeting}，{name}"

greet("王杰")             # "你好，王杰"
greet("王杰", "早上好")   # "早上好，王杰"

# *args — 接收任意数量的位置参数（装进 tuple）
def add(*numbers):
    return sum(numbers)

add(1, 2, 3)  # 6

# **kwargs — 接收任意数量的关键字参数（装进 dict）
def print_info(**info):
    for key, value in info.items():
        print(f"{key}: {value}")

print_info(name="王杰", age=25)
```

---

## 4. 模块和导入：`import` 的几种写法

```python
# 方式 1：导入整个模块
import os
os.path.exists("/tmp")

# 方式 2：从模块导入指定内容
from os import path
path.exists("/tmp")

# 方式 3：导入并起别名（常用）
import numpy as np
from anthropic import Anthropic

# 方式 4：导入全部（不推荐，容易命名冲突）
from os import *
```

### 自己写的文件怎么导入？

```text
project/
├── main.py
├── client.py
└── tools.py
```

```python
# main.py 里这样导入同目录的模块
from client import client
from tools import tools
```

---

## 5. `if __name__ == "__main__"` 是什么？

```python
# utils.py
def helper():
    print("我是工具函数")

print("这句话 import 时也会执行！")  # ← 问题所在

if __name__ == "__main__":
    print("只有直接运行 utils.py 时才执行")
    helper()
```

**解释：**

- 直接运行 `python3 utils.py` → `__name__` 等于 `"__main__"` → 里面的代码会执行
- 别的文件 `from utils import helper` → `__name__` 等于 `"utils"` → 里面的代码**不会**执行

**目的：** 让一个文件既能被别人 import，又能自己独立运行。就像你写的 `main.py` 里的写法。

---

## 6. 字符串格式化：f-string（推荐）

```python
name = "王杰"
age = 25

# ✅ f-string（Python 3.6+，推荐用这种）
msg = f"我叫{name}，今年{age}岁"
msg = f"明年 {age + 1} 岁"            # 里面可以写表达式
msg = f"名字长度: {len(name)}"         # 可以调函数

# ❌ 旧写法（能用但别学了）
msg = "我叫%s，今年%d岁" % (name, age)
msg = "我叫{}，今年{}岁".format(name, age)
```

---

## 7. 异常处理：try / except

```python
try:
    result = 10 / 0
except ZeroDivisionError:
    print("不能除以零")
except Exception as e:
    print(f"其他错误: {e}")
else:
    print("没有出错时执行")
finally:
    print("无论如何都执行")
```

**对比其他语言：**

| Python | 其他语言 |
|--------|----------|
| `try / except` | `try / catch` |
| `except Exception as e` | `catch (Exception e)` |
| `raise ValueError("xxx")` | `throw new ValueError("xxx")` |

---

## 8. 文件操作

```python
# 读文件（推荐用 with，会自动关闭文件）
with open("data.txt", "r", encoding="utf-8") as f:
    content = f.read()          # 读全部
    # lines = f.readlines()    # 读成列表，每行一个元素

# 写文件
with open("output.txt", "w", encoding="utf-8") as f:
    f.write("Hello\n")

# 追加写入
with open("log.txt", "a", encoding="utf-8") as f:
    f.write("新的一行\n")
```

---

## 9. pip 和虚拟环境

### pip — Python 的包管理器（类似 npm）

```bash
pip3 install anthropic          # 安装包
pip3 install anthropic==0.100.0 # 安装指定版本
pip3 uninstall anthropic        # 卸载
pip3 list                       # 查看已安装的包
pip3 freeze > requirements.txt  # 导出依赖清单
pip3 install -r requirements.txt # 从清单安装
```

### 虚拟环境 — 隔离每个项目的依赖（推荐养成习惯）

```bash
# 创建虚拟环境（在项目目录下）
python3 -m venv .venv

# 激活
source .venv/bin/activate       # Mac/Linux
# .venv\Scripts\activate        # Windows

# 激活后，pip install 的包只装到这个项目里
pip install anthropic

# 退出虚拟环境
deactivate
```

**为什么要用？** 不同项目可能需要不同版本的包，虚拟环境让它们互不干扰。

---

## 10. 常见坑（来自其他语言的人容易踩）

### 1) 缩进混用 Tab 和空格

```python
# ❌ 混用 Tab 和空格 → IndentationError
def test():
    print("空格缩进")   # ← 4 个空格
	print("Tab 缩进")   # ← 1 个 Tab
```

**建议：** 编辑器设置 Tab 自动转为 4 个空格。

### 2) 默认参数用可变对象

```python
# ❌ 坑：默认的 list 会在多次调用间共享
def add_item(item, lst=[]):
    lst.append(item)
    return lst

add_item("a")  # ["a"]
add_item("b")  # ["a", "b"] ← 不是 ["b"]！因为默认的 [] 是同一个对象

# ✅ 正确写法
def add_item(item, lst=None):
    if lst is None:
        lst = []
    lst.append(item)
    return lst
```

### 3) `==` vs `is`

```python
# == 比较值是否相等
# is 比较是否是同一个对象（内存地址）

a = [1, 2, 3]
b = [1, 2, 3]
a == b  # True（值相等）
a is b  # False（不是同一个对象）

# 唯一推荐用 is 的场景：判断 None
if x is None:
    pass
```

### 4) `for...else` 语法

```python
# Python 特有：for 循环正常结束（没被 break）时执行 else
for n in range(2, 10):
    if n == 5:
        print("找到了 5")
        break
else:
    print("没找到 5")  # 只有 for 没被 break 时才执行
```

### 5) 列表推导式（简洁但别过度）

```python
# 常规写法
squares = []
for x in range(10):
    squares.append(x ** 2)

# 列表推导式（一行搞定）
squares = [x ** 2 for x in range(10)]

# 带条件
even_squares = [x ** 2 for x in range(10) if x % 2 == 0]
```

---

## 11. 速查对比表

| 概念 | Python | JavaScript | Java |
|------|--------|------------|------|
| 变量声明 | `x = 10` | `let x = 10` | `int x = 10;` |
| 空值 | `None` | `null / undefined` | `null` |
| 字符串格式化 | `f"hi {name}"` | `` `hi ${name}` `` | `"hi " + name` |
| 箭头函数 | `lambda x: x * 2` | `(x) => x * 2` | 不支持 |
| 遍历 | `for x in list` | `for (x of list)` | `for (x : list)` |
| 类 | `class Dog:` | `class Dog {}` | `public class Dog {}` |
| 构造函数 | `def __init__(self):` | `constructor()` | `public Dog()` |
| 异常 | `try/except` | `try/catch` | `try/catch` |
| 包管理 | `pip` | `npm` | `Maven/Gradle` |
| 虚拟环境 | `venv` | `node_modules` | 全局/容器 |

---

## 12. 学习建议

1. **先跑通再理解** — Python 很多东西先用起来，再回头理解原理
2. **多用 `print()` 调试** — Python 没有严格的类型检查，print 是最直观的调试方式
3. **读报错信息** — Python 的错误提示很友好，从最后一行往上读
4. **善用 `type()` 和 `dir()`** — 不确定变量类型时 `print(type(x))`，不知道对象有什么方法时 `print(dir(x))`
5. **别追求一行写完** — 列表推导式、三元表达式等可以很短，但可读性更重要

---

> 📅 生成时间：2026-06-08
> 🤖 生成工具：Claude (AI)
> 📖 建议搭配：[python_vs_java_structure.md](python_vs_java_structure.md) — Python vs Java 程序结构对比
