FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    libgomp1 \ 
    && rm -rf /var/lib/apt/lists/*

##apt-get update 执行软件包列表的更新
##apt-get install -y 安装指定的软件包，-y选项表示自动回答“是”以确认安装,&&表示前一个命令成功后再执行后一个命令
##build-essential 包含编译软件所需的基本工具，如gcc、g++、make等
##libssl-dev 提供SSL和TLS协议的开发库
##libffi-dev 提供外部函数接口的开发库，允许调用C语言函数
##python3-dev 提供Python 3的开发头文件和静态库，便于编译Python扩展模块
##rm -rf /var/lib/apt/lists/* 清理apt缓存，释放空间
COPY backend/requirements.txt  /app/requirements.txt
##将宿主机的backend/requirements.txt文件复制到容器内的/app/目录下，命名为requirements.txt
RUN pip install --no-cache-dir --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple && \
    pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple && \
    pip install --no-cache-dir faiss-cpu -i https://pypi.tuna.tsinghua.edu.cn/simple
##使用pip安装requirements.txt文件中列出的Python依赖包，--no-cache-dir选项表示不使用缓存，节省空间


COPY backend/ /app/backend
##将宿主机的backend/目录复制到容器内的/app/backend/目录下

EXPOSE 8000
##声明容器在运行时会监听8000端口

ENV PYTHONPATH=/app
##设置环境变量PYTHONPATH为/app，指定Python模块搜索路径
ENV PYTHONUNBUFFERED=1
##设置环境变量PYTHONUNBUFFERED为1，确保Python输出不被缓冲

CMD ["uvicorn","backend.server:app","--host","0.0.0.0","--port","8000"]