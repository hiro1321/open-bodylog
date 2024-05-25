# ベースイメージを指定
FROM python:3.12

# 環境変数の設定
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 必要なパッケージのインストール
RUN apt-get update \
    && apt-get install -y apt-utils certbot python3-certbot-nginx \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 作業ディレクトリを設定
WORKDIR /code

# 依存関係をインストール
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# ソースコードをコピー
COPY . /code/
