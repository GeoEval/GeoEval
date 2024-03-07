import requests
import json

def get_chat_reponse(question):
    api_key = ''#
    url = "https://ai-proxy.ksord.com/wps.openai.azure.com/openai/deployments/35/chat/completions?api-version=2023-03-15-preview"
    headers = {
        "api-key": api_key,
        "Content-Type": "application/json"
    }
    data_templete = {
        "stream": False,
        "messages": [
            {
                "content": "{question}",
                "role": "system"
            }
        ],
        "frequency_penalty": 0,
        "temperature": 0.7,
        "presence_penalty": 0,
        "max_tokens": 1024,
        "top_p": 1
    }
    data_templete["messages"][0]["content"] = data_templete["messages"][0]["content"].format_map(dict(question=question))
    try:
        response = requests.post(url, headers=headers, json=data_templete)
        answer = response.json()['choices'][0]['message']['content']
    except:
        answer = 'Get Some Error During Process'
    return answer
