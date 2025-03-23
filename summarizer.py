import json
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer  # Extractive summarization

# Load filtered news data
with open("filtered_news.json", "r", encoding="utf-8") as file:
    news_data = json.load(file)

# Summarization function
def summarize_text(text, num_sentences=2):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, num_sentences)
    return " ".join(str(sentence) for sentence in summary)

# Generate summaries for each article
summarized_articles = []
for article in news_data:
    summary = summarize_text(article.get("title", ""))
    summarized_articles.append({
        "title": article["title"],
        "summary": summary,
        "link": article["link"],
        "category": article.get("category", "unknown")
    })

# Save summarized articles
with open("summarized_news.json", "w", encoding="utf-8") as file:
    json.dump(summarized_articles, file, indent=4, ensure_ascii=False)

print(f"Summarized {len(summarized_articles)} articles and saved to 'summarized_news.json'.")
