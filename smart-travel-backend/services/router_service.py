def choose_tools(user_input):

    tools = []

    # 天气相关
    if "天气" in user_input or "穿什么" in user_input:
        tools.append("weather")

    # 景点相关
    if "景点" in user_input or "去哪玩" in user_input:
        tools.append("spots")

    # 默认两个都开
    if len(tools) == 0:
        tools = ["weather", "spots"]

    return tools