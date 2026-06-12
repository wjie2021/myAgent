# 全局 Python vs 虚拟环境 .venv

> 背景：项目用的是虚拟环境 .venv，和全局 Python 有什么区别？

---

## 简单类比

| | 全局 Python | 虚拟环境 .venv |
|---|---|---|
| 类比 | 家里的公共药箱 | 每个项目自己的小药箱 |
| 安装位置 | 系统级，所有项目共享 | 项目级，只属于当前项目 |
| 包的影响 | 装一个包，所有项目都能用 | 只影响当前项目 |

---

## 核心区别

### 1. 全局 Python（系统级）

```bash
# 安装的包对所有项目生效
pip install requests   # 所有项目都能 import requests
```

**问题：**
- 项目 A 需要 `requests==2.28`
- 项目 B 需要 `requests==2.31`
- 冲突了！只能装一个版本

### 2. 虚拟环境 .venv（项目级）

```bash
# 创建虚拟环境（每个项目独立一份）
python -m venv .venv

# 激活虚拟环境
.venv\Scripts\activate    # Windows
source .venv/bin/activate # Mac/Linux

# 安装的包只对当前项目生效
pip install requests
```

**好处：**
- 每个项目有自己的依赖版本，互不干扰
- 项目删了，虚拟环境一删就干净
- 方便协作（通过 `requirements.txt` 同步环境）

---

## 项目结构示例

```
myAgent/
├── .venv/                ← 项目专属的 Python 环境
│   ├── Scripts/python    ← 这个项目用的 Python 解释器
│   └── Lib/site-packages ← 这个项目装的包
├── requirements.txt      ← 依赖清单
└── examples/
```

---

## 常用命令

```bash
# 激活虚拟环境（每次打开终端要先激活）
.venv\Scripts\activate

# 激活后，命令行前面会出现 (.venv) 标识
(.venv) D:\0my\claude\myAgent>

# 安装依赖
pip install -r requirements.txt

# 退出虚拟环境
deactivate
```

---

## 一句话总结

> **全局 Python** = 系统公用，容易版本冲突
> **虚拟环境 .venv** = 项目独占，干净隔离，推荐！

---

> 📅 创建时间：2026-06-12
