from services.weather_service import get_weather


def get_spots(destination):

    return f"""
推荐景点：

1. 浅草寺
2. 秋叶原
3. 上野公园
4. 涩谷
5. 新宿御苑
"""


def get_foods(destination):

    return f"""
推荐美食：

1. 一兰拉面
2. 吉野家牛丼
3. 回转寿司
4. 便利店便当
"""


TOOLS = {
    "weather": get_weather,
    "spots": get_spots,
    "foods": get_foods
}