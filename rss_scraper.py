import feedparser
import json
import csv
from datetime import datetime

# List of RSS Feeds
RSS_FEEDS = {
    "technology": "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml",
    "finance": "https://www.bloomberg.com/feeds/bbiz.xml",
    "sports": "https://www.espn.com/espn/rss/news",
    "entertainment": "https://www.hollywoodreporter.com/t/rss/",
    "science": "https://www.sciencenews.org/feed"
}

# Function to fetch and parse RSS feeds
def fetch_rss_data():
    articles = []
    
    for category, url in RSS_FEEDS.items():
        feed = feedparser.parse(url)
        for entry in feed.entries:
            articles.append({
                "title": entry.title,
                "link": entry.link,
                "published": entry.published if "published" in entry else "Unknown",
                "category": category
            })
    
    return articles

# Save data to JSON
def save_to_json(articles, filename="news_data.json"):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(articles, file, indent=4)

# Save data to CSV
def save_to_csv(articles, filename="news_data.csv"):
    keys = articles[0].keys() if articles else ["title", "link", "published", "category"]
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=keys)
        writer.writeheader()
        writer.writerows(articles)

# Run the scraper
if __name__ == "__main__":
    news_articles = fetch_rss_data()
    save_to_json(news_articles)
    save_to_csv(news_articles)
    print(f"Scraped {len(news_articles)} articles and saved to JSON & CSV.")
