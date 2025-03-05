# インデックスのフィールドの作成

```
PUT /kakinosuke_v1/_mapping
{
  "dynamic": false,
  "properties": {
    "chunk_no": {
      "type": "integer"     
    },
    "content": {
      "type": "text",
      "analyzer": "ja_kuromoji_index_analyzer",
      "search_analyzer": "ja_kuromoji_search_analyzer"
    },
    "text_embedding": {
      "properties": {
        "model_id": {
          "type": "keyword",
          "ignore_above": 256
        },
        "predicted_value": {
          "type": "dense_vector",
          "dims": 384
        }
      }
    }
  }
}
```
