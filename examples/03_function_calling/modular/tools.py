"""
工具定义模块
============
告诉 AI 有哪些工具可以调用。
这里定义的是"接口"，真正的实现在 executor.py 里。
"""

tools = [
    {
        "name": "run_command",
        "description": "在终端执行 shell 命令并返回输出结果。可以用来：查看目录(ls/dir)、读取文件(cat/type)、运行脚本等。",
        "input_schema": {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "要执行的终端命令，如 'ls'、'cat file.txt'、'python script.py'"
                }
            },
            "required": ["command"]
        }
    },
    {
        "name": "read_file",
        "description": "读取指定文件的内容。当用户想查看某个文件时使用。",
        "input_schema": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "文件的路径，如 '/Users/wangjie/AI/myAgent/README.md'"
                }
            },
            "required": ["file_path"]
        }
    }
]
