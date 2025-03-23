import json

# Load scraped news data
with open("news_data.json", "r", encoding="utf-8") as file:
    news_data = json.load(file)

# Define user preferences
user_preferences = {
    "categories": ["technology", "finance"],  # Example categories (case-sensitive)
}

# Filter articles based on user preferences
filtered_articles = [
    article for article in news_data
    if "category" in article and article["category"].lower() in user_preferences["categories"]
]

# Save filtered results
with open("filtered_news.json", "w", encoding="utf-8") as file:
    json.dump(filtered_articles, file, indent=4, ensure_ascii=False)

print(f"Filtered {len(filtered_articles)} articles based on user preferences and saved to 'filtered_news.json'.")
