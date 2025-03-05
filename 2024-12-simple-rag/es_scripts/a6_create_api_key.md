# 読み取り専用の API Key の作成

```
POST /_security/api_key
{
  "name": "kakinosuke_read_api_key",
  "role_descriptors": {
    "kakinosuke_api_key": {
      "cluster": ["all"],
      "indices": [
        {
          "names": ["kakinosuke*"],
          "privileges": ["read"]
        }
      ]
    }
  }
}
```
