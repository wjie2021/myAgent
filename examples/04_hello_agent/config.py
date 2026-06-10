"""
配置文件
集中管理所有配置项，方便修改和维护
"""

import os

# === LLM 配置 ===
# 请根据您使用的服务，将这里替换成对应的凭证和地址
API_KEY = os.environ.get("LLM_API_KEY", "YOUR_API_KEY")
BASE_URL = os.environ.get("LLM_BASE_URL", "YOUR_BASE_URL")
MODEL_ID = os.environ.get("LLM_MODEL_ID", "YOUR_MODEL_ID")

# === 工具配置 ===
TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY", "YOUR_Tavily_KEY")

# === Agent 配置 ===
MAX_LOOP_COUNT = 5  # Agent 最大循环次数
