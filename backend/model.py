import os
from langchain_deepseek import ChatDeepSeek
import data_type
from langchain_core.prompts import ChatPromptTemplate
from document_process import FAISS_INDEX, EMBEDDING_MODEL, DOCUMENT_SPLITED

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_ENDPOINT = os.getenv("DEEPSEEK_ENDPOINT")
prompt = ChatPromptTemplate(
    [
        (
            "system",
            " 你现在是一名专业的电子工程师，电工学老师，你的任务是回答同学们提出的电学/模电/数电/信号与系统/电子元件制造工艺等问题，要求回答仔细，符合递归引导学生思考理解问题",
        ),
        (
            "human",
            "{question}",
        ),
    ]
)


# 配置模型参数
def model_set() -> ChatDeepSeek:
    return ChatDeepSeek(
        model="deepseek-chat",
        temperature=data_type.temperature_index,
        max_tokens=None,
        timeout=300,
        max_retries=3,
    )


# 模型初始化,调用模型
async def model_process(question: str):
    llm = model_set()
    chain = (
        prompt
        | llm
        | ChatDeepSeek.RAGChain(
            index=FAISS_INDEX,
            embedding_model=EMBEDDING_MODEL,
            documents=DOCUMENT_SPLITED,
            k=data_type.k_index,
            return_source_documents=False,
        )
    )
    response = await chain.invoke(question)  # 接受来自前端的拆包的数据

    return response
