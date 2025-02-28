"""
Copyright (c) SIOS Technology, Inc. All rights reserved.

MIT License
"""

class LlmBase:
  """
  LLM 関連のクラスの基底クラス
  """
  def __init__(self):
    pass


  def create_llm(self, api_key, model_id):
    """
    Create LLM
    """
    return None


  def request_to_llm(self, question, search_results):
    """
    LLM に問い合わせる。
    """
    return None


  def retrieve_answer(self, response):
    """
    レスポンスから回答部分だけを抽出する。
    """
    return None
