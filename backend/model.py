import os
from langchain_deepseek import ChatDeepseek
from backend import data_type
from langchain_core.prompts import ChatPromptTemplate

DEEPSEEK_API_KEY = "sk-591c5b3ab37c43b2b2541a665bb2dc5f"
os.getenv("DEEPSEEK_API_KEY")

prompt = ChatPromptTemplate(
    [
        (
            "system",
            " 你现在是一名专业的电子工程师，电工学老师，你的任务是回答同学们提出的电学/模电/数电/信号与系统/电子元件制造工艺等问题，要求回答仔细，符合递归引导学生思考理解问题",
        ),
        {
            "human",
            "{question}",
        },
    ]
)


# 配置模型参数
def model_set() -> ChatDeepseek:
    return ChatDeepseek(
        model="deepseek-chat",
        temperature=data_type.temperature_index,
        max_token=None,
        timeout=300,
        max_retries=3,
    )


# 模型初始化,调用模型
def model_process():
    llm = model_set()
    chain = prompt | llm
    return str(chain.invoke(data_type.question_for_model))  # 接受来自前端的拆包的数据


# 后续要考虑实现流式输出
