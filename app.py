from flask import Flask, render_template, request, jsonify
from rag_indexer import retrieve_relevant_articles, summarize_text, load_articles, create_embeddings

app = Flask(__name__)

# Load articles and create embeddings at startup
news_file = "news_data.json"
articles = load_articles(news_file)
embeddings, texts = create_embeddings(articles)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/process", methods=["POST"])
def process():
    try:
        user_query = request.form.get("query")
        print("Received query:", user_query)
        if not user_query:
            return jsonify({"error": "No query provided"}), 400

        # Ensure embeddings and texts exist before querying
        if not embeddings or not texts:
            return jsonify({"error": "Embedding data not available"}), 500

        relevant_articles = retrieve_relevant_articles(user_query, embeddings, texts)
        results = []
        
        if not relevant_articles:
            return jsonify({"error": "No matching articles found."})
        
        for article, score in relevant_articles:
            summary = summarize_text(article)
            results.append({
                "title": article,
                "score": round(score, 2),
                "summary": summary
            })
        
        print("Returning", len(results), "results.")
        return jsonify(results)
    except Exception as e:
        print("Error in /process:", str(e))
        return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    app.run(debug=True)