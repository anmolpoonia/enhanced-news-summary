import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
from wordcloud import WordCloud
from prophet import Prophet
from transformers import pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import os
from collections import Counter

# Fetch news from VentureBeat
def fetch_latest_news():
    print("[INFO] Fetching news from VentureBeat...")
    url = "https://venturebeat.com/"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"[ERROR] Failed to fetch news. HTTP Status Code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    articles = []
    for item in soup.find_all("article")[:5]:  # Fetch top 5 articles
        try:
            title = item.find("h2").get_text(strip=True)
            link = item.find("a")["href"]
            articles.append({"title": title, "link": link})
        except AttributeError:
            print("[WARNING] Skipping an article due to missing data.")
    print(f"[INFO] Fetched {len(articles)} articles.")
    return articles

# Fetch news from NewsAPI
def fetch_newsapi_news():
    print("[INFO] Fetching news from NewsAPI...")
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        "apiKey": "521d26b995c14f5ba0ccb34a4090a622",
        "sources": "techcrunch,reuters",
        "pageSize": 5,
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"[ERROR] Failed to fetch news from NewsAPI. HTTP Status Code: {response.status_code}")
        return []

    articles = response.json().get("articles", [])
    newsapi_articles = [{"title": a["title"], "link": a["url"]} for a in articles]
    print(f"[INFO] Fetched {len(newsapi_articles)} articles from NewsAPI.")
    return newsapi_articles

# Combine news from multiple sources
def fetch_combined_news():
    venturebeat_news = fetch_latest_news()
    newsapi_news = fetch_newsapi_news()
    return venturebeat_news + newsapi_news

# Summarize news articles
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
def summarize_text(text):
    input_length = len(text.split())
    if input_length < 8:  # Skip summarization for very short titles
        return text
    max_length = min(100, input_length + 5)
    return summarizer(text, max_length=max_length, min_length=5, do_sample=False)[0]["summary_text"]



# Generate a word cloud
def generate_word_cloud(articles):
    text = " ".join(article["title"] for article in articles)
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)
    wordcloud.to_file("word_cloud.png")
    print("[INFO] Word cloud generated: word_cloud.png")

# Save news history
def save_to_history(news, file_path="news_history.csv"):
    if not os.path.exists(file_path):
        pd.DataFrame(columns=["date", "title", "sentiment", "link"]).to_csv(file_path, index=False)
    df = pd.read_csv(file_path)
    new_data = pd.DataFrame([{
        "date": datetime.now().strftime("%Y-%m-%d"),
        "title": article["title"],
        "sentiment": article.get("sentiment", "Neutral"),
        "link": article["link"]
    } for article in news])
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv(file_path, index=False)
    print("[INFO] News history saved: news_history.csv")

# Forecast sentiment trends
def forecast_sentiment(file_path="news_history.csv"):
    df = pd.read_csv(file_path)
    sentiment_counts = df.groupby("date")["sentiment"].value_counts().unstack(fill_value=0).reset_index()
    if "Positive" not in sentiment_counts.columns:
        sentiment_counts["Positive"] = 0
    sentiment_counts = sentiment_counts.rename(columns={"date": "ds", "Positive": "y"})
    sentiment_counts["ds"] = pd.to_datetime(sentiment_counts["ds"])
    if len(sentiment_counts) < 2:
        print("[WARNING] Not enough data for sentiment forecasting. Skipping...")
        return

    model = Prophet()
    model.fit(sentiment_counts)
    future = model.make_future_dataframe(periods=7)
    forecast = model.predict(future)
    forecast.to_csv("sentiment_forecast.csv", index=False)
    print("[INFO] Sentiment forecast saved: sentiment_forecast.csv")

# Generate leaderboard
def generate_leaderboard(file_path="news_history.csv"):
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        print("[WARNING] News history file is empty. Skipping leaderboard generation.")
        return

    df = pd.read_csv(file_path)
    all_titles = " ".join(df["title"])
    word_counts = Counter(all_titles.split())
    most_common_words = word_counts.most_common(5)

    with open("leaderboard.txt", "w") as file:
        file.write("Top 5 Words in News Titles:\n")
        for word, count in most_common_words:
            file.write(f"{word}: {count} mentions\n")
    print("[INFO] Leaderboard generated: leaderboard.txt")

# Save news summary to a file
def save_to_file(articles):
    with open("news_summary.txt", "w") as file:
        file.write(f"Daily News Summary - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        file.write("=" * 50 + "\n\n")
        for i, article in enumerate(articles, 1):
            file.write(f"{i}. {article['title']}\n")
            file.write(f"Link: {article['link']}\n\n")
    print("[INFO] File news_summary.txt generated successfully.")

# Main function
if __name__ == "__main__":
    news = fetch_combined_news()
    for article in news:
        article["summary"] = summarize_text(article["title"])
    generate_word_cloud(news)
    save_to_history(news)
    forecast_sentiment()
    generate_leaderboard()
    save_to_file(news)
    print("[INFO] Script completed.")
