# log_parser ディレクトリに関しての説明

## ディレクトリ構成

- data: 現状はデモデータを格納している
  - ① 　 GA 経由で取得した JPMT のログデータ（APMJ_Eventlogs_3.csv）
  - ② 　 server PC から取得した HTTP 通信のログデータ（severlog_20220719.txt）
- parser: 各 log データのパーサー
  - ① 　**ga_log_parser.py**
    - GA 経由で取得したデータをみんぷろに格納できる csv 形式に変換するスクリプト
    - 変換元の csv ファイル path と出力先の path をコマンド引数として受け取る
      - demo command（log_parser 直下で下記コマンドを実行）  
        `python3 parser/ga_log_parser.py -i data/APMJ_Eventlogs_3.csv -o APMJ_Eventlogs_3_processed.csv`
  - ② 　**serverlog_parser.py**
    - server PC から取得した HTTP ログデータから必要な情報をパースして csv に変換するスクリプト.
    - このままではみんぷろに入れられないため、別スクリプトを作成中
    - 変換元の csv ファイル path と出力先の path をコマンド引数として受け取る
      - demo command（log_parser 直下で下記コマンドを実行）  
        `python3 parser/serverlog_parser.py -i data/serverlog_20220719.txt -o serverlog_20220719.csv`
