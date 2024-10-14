FROM python:3.10-slim

# 创建一个非root用户
RUN useradd -m appuser

# 设置工作目录
WORKDIR /app

# 复制当前目录内容到工作目录
COPY . /app

# 创建 vote 目录并设置权限
RUN mkdir -p /app/vote && chown -R appuser:appuser /app/vote

# 切换到非root用户
USER appuser

# 设置环境变量
ENV PATH="/home/appuser/.local/bin:${PATH}"

# 更新pip并安装Python依赖项
RUN pip install --no-cache-dir --user --upgrade pip \
    && pip install --no-cache-dir --user fastapi uvicorn sympy pycryptodome pyjwt requests flask flask_cors gunicorn

# 暴露应用程序运行的端口
EXPOSE 5001

# 设置容器启动时运行的命令
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5001", "app:app"]