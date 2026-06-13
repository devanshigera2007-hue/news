import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# -----------------------------
# CONFIG
# -----------------------------
API_KEY = "df63bd871eb24da6ae2c6005f8f23f54"
BASE_URL = "https://newsapi.org/v2/top-headlines"

st.set_page_config(
    page_title="Advanced News Dashboard",
    page_icon="📰",
    layout="wide"
)

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.title("⚙️ News Filters")

countries = {
    "India": "in",
    "United States": "us",
    "United Kingdom": "gb",
    "Australia": "au",
    "Canada": "ca",
    "Germany": "de",
    "France": "fr",
    "Japan": "jp"
}

categories = [
    "general",
    "business",
    "entertainment",
    "health",
    "science",
    "sports",
    "technology"
]

selected_country = st.sidebar.selectbox(
    "Select Country",
    list(countries.keys())
)

selected_category = st.sidebar.selectbox(
    "Select Topic",
    categories
)

keyword = st.sidebar.text_input(
    "Search Keyword",
    placeholder="AI, Cricket, Tesla..."
)

article_count = st.sidebar.slider(
    "Number of Articles",
    min_value=5,
    max_value=50,
    value=15
)

refresh = st.sidebar.button("🔄 Refresh News")

# -----------------------------
# NEWS FETCHER
# -----------------------------
@st.cache_data(ttl=300)
def fetch_news(country, category, keyword, page_size):
    params = {
        "apiKey": API_KEY,
        "country": country,
        "category": category,
        "pageSize": page_size
    }

    if keyword:
        params["q"] = keyword

    try:
        response = requests.get(
            BASE_URL,
            params=params,
            timeout=15
        )

        response.raise_for_status()

        data = response.json()

        if data["status"] == "ok":
            return data["articles"]

        return []

    except Exception as e:
        st.error(f"Error fetching news: {e}")
        return []

# Clear cache on refresh
if refresh:
    st.cache_data.clear()

# -----------------------------
# HEADER
# -----------------------------
st.title("📰 Advanced News Dashboard")
st.markdown(
    "Browse top headlines by location, category, and keywords."
)

# -----------------------------
# FETCH DATA
# -----------------------------
articles = fetch_news(
    countries[selected_country],
    selected_category,
    keyword,
    article_count
)

# -----------------------------
# SUMMARY METRICS
# -----------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Country", selected_country)

with col2:
    st.metric("Category", selected_category.title())

with col3:
    st.metric("Articles Found", len(articles))

st.divider()

# -----------------------------
# ARTICLES DISPLAY
# -----------------------------
if articles:

    for idx, article in enumerate(articles, start=1):

        title = article.get("title", "No Title")
        source = article.get("source", {}).get("name", "Unknown")
        desc = article.get("description", "")
        url = article.get("url", "")
        image = article.get("urlToImage")
        published = article.get("publishedAt", "")

        with st.container():

            col1, col2 = st.columns([1, 3])

            with col1:
                if image:
                    st.image(image, use_container_width=True)

            with col2:
                st.subheader(f"{idx}. {title}")

                st.caption(
                    f"Source: {source} | Published: {published}"
                )

                if desc:
                    st.write(desc)

                st.link_button(
                    "Read Full Article",
                    url
                )

            st.divider()

else:
    st.warning("No articles found. Try changing filters.")