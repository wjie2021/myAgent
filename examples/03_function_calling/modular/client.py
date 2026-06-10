"""
客户端模块
==========
初始化 Anthropic 客户端，供其他模块调用。
"""

from anthropic import Anthropic

# 创建客户端实例（整个程序共用这一个）
client = Anthropic(
    api_key="tp-ci6a2b51kji3da55zqnlvh7x6pqs9ebezverd7hjrnppgc8g",
    base_url="https://token-plan-cn.xiaomimimo.com/anthropic"
)
