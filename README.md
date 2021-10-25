# fast-api-sample

## 参考URL
### https://zenn.dev/sh0nk/books/537bb028709ab9/viewer/f1b6fc
### https://qiita.com/bee2/items/75d9c0d7ba20e7a4a0e9


# 1. 環境構築
## poetryによるPython環境のセットアップ
$ docker-compose run \
  --entrypoint "poetry init \
    --name demo-app \
    --dependency fastapi \
    --dependency uvicorn[standard]" \
  demo-app

## FastAPIのインストール
docker-compose run --entrypoint "poetry install" demo-app


# 2. データベースの接続（MySQL）
## "db" コンテナの中で "mysql demo" コマンドを発行
docker-compose exec db mysql demo

## mysqlクライアントのインストール
## "demo-app" コンテナの中で "poetry add sqlalchemy aiomysql" を実行
docker-compose exec demo-app poetry add sqlalchemy aiomysql


# 3. DockerコンテナのMySQLにテーブルを作成
## api モジュールの migrate_db スクリプトを実行する
docker-compose exec demo-app poetry run python -m api.migrate_db
