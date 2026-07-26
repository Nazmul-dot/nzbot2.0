from langchain_core.tools import tool
from langchain_tavily import TavilySearch
from app.config import OPEN_WEATHER_API_KEY, TAVILY_API_KEY
import requests


# -----------------------------
# OpenWeather Tool
# -----------------------------

@tool
def get_weather(city: str) -> str:
    """
    Get current weather information for a city.
    Input should be a city name.
    """

    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": city,
        "appid": OPEN_WEATHER_API_KEY,
        "units": "metric"
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        return f"Could not fetch weather information for {city}"

    data = response.json()

    temperature = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    description = data["weather"][0]["description"]

    return (
        f"Weather in {city}: "
        f"{description}, "
        f"temperature {temperature}°C, "
        f"humidity {humidity}%."
    )


# -----------------------------
# Tavily Search Tool
# -----------------------------

tavily_search = TavilySearch(
    max_results=5,
    tavily_api_key=TAVILY_API_KEY
)


@tool
def web_search(query: str) -> str:
    """
    use this tool when you need to search the web for 
    current information or any unknown information.
    """

    results = tavily_search.invoke(query)

    return str(results)


tools = [
    get_weather,
    web_search
]
