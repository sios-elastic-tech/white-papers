"""
Copyright (c) SIOS Technology, Inc. All rights reserved.

MIT License
"""

import os

import streamlit as st
from dotenv import load_dotenv
from elastic.es_func import create_es_client, create_search_params, es_search_template

from common_logger import CommonLogger


highlight = True

logger = CommonLogger(__name__)


def initialize_es():
  """
  Elasticsearchの初期化を行う。
  """
  elasticsearch_endpoint: str = ''
  read_api_key_encoded: str = ''

  if load_dotenv(verbose=True):
    logger.debug('load_dotenv success')

    if 'elasticsearch_endpoint' in os.environ:
      elasticsearch_endpoint = os.environ['elasticsearch_endpoint']

    if 'read_api_key_encoded' in os.environ:
      read_api_key_encoded = os.environ['read_api_key_encoded']

  if read_api_key_encoded == '':
    logger.error('please set elasticsearch_endpoint and read_api_key_encoded in .env')
    return None
  else:
    es_client = create_es_client(elasticsearch_endpoint, read_api_key_encoded)
    logger.debug(f'{es_client.info()=}')

    return es_client


def search(query):
  """
  質問が入力された後に呼ばれる検索処理。
  (Elasticsearch へ検索を依頼する)
  """
  es_client = st.session_state['es_client']

  # 検索用パラメタを生成する。
  search_params = create_search_params(query, highlight)

  # 検索テンプレートを使って検索する。
  search_results = es_search_template(es_client, search_params)

  return search_results


def search_onclick():
  """
  検索ボタンが押された場合の処理
  """
  # 1. ユーザーからの質問を受けとる。
  query = st.session_state['query']
  st.write(query)

  # 2. Elasticsearch へ問い合わせ / 3. 検索結果の受け取り
  search_results = search(query)

  # 4. 検索結果の表示
  for i, results in enumerate(search_results):
    st.write(f'{i}')
    for sub_result in results:
      st.write(f'{sub_result}', unsafe_allow_html=True)


def show_ui():
  """
  画面の表示
  """
  st.set_page_config(page_title='柿之助 検索アプリ')
  st.text_input(label='クエリ', key='query')
  st.button(label='検索', on_click=search_onclick)


# ----- main -----
if 'es_client' not in st.session_state:
  es_client = initialize_es()
  
  if es_client is None:
    print('Initialize is failed.')
    exit()
  else:
    st.session_state['es_client'] = es_client

show_ui()
