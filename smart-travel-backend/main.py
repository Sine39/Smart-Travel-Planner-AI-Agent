from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from services.gpt_service import generate_trip_plan
from services.weather_service import get_weather
from services.spot_service import get_spots
from services.router_service import choose_tools
from services.llm_router import choose_tools_by_llm
from services.parser_service import parse_user_request
from services.tools import TOOLS
import json
from services.weather_forecast import get_trip_weather

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# 请求模型
class TripRequest(BaseModel):
    destination: str
    budget: float
    start_date: str
    days: int
    user_input: str

@app.get("/hello")
def hello():
    return {"message": "Hello World"}

@app.post("/plan-trip")
def plan_trip(req: TripRequest):

    print("收到请求：", req)

    # 1. 查询未来天气
    weather_info = get_trip_weather(
        req.destination,
        req.start_date,
        req.days
    )

    print("天气预报：", weather_info)

    # 2. 查询景点
    spots_info = get_spots(req.destination)

    print("景点信息：", spots_info)

    # 3. 调用AI生成旅行方案
    trip_summary = generate_trip_plan(
        req.destination,
        req.budget,
        req.days,
        weather_info,
        spots_info,
        req.user_input
    )

    # 4. 生成天气穿搭总结
    weather_advice = ""

    if weather_info:

        temps = [item["temp"] for item in weather_info]

        min_temp = round(min(temps))
        max_temp = round(max(temps))

        clothes = list(
            set(
                item["clothes"]
                for item in weather_info
            )
        )

        weather_advice = (
            f"出行 {req.days} 天气温约 "
            f"{min_temp}℃ ~ {max_temp}℃，"
            f"建议穿着：{'、'.join(clothes)}。"
        )

    # 5. 返回给前端
    return {
        "weather_forecast": weather_info,
        "weather_advice": weather_advice,

        "spots": trip_summary.get("spots", ""),
        "foods": trip_summary.get("foods", ""),
        "tips": trip_summary.get("tips", ""),

        "itinerary": trip_summary.get(
            "itinerary",
            []
        )
    }

@app.get("/weather")
def weather():

    result = get_weather("Tokyo")

    return {
        "weather": result
    }