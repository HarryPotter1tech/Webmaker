from fastapi import Body, FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os
from backend import data_type
from backend import model
from backend import database

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST", "GET", "OPTIONS"],
    allow_headers=["*"],
)


@app.post("/ask", response_model=data_type.response_type)  # 声明强制返回数据类型
async def response_deepseek(question: data_type.question_type):
    AIresponse = await model.model_process(
        question.question
    )  # 调用模型处理用户问题(回复信息)
    data_type.response.response = AIresponse.content  # 模型返回的回答内容
    data_type.response.numbers = question.numbers  # 保持和请求一致的对话轮次
    data_type.response.status = 200
    data_type.response.token_used = AIresponse.usage_metadata.get("total_tokens", 0)
    print("Tokens used:", data_type.response.token_used)
    print("AI Response:", data_type.response.response)

    database.update_db(  # 保存用户聊天记录到数据库
        role=data_type.question.role,
        message=data_type.question.question,
        talkcycle=data_type.question.numbers,
    )

    database.update_db(  # 保存模型回答到数据库
        role=data_type.response.role,
        message=data_type.response.response,
        talkcycle=data_type.response.numbers,
    )
    return data_type.response


@app.post("/temperature")
async def change_temperature(payload: dict = Body(...)):
    data_type.temperature_index = payload.get("temperature", 0.0)
    return {"temperature": data_type.temperature_index}


@app.get("/download_chat_history")
async def download_chat_history(background_tasks: BackgroundTasks):
    print("download_chat_history: called")
    file_ = database.transform_db_to_word()  # 生成唯一临时文件
    background_tasks.add_task(
        lambda p: os.remove(p) if os.path.exists(p) else None, file_["file_path"]
    )
    headers = {"Cache-Control": "no-store", "Pragma": "no-cache", "Expires": "0"}
    return FileResponse(
        path=file_["file_path"], filename=file_["filename"], headers=headers
    )
