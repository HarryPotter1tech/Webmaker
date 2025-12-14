from pydantic import BaseModel


class response_type(BaseModel):
    role: str  # 回复角色
    response: str  # 模型回复
    numbers: int  # 对话轮数
    status: int  # 回答状态
    token_used: int  # 此轮对话使用的token数


class question_type(BaseModel):
    role: str  # 提问角色
    question: str  # 用户问题
    numbers: int  # 对话轮数
    status: int  # 问题状态


question: question_type = question_type(
    role="user", question="", numbers=0, status=0
)  # 用户问题数据结构
response: response_type = response_type(
    role="Deepseek", response="", numbers=0, status=0, token_used=0
)  # 模型回复数据结构
temperature_index: float = 0.0  # 模型温度参数，默认0.0，后续可调整
