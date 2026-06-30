# 07_ReActChat

前后端分离的 ReAct 聊天 Demo。

## 技术栈

- **后端**: Python + FastAPI + SSE
- **前端**: React + Ant Design + Vite

## 启动方式

### 1. 启动后端

```bash
cd backend
pip install -r requirements.txt
python app.py
```

后端运行在 http://127.0.0.1:8000

### 2. 启动前端

```bash
cd frontend
npm install
npm run dev
```

前端运行在 http://localhost:5173

## 项目结构

```
07_ReActChat/
├── backend/
│   ├── app.py          # FastAPI 服务（SSE 流式接口）
│   ├── agent.py        # ReAct Agent
│   ├── llm.py          # LLM 客户端
│   ├── tools.py        # 工具执行器
│   ├── .env            # 环境变量
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.jsx     # 主组件
│   │   ├── App.css     # 样式
│   │   └── main.jsx    # 入口
│   ├── index.html
│   ├── package.json
│   └── vite.config.js  # Vite 配置（含 API 代理）
└── README.md
```

## API 接口

- `GET /api/health` - 健康检查
- `POST /api/chat` - 同步接口，返回最终结果
- `POST /api/chat/stream` - SSE 流式接口，逐步返回思考过程
