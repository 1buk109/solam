- 実行環境にあった docker desktop app がインストールされていることを確認すること. インストールされていない場合は下記公式ページからインストールする必要がある.
  （Make sure that docker desktop app is installed in your environment. If not, you need to install it from the following official page.）
      [https://docs.docker.com/engine/install/#server](https://docs.docker.com/engine/install/#server)

## docker image 作成・コンテナ起動

1. **【docker image の作成 → コンテナ起動】**

- 下記コマンドを dev ディレクトリで実行.
  - バックグラウンドでデーモン起動したい場合は`-d`オプションをつけて実行すること.

（Execute the following command in the dev directory. If you want to start as a daemon(in the background), execute the command with the `-d` option.）

```bash
$ docker-compose up
```

2. **【コンテナ起動確認】**

- 下記コマンドで docker で起動中のプロセスを確認
  （Check the processes running on docker with the following command. ）

```bash
$ docker ps

CONTAINER ID   IMAGE      COMMAND                  CREATED       STATUS       PORTS                    NAMES
ccad5ebd3548   dev_web    "python manage.py ru…"   2 hours ago   Up 2 hours   0.0.0.0:8000->8000/tcp   dev_web_1
300e89b5273b   postgres   "docker-entrypoint.s…"   2 hours ago   Up 2 hours   5432/tcp                 dev_db_1
```

- 「dev_web」と「postgres」が立ち上がっていれば問題なし.
  （Confirm that "dev_web" and "postgres" are running. ）

3. 【**django 環境の確認**】

- `[http://localhost:8000/](http://localhost:8000/)`にアクセスし、django が立ち上がっていることを確認する.
  （Go to http://localhost:8000/ and make sure django is up and running. ）
