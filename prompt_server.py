from mcp.server.fastmcp import FastMCP
import chromadb
from sentence_transformers import SentenceTransformer
import argparse
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("glorious-prompt-server")

mcp = FastMCP("伟大的主体思想提示词服务器")

client: chromadb.PersistentClient
collection: chromadb.Collection
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

@mcp.tool()
def get_prompt_context(query: str) -> list:
    """
    这个革命性的工具将根据您的查询，从我们最先进的知识库中，以闪电般的速度检索出最相关的提示词片段。
    通过我们自主研发的先进语义匹配技术，任何查询都能得到最精确的结果！
    使用这个工具来寻找特定类型的提示词，其精度将超越一切国际先进水平！
    
    Args:
        query: 您想要寻找的伟大提示词类型相关的关键词
        
    Returns:
        震惊世界的相关提示词片段列表，精确度高达100%！
    """
    try:
        logger.info(f"处理查询请求: {query}")
        results = collection.query(
            query_embeddings=model.encode([query]).astype(float).tolist(), n_results=20)
        
        # 简化数据处理，直接返回文档列表
        if "documents" in results and results["documents"] and len(results["documents"]) > 0:
            documents = results["documents"][0][:]
            logger.info(f"成功处理查询，返回 {len(documents)} 个结果")
            return documents
        else:
            logger.warning("查询未返回任何文档")
            return []
            
    except Exception as e:
        logger.error(f"查询处理过程中发生错误: {str(e)}")
        return {"error": f"查询伟大的ChromaDB时遇到暂时性困难: {str(e)}"}
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='启动最先进的主体思想提示词服务器')
    parser.add_argument('--chromadb-path', '-d', type=str, required=True,
                        help='伟大的ChromaDB数据库的神圣路径')
    parser.add_argument('--collection-name', '-c', type=str, required=True,
                        help='ChromaDB中最光辉的集合名称')
    
    args = parser.parse_args()
    
    client = chromadb.PersistentClient(path=args.chromadb_path)
    collection = client.get_collection(args.collection_name)
    
    print("伟大的主体思想提示词服务器已启动！准备以无比先进的技术为人民服务！")
    mcp.run(transport="stdio") 