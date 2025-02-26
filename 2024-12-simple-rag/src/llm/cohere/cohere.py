from typing import override

from langchain_cohere import ChatCohere, CohereRagRetriever
from langchain_core.documents import Document
from llm.llm_base import LlmBase

#
# Copyright (c) SIOS Technology, Inc. All rights reserved.
# 
# MIT License
# 


class Cohere(LlmBase):
  """
  Class for Cohere.
  """

  @override
  def create_llm(self, api_key, model_id):
    """
    Define the Cohere LLM
    """
    return ChatCohere(cohere_api_key=api_key, model=model_id)


  @override
  def request_to_llm(self, question, search_results):
    """
    LLM に問い合わせる。
    """
    documents = []
    for search_result in search_results:
      # search_result は配列で返ってくるが、
      # これまでに要素数>1の結果が返ってきたことはないので、先頭のみ参照する。
      documents.append(Document(page_content=search_result[0]))

    rag = CohereRagRetriever(llm=self.llm, connectors=[])
    response = rag.invoke(input=question, documents=documents)

    return response


  @override
  def retrieve_answer(self, response):
    """
    response から 回答を取り出す。
    Cohere の場合、response の最後の要素の page_content に回答が格納されている。
    なお、引用元は、citations に含まれている。
    """
    return response[-1].page_content

