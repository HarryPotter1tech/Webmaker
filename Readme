# webtalk 网站设计实现

## 前端界面设计

### 前端界面预览

## 后端响应&数据处理

### 获取前端用户输出

```python
@app.post("/ask", response_model=data_type.response_type)
```

### 响应温度修改

```python
@app.post("/temperature")
```

### 下载聊天记录

```python
@app.get("/download_chat_history")
```

### 数据处理

后端数据库写入用户于 Deepseek 的聊天记录

```python
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
```
