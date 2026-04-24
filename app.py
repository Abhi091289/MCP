import streamlit as st
import asyncio
import json
import pandas as pd
import matplotlib.pyplot as plt
from fastmcp import Client

st.set_page_config(page_title="Brand Comparison", layout="centered")

st.title("👟 Nike vs Puma Comparison")

# ----------- ANALYSIS FUNCTION -----------
def analyze(data):
    prices, ratings = [], []

    for item in data:
        # Price
        if item.get("price"):
            try:
                prices.append(float(item["price"].replace("$", "").replace(",", "")))
            except:
                pass

        # Rating
        if item.get("rating") is not None:
            try:
                ratings.append(float(item["rating"]))
            except:
                pass

    avg_price = sum(prices) / len(prices) if prices else 0
    avg_rating = sum(ratings) / len(ratings) if ratings else 0

    return avg_price, avg_rating


# ----------- BUTTON -----------
if st.button("Compare Brands"):

    async def run():
        async with Client("compare_server.py") as client:
            nike_raw = await client.call_tool("get_brand_data", {"brand_name": "nike"})
            puma_raw = await client.call_tool("get_brand_data", {"brand_name": "puma"})

            nike_data = json.loads(nike_raw.content[0].text)
            puma_data = json.loads(puma_raw.content[0].text)

            return nike_data, puma_data

    nike_data, puma_data = asyncio.run(run())

    nike_df = pd.DataFrame(nike_data)
    puma_df = pd.DataFrame(puma_data)

    # -------- TABLES --------
    st.subheader("Nike Data")
    st.dataframe(nike_df)

    st.subheader("Puma Data")
    st.dataframe(puma_df)

    # -------- ANALYSIS --------
    nike_price, nike_rating = analyze(nike_data)
    puma_price, puma_rating = analyze(puma_data)

    # -------- METRICS --------
    st.subheader("Comparison Summary")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Nike Avg Price", f"${nike_price:.2f}")
        st.metric("Nike Avg Rating", f"{nike_rating:.2f}")

    with col2:
        st.metric("Puma Avg Price", f"${puma_price:.2f}")
        st.metric("Puma Avg Rating", f"{puma_rating:.2f}")

    # -------- GRAPH 1 --------
    st.subheader("Average Price Comparison")
    fig1, ax1 = plt.subplots()
    ax1.bar(["Nike", "Puma"], [nike_price, puma_price])
    st.pyplot(fig1)

    # -------- GRAPH 2 --------
    st.subheader("Average Rating Comparison")
    fig2, ax2 = plt.subplots()
    ax2.bar(["Nike", "Puma"], [nike_rating, puma_rating])
    st.pyplot(fig2)

    # -------- PRICE DISTRIBUTION --------
    nike_prices = [float(x["price"].replace("$", "")) for x in nike_data if x.get("price")]
    puma_prices = [float(x["price"].replace("$", "")) for x in puma_data if x.get("price")]

    fig3, ax3 = plt.subplots()
    ax3.hist(nike_prices, alpha=0.5, label="Nike")
    ax3.hist(puma_prices, alpha=0.5, label="Puma")
    ax3.legend()
    st.pyplot(fig3)

    # -------- RATING DISTRIBUTION --------
    nike_ratings = [x["rating"] for x in nike_data if x.get("rating")]
    puma_ratings = [x["rating"] for x in puma_data if x.get("rating")]

    fig4, ax4 = plt.subplots()
    ax4.hist(nike_ratings, alpha=0.5, label="Nike")
    ax4.hist(puma_ratings, alpha=0.5, label="Puma")
    ax4.legend()
    st.pyplot(fig4)

    # -------- TOP PRODUCTS --------
    st.subheader("Top Rated Products")

    nike_top = sorted(nike_data, key=lambda x: x.get("rating") or 0, reverse=True)[:5]
    puma_top = sorted(puma_data, key=lambda x: x.get("rating") or 0, reverse=True)[:5]

    st.write("Top Nike Products")
    st.dataframe(pd.DataFrame(nike_top))

    st.write("Top Puma Products")
    st.dataframe(pd.DataFrame(puma_top))