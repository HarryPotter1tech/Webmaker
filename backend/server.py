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


@app.post("/ask", response_model=data_type.response_type)
async def response_deepseek(question: data_type.question_type):
    # 1. 这里的 question 是本次请求独有的数据，不会被别人覆盖

    # 调用模型
    AIresponse = await model.model_process(question.question)

    # 提取数据
    current_token = AIresponse.usage_metadata.get("total_tokens", 0)
    current_content = AIresponse.content

    print("Tokens used:", current_token)
    print("AI Response:", current_content)

    # 2. 【关键】创建一个新的对象来返回，而不是修改全局变量
    # 这样每个人拿到的都是属于自己的那份拷贝
    new_response = data_type.response_type(
        role="assistant",
        response=current_content,
        numbers=question.numbers,
        status=200,
        token_used=current_token,
    )

    # 3. 存数据库时，直接用函数参数(question)和上面的局部变量(current_content)
    database.update_db(
        role=question.role,  # 用户的角色
        message=question.question,  # 用户的问题
        talkcycle=question.numbers,  # 用户的轮次
    )

    database.update_db(
        role="assistant",
        message=current_content,  # AI 的回答
        talkcycle=question.numbers,
    )

    # 4. 返回这个新创建的对象
    return new_response


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
