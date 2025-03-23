import os
import json
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from sentence_transformers import SentenceTransformer, util
import torch

# Load models
tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-cnn")
summarization_model = AutoModelForSeq2SeqLM.from_pretrained("facebook/bart-large-cnn")
retrieval_model = SentenceTransformer("all-MiniLM-L6-v2")

def load_articles(news_file):
    """Load news articles from a JSON file."""
    try:
        with open(news_file, "r", encoding="utf-8") as file:
            articles = json.load(file)
        return articles
    except Exception as e:
        print("Error loading articles:", e)
        return []

def create_embeddings(articles):
    """Create embeddings for article titles and summaries."""
    if not articles:
        return None, None
    texts = [article["title"] + " " + article.get("summary", "") for article in articles]
    embeddings = retrieval_model.encode(texts, convert_to_tensor=True)
    return embeddings, texts

def retrieve_relevant_articles(query, embeddings, texts, top_k=5):
    """Retrieve the top_k articles most relevant to the query."""
    query_embedding = retrieval_model.encode(query, convert_to_tensor=True)
    similarities = util.pytorch_cos_sim(query_embedding, embeddings)[0]
    top_results = torch.topk(similarities, k=min(top_k, len(texts)))
    
    retrieved_articles = []
    for score, idx in zip(top_results[0], top_results[1]):
        retrieved_articles.append((texts[idx], score.item()))
    return retrieved_articles

def summarize_text(text):
    """Generate a summary for the given text using BART."""
    try:
        inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=1024)
        summary_ids = summarization_model.generate(
            inputs.input_ids,
            max_length=150,
            min_length=50,
            length_penalty=2.0,
            num_beams=4,
            early_stopping=True
        )
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        return summary
    except Exception as e:
        print("Error during summarization:", e)
        return "Summary unavailable."

if __name__ == "__main__":
    news_file = "news_data.json"  # Ensure this file exists with your scraped data.
    articles = load_articles(news_file)
    embeddings, texts = create_embeddings(articles)
    
    user_query = input("Enter your news topic of interest: ")
    relevant_articles = retrieve_relevant_articles(user_query, embeddings, texts)
    
    print("\nTop retrieved articles:")
    for article, score in relevant_articles:
        print(f"\nArticle: {article}\nRelevance Score: {score:.2f}")
        summary = summarize_text(article)
        print(f"Summary: {summary}\n")
