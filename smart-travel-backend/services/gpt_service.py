from openai import OpenAI
import json

client = OpenAI(
    api_key="sk-01a25a894d7b4703a4c2a6ad0ac0dff9",
    base_url="https://api.deepseek.com"
)

def generate_trip_plan(
    destination,
    budget,
    days,
    weather_info,
    spots_info,
    user_input
):

    prompt = f"""
你是一名专业旅行规划师。

请为用户生成旅行方案。

用户信息：

目的地：{destination}
预算：{budget}
天数：{days}
用户特殊需求：
{user_input}
天气信息：
{weather_info}

景点信息：
{spots_info}

你必须：
1. 仅返回 JSON
2. 不要返回 markdown
3. 不要返回 ```json
4. 不要添加解释
请严格返回 JSON：

{{
  "weather": "",
  "spots": "",
  "foods": "",
  "tips": "",
  "itinerary": [
    {{
      "day": "Day1",
      "plans": [
        "09:00 浅草寺",
        "12:00 一兰拉面",
        "15:00 秋叶原"
      ]
    }}
  ]
}}
"""

    response = client.chat.completions.create(
        model="deepseek-v4-flash",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    content = response.choices[0].message.content

    print(content)
    try:

        content = content.replace("```json", "")
        content = content.replace("```", "")
        content = content.strip()

        return json.loads(content)

    except Exception as e:

        print("JSON解析失败：", e)

        return {
            "weather": weather_info,
            "spots": spots_info,
            "foods": "暂无美食推荐",
            "tips": "AI 返回格式异常",
            "itinerary": []
        }