"""
ReAct Chat 后端服务
基于 FastAPI，提供 SSE 流式接口
"""

import json
import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from llm import HelloAgentsLLM
from tools import ToolExecutor, search
from agent import ReActAgent

# --- 初始化 ---
app = FastAPI(title="ReAct Chat API")

# 允许前端跨域访问（开发时 localhost:5173）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化 Agent 组件
llm_client = HelloAgentsLLM()
tool_executor = ToolExecutor()
search_description = "一个网页搜索引擎。当你需要回答关于时事、事实以及在你的知识库中找不到的信息时，应使用此工具。"
tool_executor.registerTool("Search", search_description, search)
agent = ReActAgent(llm_client=llm_client, tool_executor=tool_executor)


# --- 数据模型 ---
class ChatRequest(BaseModel):
    question: str


# --- 接口 ---

@app.get("/api/health")
def health():
    """健康检查"""
    return {"status": "ok"}


@app.post("/api/chat")
async def chat(request: ChatRequest):
    """
    同步接口：一次性返回最终结果
    """
    result = agent.run(request.question)
    return result


@app.post("/api/chat/stream")
async def chat_stream(request: ChatRequest):
    """
    SSE 流式接口：逐步返回思考过程
    每一步都会推送一个 JSON 事件
    """
    def event_generator():
        """SSE 事件生成器"""
        queue = []

        def on_step(step_data):
            queue.append(step_data)

        # 在线程中运行 Agent（因为 Agent 是同步的）
        import threading
        result = [None]

        def run_agent():
            result[0] = agent.run(request.question, on_step=on_step)

        thread = threading.Thread(target=run_agent)
        thread.start()

        # 等待 Agent 完成，期间持续发送事件
        sent_index = 0
        while thread.is_alive() or sent_index < len(queue):
            # 发送新事件
            while sent_index < len(queue):
                data = json.dumps(queue[sent_index], ensure_ascii=False)
                yield f"data: {data}\n\n"
                sent_index += 1
            # 短暂等待
            if thread.is_alive():
                import time
                time.sleep(0.1)

        # 发送结束标记
        yield f"data: {json.dumps({'type': 'done'}, ensure_ascii=False)}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        },
    )


if __name__ == "__main__":
    import uvicorn
    print("\n[START] ReAct Chat backend starting...")
    print("[API] http://127.0.0.1:8000")
    print("[DOC] http://127.0.0.1:8000/docs\n")
    uvicorn.run(app, host="0.0.0.0", port=8000)
