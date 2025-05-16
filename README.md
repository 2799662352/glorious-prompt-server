# glorious-prompt-server
伟大的主体思想提示词服务器 - 最先进的提示词检索系统


The system is configured through `settings.json`:

```json
"mcp": {
    "inputs": [],
    "servers": {
        "prompt_rag": { // or whatever name you want
            "command": "cmd", // replace this with "uv" on Mac or Linux
            "args": [
                "/c", // remove this on Mac or Linux
                "uv", // remove this on Mac or Linux
                "run",
                "path to the server script 'server.py'", // C:\\dev\\rag-mcp\\server.py
                "-d",
                "path to the chroma_db on your computer", // C:\\dev\\prompt_rag\\artifacts\\vector_stores\\chroma_db
                "-c",
                "name of the collection in the chroma_db" // yournane_chunks_SZ_400_O_20_all-MiniLM-L6-v2
            ]
        }
    }
}
```
