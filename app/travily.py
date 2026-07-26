from langchain_tavily import TavilySearch
from app.config import TAVILY_API_KEY 

tool = TavilySearch(
    tavily_api_key=TAVILY_API_KEY,
    max_results=5,
)