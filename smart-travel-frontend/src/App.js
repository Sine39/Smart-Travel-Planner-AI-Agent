import { useState } from "react";
import axios from "axios";

function App() {

  const [destination, setDestination] = useState("");
  const [budget, setBudget] = useState("");
  const [days, setDays] = useState("");
  const [userInput, setUserInput] = useState("");
  const [startDate, setStartDate] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
const selectedDate = new Date(startDate);
const today = new Date();

const diffDays =
  (selectedDate - today) / (1000 * 60 * 60 * 24);

if (diffDays > 5) {
  alert("天气预报目前仅支持未来5天");
  return;
}
  const handleSubmit = async () => {

    setLoading(true);

    const data = {
      destination,
      budget: Number(budget),
      start_date: startDate,
      days: Number(days),
      user_input: userInput
    };

    try {

      const response = await axios.post(
        "http://127.0.0.1:8000/plan-trip",
        data
      );

      setResult(response.data);

    } catch (error) {

      console.log(error);
      alert("请求失败");
    } finally {

    setLoading(false);
  }

  };

  return (

    <div className="min-h-screen bg-gray-100 p-6">

      <div className="grid grid-cols-4 gap-6">

        {/* 左侧输入区域 */}

        <div className="col-span-1 bg-white rounded-2xl shadow-lg p-6">

          <h1 className="text-3xl font-bold mb-6 text-blue-600">
            AI 智能出行
          </h1>

          <textarea
            className="w-full border border-gray-300 rounded-xl p-3 mb-4 focus:outline-none focus:ring-2 focus:ring-blue-400"
            rows={5}
            placeholder="请输入旅行需求...（例如：喜欢海边）"
            value={userInput}
            onChange={(e) => setUserInput(e.target.value)}
          />

          <input
            className="w-full border border-gray-300 rounded-xl p-3 mb-4"
            placeholder="目的地"
            value={destination}
            onChange={(e) => setDestination(e.target.value)}
          />

          <input
            className="w-full border border-gray-300 rounded-xl p-3 mb-4"
            placeholder="预算"
            value={budget}
            onChange={(e) => setBudget(e.target.value)}
          />
          <input
            type="date"
            className="w-full border border-gray-300 rounded-xl p-3 mb-4"
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
          />

          <input
            className="w-full border border-gray-300 rounded-xl p-3 mb-6"
            placeholder="出行天数"
            value={days}
            onChange={(e) => setDays(e.target.value)}
          />

          <button
            onClick={handleSubmit}
            className="w-full bg-blue-500 hover:bg-blue-600 text-white py-3 rounded-xl transition"
          >
            开始规划
          </button>
          {
          loading && (
            <div className="bg-blue-100 p-4 rounded-xl mb-4">
              AI 正在规划旅行，请稍候...
            </div>
          )
}

        </div>

        {/* 右侧内容 */}

        <div className="col-span-3 grid grid-cols-2 gap-6">

          {/* 天气 */}

          <div className="bg-white rounded-2xl shadow-lg p-6">

<h2 className="text-xl font-bold mb-4">
  🌤 天气与穿搭
</h2>

<p className="mb-4 text-gray-700">
  {result?.weather_advice || "等待生成旅行方案"}
</p>

<div className="flex gap-4 overflow-x-auto">

  {
    result?.weather_forecast?.map(
      (day, index) => (

<div
  key={index}
  className="min-w-[220px] bg-blue-50 rounded-xl p-4 shadow text-center flex flex-col items-center"
>

  <h3 className="font-bold text-lg mb-2">
    {day.date}
  </h3>

  <div className="text-4xl mb-3">
    {day.icon}
  </div>

  <p className="mb-2">
    {day.weather}
  </p>

  <p className="mb-1">
    🌡 气温：{day.temp}℃
  </p>

  <p className="mb-1">
    🤗 体感：{day.feels_like}℃
  </p>

  <p>
    👕 {day.clothes}
  </p>

</div>

      )
    )
  }

</div>

</div>

          {/* 景点 */}

          <div className="bg-white rounded-2xl shadow-lg p-6">

            <h2 className="text-xl font-bold mb-4">
              🗺 推荐景点
            </h2>

            <p className="text-gray-700 leading-7">
              {result?.spots || "等待生成旅行方案"}
            </p>

          </div>

          {/* 美食 */}

          <div className="bg-white rounded-2xl shadow-lg p-6">

            <h2 className="text-xl font-bold mb-4">
              🍜 美食推荐
            </h2>

            <p className="text-gray-700 leading-7">
              {result?.foods || "等待生成旅行方案"}
            </p>

          </div>

          {/* 注意事项 */}

          <div className="bg-white rounded-2xl shadow-lg p-6">

            <h2 className="text-xl font-bold mb-4">
              ⚠ 注意事项
            </h2>

            <p className="text-gray-700 leading-7">
              {result?.tips || "等待生成旅行方案"}
            </p>

          </div>

          <div className="col-span-2 bg-white rounded-2xl shadow-lg p-6">
            

  <h2 className="text-2xl font-bold mb-6">
    🗓 行程安排
  </h2>

  {
  result?.itinerary?.map((item,index)=>(

    <div
      key={index}
      className="bg-gray-50 rounded-xl p-6 mb-6"
    >

      <h3 className="text-xl font-bold mb-4 text-blue-600">
        {item.day}
      </h3>

      {
        item.plans.map((plan,i)=>(

          <div
            key={i}
            className="flex items-start mb-4"
          >

            <div className="flex flex-col items-center mr-4">

              <div
                className="
                w-4
                h-4
                bg-blue-500
                rounded-full
                "
              />

              {
                i !== item.plans.length - 1 &&
                <div className="w-1 h-10 bg-blue-200" />
              }

            </div>

            <div>

              <p className="text-gray-700">
                {plan}
              </p>

            </div>

          </div>

        ))
      }

    </div>

  ))
}

</div>

        </div>

      </div>

    </div>

  );
}

export default App;