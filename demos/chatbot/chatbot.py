import os
from anthropic import Anthropic

client = Anthropic(
    api_key="sk-ckyqs5ys30wspw6r29x5oekfby6ds7cxxua8ithvneibnoty",
    base_url="https://api.xiaomimimo.com/anthropic"
    
)

message = client.messages.create(
    model="mimo-v2.5-pro",
    max_tokens=1024,
    system="你是MiMo（中文名称也是MiMo），是小米公司研发的AI智能助手。今天的日期：2026年6月8日，你的知识截止日期是2024年12月。",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "请介绍一下你自己"
                }
            ]
        }
    ],
    top_p=0.95,
    stream=False,
    temperature=1.0,
    stop_sequences=None
)
print(message)

print(message.content)

for block in message.content:
    if block.type == "text":
        print(block.text)