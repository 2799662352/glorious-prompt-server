"""
提示词服务器启动脚本 - 快速启动提示词检索服务

这个脚本提供了一种简单的方式来启动提示词服务器，
支持配置文件或命令行参数，便于快速部署和测试。
"""

import os
import sys
import json
import logging
import argparse
import subprocess
from pathlib import Path

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/server.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("start_server")

def load_config(config_path: str) -> dict:
    """
    加载配置文件
    
    Args:
        config_path: 配置文件路径
        
    Returns:
        配置字典
    """
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config
    except Exception as e:
        logger.error(f"加载配置文件失败: {str(e)}")
        return {}

def start_server(
    server_script: str,
    chromadb_path: str,
    collection_name: str,
    log_file: str = None
) -> None:
    """
    启动提示词服务器
    
    Args:
        server_script: 服务器脚本路径
        chromadb_path: ChromaDB数据库路径
        collection_name: 集合名称
        log_file: 日志文件路径
    """
    # 确保logs目录存在
    os.makedirs("logs", exist_ok=True)
    
    # 准备命令
    cmd = [
        sys.executable,
        server_script,
        "-d", chromadb_path,
        "-c", collection_name
    ]
    
    log_path = log_file or "logs/server_output.log"
    
    try:
        logger.info(f"启动服务器: {' '.join(cmd)}")
        logger.info(f"输出将被记录到: {log_path}")
        
        # 创建日志文件
        with open(log_path, 'w') as log_file:
            # 启动进程并重定向输出
            process = subprocess.Popen(
                cmd,
                stdout=log_file,
                stderr=subprocess.STDOUT,
                text=True
            )
            
            logger.info(f"服务器已启动，进程ID: {process.pid}")
            logger.info("服务器正在运行中，按Ctrl+C停止...")
            
            # 等待进程结束
            process.wait()
            
    except KeyboardInterrupt:
        logger.info("接收到中断信号，正在停止服务器...")
        process.terminate()
        logger.info("服务器已停止")
    except Exception as e:
        logger.error(f"启动服务器时出错: {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="启动提示词服务器")
    parser.add_argument("--config", type=str, 
                        help="配置文件路径")
    parser.add_argument("--server-script", type=str, default="prompt_server.py",
                        help="服务器脚本路径")
    parser.add_argument("--chromadb-path", type=str,
                        help="ChromaDB数据库路径")
    parser.add_argument("--collection-name", type=str,
                        help="集合名称")
    parser.add_argument("--log-file", type=str, 
                        help="日志文件路径")
    
    args = parser.parse_args()
    
    # 如果提供了配置文件，从配置文件加载
    if args.config:
        config = load_config(args.config)
        server_script = config.get("server_script", args.server_script)
        chromadb_path = config.get("chromadb_path", args.chromadb_path)
        collection_name = config.get("collection_name", args.collection_name)
        log_file = config.get("log_file", args.log_file)
    else:
        server_script = args.server_script
        chromadb_path = args.chromadb_path
        collection_name = args.collection_name
        log_file = args.log_file
    
    # 验证必要的参数
    if not chromadb_path:
        logger.error("必须提供ChromaDB路径")
        sys.exit(1)
    
    if not collection_name:
        logger.error("必须提供集合名称")
        sys.exit(1)
    
    # 启动服务器
    start_server(
        server_script=server_script,
        chromadb_path=chromadb_path,
        collection_name=collection_name,
        log_file=log_file
    )