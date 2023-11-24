import requests
import json

url = "http://pcv-test-chatglm.wps.cn/v1/chat/completions"

payload = json.dumps({
  "stream": False,
  "temperature": 0.5,
  "messages": [
    {
      "role": "system",
      "content": "你的任务是帮我区分以下文本是否与翻译相关，如果是则输出1，否则输出0"
    },
    {
      "role": "user",
      "content": "帮我翻译这句话"
    },
    {
      "role": "assistant",
      "content": "1"
    },
    {
      "role": "user",
      "content": "我的爸爸是个"
    }
  ]
})
headers = {
  'Pcv-Client-Type': 'zhai',
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)