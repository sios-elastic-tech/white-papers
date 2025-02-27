# Elasticsearchを使った簡易RAGアプリケーション

## 概要

「Elasticsearchを使った簡易RAGアプリケーションの作成」
のホワイトペーパー用に作成した簡易RAGアプリケーションです。

※注 ホワイトペーパー内に記載したソースとほぼ同じですが、細部は若干修正が入っています。

## できること

1. テキストファイルを読み込んで、チャンキングを行う。

2. テキストファイルを読み込んで、1行ずつ Elasticsearch のインデックスへ登録する。

3. Streamlit と Elasticsearch を使って、ハイブリッド検索を行う。

4. Streamlit, Elasticsearch, Cohere Command R を使って、RAG を行う。

## 動作に必要な環境など

- Elastic Cloud (筆者は Enterprise Edition v8.17.0 で動作確認)
- Docker
- Cohere (Trial Key で可)

その他、下記のライブラリは、自動でダウンロードされます。

- Python 3.12
- elasticsearch 8.15.0 (Elasticsearch の Python用のClient)
- streamlit 1.39.0
- langchain-cohere 0.3.1
- python-dotenv 1.0.1


## 動かし方

### 1. 準備

#### 1.1. Elastic Cloud 上での準備

- デプロイメントの作成

- 日本語用の形態素解析の準備

- 日本語用の密ベクトルの生成準備

- インデックスの作成

詳細は、https://elastic.sios.jp/whitepaper/ の
「Elasticsearchを使った簡易RAGアプリケーションの作成」を参照してください。


#### 1.2. .env ファイルに動作に必要な情報を記載する。

```
elasticsearch_endpoint='...'

read_api_key_encoded='...'

write_api_key_encoded='...'

llm_api_key='...'

llm_model_id='...'
```


### 2. ビルド ～ コンテナ内での bash の実行

#### 2.1. ビルド

docker-compose.yml があるディレクトリで下記を実行する。

```docker compose build```

#### 2.2. コンテナの起動

```docker compose up -d```

#### 2.3. コンテナ内で bash を実行

```docker exec -it sios_es_sample_202412 /bin/bash```

("sios_es_sample_202412"はコンテナ名)




### 3. Elasticsearch へのデータ登録

さきほど実行開始した bash から以下のコマンドを実行する。

#### 3.1. チャンキングを行う。

```python src/split_txt.py data/kakinosuke.txt 200 50```

チャンキングに成功すると、data/kakinosuke.txt_chunked.txt ファイルが生成されます。

#### 3.2. チャンクされたデータをインデックスへ登録する。

チャンクされたデータを指定したインデックス("kakinosuke")へ登録する。

```python src/bulk_from_txt.py data/kakinosuke.txt_chunked.txt```

正常終了すると、指定したインデックス("kakinosuke")に、ドキュメントが登録されます。

### 4. アプリの開始

#### 4.1. ハイブリッド検索アプリの開始

```streamlit run src/app_kakinosuke_search.py```

Web Browser から http://localhost:8501/ にアクセスして、ハイブリッド検索を行ってください。

※停止ボタンは用意していないので、停止させたい場合は、Ctrl+C を押す、あるいは、
ハイブリッド検索アプリのプロセスを停止させるなどの処置を行ってください。

#### 4.2. RAG アプリケーションの開始

```streamlit run src/app_kakinosuke_rag.py```

Web Browser から http://localhost:8501/ にアクセスして、RAGを行ってください。

※停止ボタンは用意していないので、停止させたい場合は、Ctrl+C を押す、あるいは、
ハイブリッド検索アプリのプロセスを停止させるなどの処置を行ってください。

## ファイルの説明

| 相対ファイルパス | 説明 |
|---|---|
| ./.env | 接続に必要な API Key などを記載するファイル |
| ./docker-compose.yml | Docker の Compose ファイル |
| ./Dockerfile | Docerfile |
| ./README.md | このファイル |
| ./requirements.txt | 動作に必要なライブラリの指定ファイル |
| data/kakinosuke.txt | 桃太郎を改変した柿之助のお話 |
| data/README.md | kakinosuke.txt の説明 |
| es_scripts/*.txt | Elasticsearch用の各種設定スクリプト |
| src/app_kakinosuke_rag.py | 柿之助のRAGアプリケーションの本体 |
| src/app_kakinosuke_search.py | 柿之助のハイブリッド検索アプリケーションの本体 |
| src/bulk_from_txt.py | テキストファイルを読み込んで、Elasticsearch へ データ登録するプログラム |
| src/common_logger.py | ロガー用関数 |
| src/consts.py | チャンクサイズの定義ファイル |
| src/split_txt.py | テキストファイルをチャンキングするプログラム |
| src/elastic/es_consts.py | Elasticsearch関連の定数定義ファイル |
| src/elastic/es_func.py | Elasticsearch関連の関数を集めたファイル |
| src/llm/llm_base.py | LLM関連の基底クラス |
| src/llm/llm_consts.py | LLM関連の定数定義ファイル |
| src/llm/llm_wapper.py | LLM関連の処理を呼び出すためのラッパー |
| src/llm/cohere/cohere.py | Cohere用のクラス |

