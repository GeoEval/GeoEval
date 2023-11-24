curl -X "POST" "https://ai-proxy.ksord.com/wps.openai.azure.com/openai/deployments/35/chat/completions?api-version=2023-03-15-preview" \
-H 'api-key: PX2bgbqP2MnUY3W8tqbVrxnJ7YwKeIWI' \
-H 'Content-Type: application/json' \
-d $'{
  "stream": false,
  "messages": [
    {
      "content": "你是一个翻译助手，翻译用户的中文到英文，每次回复前使用您好， 结尾用这个词讲个笑话",
      "role": "system"
    }
  ],
  "frequency_penalty": 0,
  "temperature": 0.7,
  "presence_penalty": 0,
  "max_tokens": 256,
  "top_p": 1
}'
