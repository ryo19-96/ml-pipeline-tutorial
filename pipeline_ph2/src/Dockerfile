# syntax=docker/dockerfile:1
FROM python:3.10-slim

WORKDIR /app

# 必要ファイルのコピー
COPY pyproject.toml uv.lock ./

# uvのインストールと依存パッケージのインストール
RUN pip install --upgrade pip && \
    pip install uv && \
    uv pip install --system --requirement <(uv pip compile pyproject.toml)

# アプリケーションコードのコピー
COPY model/ ./model/

# デフォルトコマンド
CMD ["bash"]