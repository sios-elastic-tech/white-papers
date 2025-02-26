import os

import streamlit as st
from dotenv import load_dotenv
from elastic.es_func import create_es_client, create_search_params, es_search_template
from llm.llm_base import LlmBase
from llm.llm_wrapper import create_llm_base

from common_logger import CommonLogger

#
# Copyright (c) SIOS Technology, Inc. All rights reserved.
# 
# MIT License
# 


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
    return ''
  else:
    es_client = create_es_client(elasticsearch_endpoint, read_api_key_encoded)

    logger.debug(f'{es_client.info()=}')
    return es_client


def initialize_llm_base():
  """
  LLM の初期化を行う。
  """
  llm_api_key: str = ''
  llm_model_id: str = ''

  if load_dotenv(verbose=True):
    logger.debug('load_dotenv success')

  if 'llm_api_key' in os.environ:
    llm_api_key = os.environ['llm_api_key']

  if 'llm_model_id' in os.environ:
    llm_model_id = os.environ['llm_model_id']

  llm_base: LlmBase = create_llm_base(api_key=llm_api_key, model_id=llm_model_id)

  return llm_base


def search(query):
  """
  質問が入力された後に呼ばれる検索処理。
  (Elasticsearch へ検索を依頼する)
  """
  es_client = st.session_state['es_client']

  # 検索用パラメタを生成する。
  search_params = create_search_params(query)

  # 検索テンプレートを使って検索する。
  search_results = es_search_template(es_client, search_params)

  logger.debug('----- 検索結果 -----')
  for i, results in enumerate(search_results):
    logger.debug(f'{i}')
    for sub_result in results:
      logger.debug(f'{sub_result}')

  return search_results


def question_to_llm(question, search_results):
  """
  検索結果を情報源としてLLMへ問い合わせる。
  """
  # LLM に問い合わせる。
  llm_base: LlmBase = st.session_state['llm_base']
  response = llm_base.request_to_llm(question=question, search_results=search_results)

  # for debug (LLMの結果)
  logger.debug('----- LLMからのレスポンス -----')
  for r in response:
    logger.debug(r)

  answer = llm_base.retrieve_answer(response=response)

  return answer


def show_ui(prompt_to_user='質問を入力してください。'):
  """
  画面の表示
  """
  st.set_page_config(page_title='柿之助 RAG')
  st.title('柿之助 RAG')

  if 'messages' not in st.session_state.keys():
    st.session_state.messages = [{'role': 'assistant', 'content': prompt_to_user}]

  # Display chat messages
  for message in st.session_state.messages:
    with st.chat_message(message['role']):
      st.write(message['content'])

  # 1. ユーザーからの質問を受け付ける。
  if query := st.chat_input():
    with st.chat_message('user'):
      st.write(query)
    st.session_state.messages.append({'role': 'user', 'content': query})

    # Generate a new response if last message is not from assistant
    if st.session_state.messages[-1]['role'] != 'assistant':
      with st.chat_message('assistant'):
        with st.spinner('Thinking...'):
          # 2. Elasticsearch へ問い合わせ / 3.検索結果の受け取り
          search_results = search(query)

          # 4. LLM へ問い合わせ / 5. 回答結果の受け取り
          answer = question_to_llm(query, search_results)

          print(type(answer))

          # 6. 回答結果の表示
          st.markdown(answer)

          # if type(answer) == Message:
          #   message = answer
          # else:
          message = {'role': 'assistant', 'content': answer}
          st.session_state.messages.append(message)


# ----- main -----
if 'es_client' not in st.session_state:
  es_client = initialize_es()
  st.session_state['es_client'] = es_client

if 'llm_base' not in st.session_state:
  llm_base = initialize_llm_base()
  st.session_state['llm_base'] = llm_base

show_ui()
