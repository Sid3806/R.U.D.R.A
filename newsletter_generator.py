import json

# Load summarized news data
with open("summarized_news.json", "r", encoding="utf-8") as file:
    news_data = json.load(file)

# Start Markdown content
newsletter_content = """# 📢 AI-Powered Personalized Newsletter 📰  
Stay updated with the latest news based on your preferences!  

"""

# Organize articles by category
categories = {}
for article in news_data:
    category = article.get("category", "General").title()
    if category not in categories:
        categories[category] = []
    categories[category].append(article)

# Format articles in Markdown
for category, articles in categories.items():
    newsletter_content += f"\n## 🔹 {category} News\n"
    for article in articles:
        newsletter_content += f"- **[{article['title']}]({article['link']})**\n"
        newsletter_content += f"  - *{article['summary']}*\n\n"

# Save newsletter to file
with open("newsletter.md", "w", encoding="utf-8") as file:
    file.write(newsletter_content)

print("✅ Newsletter generated and saved as 'newsletter.md'.")
