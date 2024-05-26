# nginx のベースイメージを指定
FROM nginx:alpine

# 必要なパッケージをインストール
RUN apk update && apk add certbot

# 証明書生成スクリプトをコピー
COPY generate-certs.sh /etc/nginx/generate-certs.sh
RUN chmod +x /etc/nginx/generate-certs.sh

# 証明書ディレクトリのマウント
VOLUME ["/etc/letsencrypt"]

# nginxを起動するためのCMDを指定
CMD ["nginx", "-g", "daemon off;"]
