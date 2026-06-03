from openai import OpenAI
import json

client = OpenAI(
    api_key="sk-01a25a894d7b4703a4c2a6ad0ac0dff9",
    base_url="https://api.deepseek.com"
)

def parse_user_request(user_input):

    prompt = f"""
你是一个旅行需求分析助手。

你需要从用户输入中提取：

1. destination
2. budget
3. days

只返回 JSON。

例如：

{{
  "destination": "东京",
  "budget": 3000,
  "days": 3
}}

用户输入：

{user_input}
"""

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    result = response.choices[0].message.content

    print("参数提取结果：", result)

    return json.loads(result)