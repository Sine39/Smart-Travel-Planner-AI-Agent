from openai import OpenAI
import json

client = OpenAI(
    api_key="sk-01a25a894d7b4703a4c2a6ad0ac0dff9",
    base_url="https://api.deepseek.com"
)

def choose_tools_by_llm(user_input):

    prompt = f"""
你是一个 AI Agent 工具路由器。

可用工具：

1.weather
作用：查询未来天气和穿搭建议

2.spots
作用：查询旅游景点

规则：

如果用户提到：

- 旅行
- 旅游
- 出行
- 攻略
- 行程
- 几日游
- 预算

返回：

["weather","spots"]

如果只问天气：

["weather"]

如果只问景点：

["spots"]

只返回 JSON 数组。
不要返回其它内容。

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

    print("LLM Router 返回：", result)

    try:
        return json.loads(result)
    except:
        return ["weather", "spots"]