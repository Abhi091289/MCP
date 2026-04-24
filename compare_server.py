import os
from dotenv import load_dotenv
from fastmcp import FastMCP
from serpapi.google_search import GoogleSearch

load_dotenv()

SERP_API_KEY = os.getenv("SERP_API_KEY")

mcp = FastMCP("Brand Comparison Server")


@mcp.tool()
def get_brand_data(brand_name: str, product_type: str = "shoes") -> list:
    """
    Fetch product data from Google Shopping using SerpAPI
    """

    params = {
        "engine": "google_shopping",
        "q": f"{brand_name} {product_type}",
        "api_key": SERP_API_KEY,
        "num": 5
    }

    search = GoogleSearch(params)
    results = search.get_dict().get("shopping_results", [])

    cleaned = []
    for r in results:
        cleaned.append({
            "title": r.get("title"),
            "price": r.get("price"),
            "rating": r.get("rating")
        })

    return cleaned


if __name__ == "__main__":
    mcp.run()