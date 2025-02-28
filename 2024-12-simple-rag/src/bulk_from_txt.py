"""
Copyright (c) SIOS Technology, Inc. All rights reserved.

MIT License

text を読み込んで、bulk により 文章と登録するツール

usage: python bulk_from_txt.py chunked_textfilepath

登録先のindex名などは、es_consts.py に記載しておく。
"""

import os
import sys

from dotenv import load_dotenv
from elastic.es_consts import INGEST_PIPELINE, SEARCH_INDEX
from elastic.es_func import create_es_client, refresh_index, streaming_bulk_wrapper

from common_logger import CommonLogger


logger = CommonLogger(__name__)


def initialize_es():
  """
  Elasticsearchの初期化を行う。
  """
  elasticsearch_endpoint: str = ''
  write_api_key_encoded: str = ''

  if load_dotenv(verbose=True):
    logger.debug('load_dotenv success')

    if 'elasticsearch_endpoint' in os.environ:
      elasticsearch_endpoint = os.environ['elasticsearch_endpoint']

      if 'write_api_key_encoded' in os.environ:
        write_api_key_encoded = os.environ['write_api_key_encoded']

  if write_api_key_encoded == '':
    print('please set elasticsearch_endpoint and write_api_key_encoded in .env')
    logger.error('please set elasticsearch_endpoint and write_api_key_encoded in .env')
    return None
  else:
    es_client = create_es_client(elasticsearch_endpoint, write_api_key_encoded)
    logger.debug(f'{es_client.info()=}')

    return es_client


def data_generator(input_file, index_name = SEARCH_INDEX, ingest_pipeline_name = INGEST_PIPELINE):
    chunk_no :int = 0

    for content in input_file:
        # 末尾の改行文字を削除する。
        line_content = content.rstrip('\r\n')

        doc = {
            'chunk_no': chunk_no,
            'content': f"{line_content}"
        }

        chunk_no += 1

        # 1行ずつ処理する。
        yield {
            '_index': index_name,
            'pipeline': ingest_pipeline_name,
            '_source': doc
        }


def bulk_from_file(es_client, input_text_filename:str, index_name=SEARCH_INDEX, refresh=False):
    """
    1つのtextファイルを1行ずつ読み込んで、elasticsearch にドキュメント登録する。
    (streaming_bulk を使用する)
    
    example of streaming_bulk
    https://www.programcreek.com/python/example/104890/elasticsearch.helpers.streaming_bulk
    """

    with open(file=input_text_filename, buffering=-1, encoding="utf-8") as input_file:

        # debug
        # for line in data_generator(input_file):
        #    print(line)
  
        success_count = streaming_bulk_wrapper(es_client=es_client, actions=data_generator(input_file))
        print(f'{success_count=}')
        # logger.info(f'{success_count=}')
        
        if refresh and success_count > 0:
            refresh_index(es_client, index_name=index_name)


# ----- main -----
es_client = initialize_es()

if es_client is None:
   print('Initialize is failed.')
   exit()

args: list[str] = sys.argv

text_filepath: str = args[1]

bulk_from_file(es_client=es_client, input_text_filename=text_filepath, index_name=SEARCH_INDEX, refresh=True)
