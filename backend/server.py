from fastapi import Body, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
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
    data_type.question_for_model = question.question
    data_type.response_for_client = model.model_process()  # 调用模型处理用户问题
    data_type.response.response = data_type.response_for_client
    data_type.response.numbers = question.numbers  # 保持和请求一致的对话轮次
    data_type.response.status = 200

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
async def download_chat_history():
    file_ = model.transform_db_to_word()  # file是一个字典，包含文件路径和文件名
    return FileResponse(path=file_["file_path"], filename=file_["filename"])
