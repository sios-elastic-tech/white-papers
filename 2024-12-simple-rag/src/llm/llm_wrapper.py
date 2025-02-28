"""
Copyright (c) SIOS Technology, Inc. All rights reserved.

MIT License
"""

from llm.cohere.cohere import Cohere
from llm.llm_base import LlmBase
from llm.llm_consts import COHERE_COMMAND_R, COHERE_COMMAND_R_PLUS


def create_llm_base(api_key, model_id):
  """
  Create LLM Base.
  将来的にモデルを変更可能としておく。
  """
  llm_base: LlmBase

  if model_id == COHERE_COMMAND_R or model_id == COHERE_COMMAND_R_PLUS:
    llm_base = Cohere()
  else:
    print('実装してください。')
    llm_base = LlmBase()

  llm_base.llm = llm_base.create_llm(api_key=api_key, model_id=model_id)

  return llm_base
