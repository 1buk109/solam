# log_parser ディレクトリに関しての説明

## ディレクトリ構成

- data: 現状はデモデータを格納している
  - ① 　 GA 経由で取得した JPMT のログデータ
    - APMJ_Eventlogs_3.csv
    - APMJ_Eventlogs_3_processed.csv (process_end を差し込んだ csv)
  - ② 　 server PC から取得した HTTP 通信のログデータ
    - 0_server_log_20220728.txt
      - サーバーログデータを tcpdump で取得した json 形式のテキストファイル
    - 1_server_log_20220728.csv
      - tcpdump から独断と偏見でデータ抽出した csv（改修の余地あり）
    - 2_server_log_20220728.csv
      - 1\_ の csv を元に、PM に必要なデータをさらに抽出、パースした csv
      - これをそのままみんぷろに入れることができる
- parser: 各 log データのパーサー

  - ① 　**ga_log_parser.py**
    - GA 経由で取得したデータをみんぷろに格納できる csv 形式に変換するスクリプト
    - 変換元の csv ファイル path と出力先の path をコマンド引数として受け取る
      - demo command（log_parser 直下で下記コマンドを実行）  
        `python3 parser/ga_log_parser.py -i data/APMJ_Eventlogs_3.csv -o APMJ_Eventlogs_3_processed.csv`
  - ② 　**server_log_parser.py**
    - server PC から取得した HTTP ログデータから必要な情報をパースして csv に変換するスクリプト.
    - 変換元の csv ファイル path と出力先の path をコマンド引数として受け取る
      - demo command（log_parser 直下で下記コマンドを実行）  
        `python3 parsers/server_log_parser.py -i data/0_server_log_20220728.txt -o 1_server_log_20220728.csv`
  - ③ 　**pm_log_parser.py**
    - `server_log_parser.py`でパースした csv を元に、PM に必要な[case_id, activity, timestamp]形式にパースした csv ファイルを作成するスクリプト.
    - 変換元の csv ファイル path と出力先の path をコマンド引数として受け取る
      - demo command（log_parser 直下で下記コマンドを実行）  
        `python3 parsers/pm_log_parser.py -i data/1_server_log_20220728.csv -o 2_server_log_20220728.csv`

## メインスクリプトの説明

### サーバーログパーサー ラッパー

- **server_log_wrapper.py**
  - server_log_parser.py と pm_log_parser.py をラップするスクリプト.
  - tcpdump の出力 txt ファイル（0*）を入力として受け取り、csv 変換（1*）と PM 用 csv データ（2\_）を同時に作成.
    - demo command（log_parser 直下で下記コマンドを実行）  
       `python3 server_log_wrapper.py -i data/server_log_20220728.txt -o data/server_log_20220728.csv`
