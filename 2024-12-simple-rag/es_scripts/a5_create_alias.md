# エイリアスの作成

```
POST _aliases
{
  "actions": [
    {
      "add": {
        "index": "kakinosuke_v1",
        "alias": "kakinosuke"
      }
    }
  ]
}
```
