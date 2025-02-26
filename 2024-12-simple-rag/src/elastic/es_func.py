from elastic.es_consts import SEARCH_INDEX, SEARCH_TEMPLATE_ID
from elasticsearch import Elasticsearch, helpers
from common_logger import CommonLogger

#
# Copyright (c) SIOS Technology, Inc. All rights reserved.
# 
# MIT License
# 


def create_es_client(elasticsearch_endpoint, api_key_encoded):
  """
  Elasticsearch へアクセスするための client を生成する。
  """
  es_client: Elasticsearch = None
  if elasticsearch_endpoint != '' and api_key_encoded != '':
    es_client = Elasticsearch(hosts=elasticsearch_endpoint, api_key=api_key_encoded)
  return es_client


def streaming_bulk_wrapper(es_client, actions):
  """
  bulk を使って、データを投入する。
  """
  success_count: int = 0
  for response in helpers.streaming_bulk(client=es_client, actions=actions):
    if response[0]:
      success_count += 1

  return success_count



def refresh_index(es_client, index_name=SEARCH_INDEX):
  """
  bulk 後などに、refresh を呼び出す。
  """
  es_client.indices.refresh(index=index_name)



def create_search_params(query, highlight=False):
  """
  検索テンプレートに埋め込むパラメタを生成する。
  """
  search_params = {
      'query_string': query,
      'query_for_vector': query,
      'highlight': highlight
  }

  return search_params


def es_search_template(es_client, search_params, search_index=SEARCH_INDEX, search_template_id=SEARCH_TEMPLATE_ID,
                       field_name='content', max_count=5):
  """
  検索テンプレートを使って、検索を行う。
  """
  results = []
  search_results = es_client.search_template(index=search_index, id=search_template_id,
                                             params=search_params)

  logger = CommonLogger(__name__)
  logger.debug('-----')

  if search_params['highlight']:
    for doc in search_results['hits']['hits'][:max_count]:
      # print(f'{doc=}')
      logger.debug(f'{doc=}')
      if 'highlight' in doc:
        results.append(doc['highlight'][field_name])
      else:
        results.append(doc['fields'][field_name])
  else:
    for doc in search_results['hits']['hits'][:max_count]:
      # print(f'{doc=}')
      logger.debug(f'{doc=}')
      results.append(doc['fields'][field_name])

  return results
