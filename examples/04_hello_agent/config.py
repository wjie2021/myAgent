"""
配置文件
集中管理所有配置项，方便修改和维护
"""

import os

# === LLM 配置 ===
# 请根据您使用的服务，将这里替换成对应的凭证和地址
API_KEY = os.environ.get("LLM_API_KEY", "tp-ci6a2b51kji3da55zqnlvh7x6pqs9ebezverd7hjrnppgc8g")
BASE_URL = os.environ.get("LLM_BASE_URL", "https://token-plan-cn.xiaomimimo.com/v1")
MODEL_ID = os.environ.get("LLM_MODEL_ID", "mimo-v2.5")

# === 工具配置 ===
TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY", "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")

# === Agent 配置 ===
MAX_LOOP_COUNT = 5  # Agent 最大循环次数
