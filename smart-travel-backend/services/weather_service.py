import requests

CITY_MAPPING = {
    "东京": "Tokyo",
    "北京": "Beijing",
    "上海": "Shanghai",
    "广州": "Guangzhou",
    "深圳": "Shenzhen",
    "首尔": "Seoul",
    "巴黎": "Paris",
    "伦敦": "London",
    "纽约": "New York"
}

API_KEY = "7a0ff8199b9dfabb135357b35e33dcb5"

def get_weather(city):

    city = CITY_MAPPING.get(city, city)

    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
        "lang": "zh_cn"
    }

    response = requests.get(url, params=params)

    data = response.json()

    print(data)

    # 错误处理
    if "weather" not in data:

        return f"天气查询失败：{data}"

    weather = data["weather"][0]["description"]

    temp = data["main"]["temp"]

    return f"{city}当前天气：{weather}，气温 {temp}°C"