import requests
from datetime import datetime, timedelta

API_KEY = "7a0ff8199b9dfabb135357b35e33dcb5"

#CITY_MAPPING = {
    #"东京": "Tokyo",
    #"北京": "Beijing",
    #"上海": "Shanghai",
    #"广州": "Guangzhou",
    #"深圳": "Shenzhen",
    #"首尔": "Seoul",
    #"巴黎": "Paris",
    #"伦敦": "London",
    #"纽约": "New York"
#}
def normalize_city(city):

    url = "http://api.openweathermap.org/geo/1.0/direct"

    params = {
        "q": city,
        "limit": 1,
        "appid": API_KEY
    }

    response = requests.get(url, params=params)

    data = response.json()

    print("Geo结果：", data)

    if len(data) == 0:
        return None

    return {
        "name": data[0]["name"],
        "lat": data[0]["lat"],
        "lon": data[0]["lon"]
    }

def get_forecast(city):

    city = normalize_city(city)
    #city = CITY_MAPPING.get(city, city)

    url = "https://api.openweathermap.org/data/2.5/forecast"

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
        "lang": "zh_cn"
    }

    response = requests.get(url, params=params)

    data = response.json()

    return data

def get_weather_icon(weather):

    weather = weather.lower()

    if "晴" in weather:
        return "☀️"

    if "雨" in weather:
        return "🌧️"

    if "雪" in weather:
        return "❄️"

    if "云" in weather:
        return "☁️"

    return "🌤️"

def get_clothes_advice(temp):

    if temp >= 30:
        return "短袖、短裤、防晒帽"

    elif temp >= 20:
        return "短袖+薄外套"

    elif temp >= 10:
        return "长袖、卫衣"

    else:
        return "羽绒服、围巾"

def get_trip_weather(city,start_date,days):
    location = normalize_city(city)

    if not location:
        return []

    lat = location["lat"]
    lon = location["lon"]

    print("纬度：", lat)
    print("经度：", lon)

    url = "https://api.openweathermap.org/data/2.5/forecast"
    print("查询城市：", city)
    params = {
        "lat": lat,
        "lon": lon,
        "appid": API_KEY,
        "units": "metric",
        "lang": "zh_cn"
    }

    response = requests.get(url, params=params)

    data = response.json()

    print(data)

    if "list" not in data:
        return []

    start = datetime.strptime(
    start_date,
    "%Y-%m-%d"
    )

    today = datetime.now()

    days_diff = (start - today).days

    # OpenWeather免费版只支持未来5天
    if days_diff > 5:
         return [
            {
            "date": start_date,
            "weather": "暂无天气数据",
            "temp": "--",
            "clothes": "天气服务仅支持未来5天预报"
        }
    ]

    result = []

    for i in range(days):

        target_day = (
            start + timedelta(days=i)
        ).strftime("%Y-%m-%d")

        day_weather = None

        for item in data["list"]:

            if item["dt_txt"].startswith(target_day):

                day_weather = item
                break

        if day_weather:

            temp = day_weather["main"]["temp"]
            feels_like = day_weather["main"]["feels_like"]
            result.append({
                "date": target_day,
                "weather": day_weather["weather"][0]["description"],
                "icon": get_weather_icon(
                    day_weather["weather"][0]["description"]
                ),
                "temp": temp,
                "feels_like": feels_like,
                "clothes": get_clothes_advice(temp)
            })

    return result