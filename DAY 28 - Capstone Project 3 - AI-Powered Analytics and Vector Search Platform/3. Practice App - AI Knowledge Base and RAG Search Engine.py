"""
Day 28 Practice Application: AI Knowledge Base & RAG Vector Engine
===================================================================
This application demonstrates:
1. Converting text documents into vector embeddings and storing in vector index.
2. Calculating Cosine Similarity metrics to find top-K relevant context chunks.
3. Building a Retrieval-Augmented Generation (RAG) prompt pipeline.
4. Real-Time streaming responses using Server-Sent Events (Response(mimetype='text/event-stream')).
5. Interactive Web Dashboard for document ingestion, semantic vector search, and AI chat.
"""

import time
import math
from flask import Flask, jsonify, request, Response, stream_with_context, render_template_string

app = Flask(__name__)
app.config['SECRET_KEY'] = 'day28-rag-vector-masterclass-secret'

# In-Memory Vector Store Simulator
VECTOR_STORE = []


# ------------------------------------------------------------------------------
# 1. Vector Math & Embedding Engine (Simulated Embedding Model)
# ------------------------------------------------------------------------------
def generate_simple_vector_embedding(text):
    """Generates a normalized 8-dimensional semantic vector embedding."""
    words = text.lower().split()
    vocab = ["flask", "python", "database", "security", "docker", "gunicorn", "api", "auth"]
    vec = [words.count(word) for word in vocab]
    
    # Calculate vector magnitude (L2 Norm)
    magnitude = math.sqrt(sum(val ** 2 for val in vec))
    if magnitude == 0:
        return [0.1] * len(vocab)
    return [round(val / magnitude, 4) for val in vec]

def cosine_similarity(vec1, vec2):
    """Calculates Cosine Similarity between two vector embeddings."""
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    mag1 = math.sqrt(sum(a ** 2 for a in vec1))
    mag2 = math.sqrt(sum(b ** 2 for b in vec2))
    if mag1 == 0 or mag2 == 0:
        return 0.0
    return round(dot_product / (mag1 * mag2), 4)


# Seed Knowledge Base
with app.app_context():
    sample_docs = [
        "Flask is a lightweight WSGI web application framework in Python.",
        "Gunicorn pre-fork worker model handles production Flask HTTP requests.",
        "Docker containerizes Flask applications with multi-stage builds.",
        "Flask-Security and Flask-WTF prevent CSRF and XSS security vulnerabilities.",
        "PostgreSQL and SQLAlchemy ORM manage relational database persistence."
    ]
    for doc in sample_docs:
        emb = generate_simple_vector_embedding(doc)
        VECTOR_STORE.append({"text": doc, "embedding": emb})


# ------------------------------------------------------------------------------
# 2. Interactive AI Dashboard UI
# ------------------------------------------------------------------------------
AI_DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Day 28 RAG & Vector Search Masterclass</title>
    <style>
        body { font-family: Arial, sans-serif; background: #0f172a; color: #f8fafc; margin: 30px; }
        .card { max-width: 900px; margin: auto; background: #1e293b; padding: 25px; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }
        .input-group { margin-bottom: 15px; }
        input[type="text"] { width: 70%; padding: 10px; border-radius: 4px; border: 1px solid #475569; background: #0f172a; color: white; }
        .btn { background: #3b82f6; color: white; border: none; padding: 10px 18px; border-radius: 4px; cursor: pointer; }
        .btn-success { background: #10b981; }
        .box { background: #020617; color: #38bdf8; padding: 15px; border-radius: 6px; font-family: monospace; font-size: 0.9em; margin-top: 15px; height: 180px; overflow-y: scroll; white-space: pre-wrap; }
    </style>
</head>
<body>
    <div class="card">
        <h2>🤖 AI-Powered RAG & Vector Search Engine (Day 28)</h2>
        <p>Demonstrating Vector Embeddings, Cosine Similarity, RAG Prompt Grounding, and Token Streaming (SSE).</p>

        <div class="input-group">
            <input type="text" id="query_input" value="How does Gunicorn run Flask in production?" placeholder="Ask a question...">
            <button class="btn" onclick="performVectorSearch()">Vector Semantic Search</button>
            <button class="btn btn-success" onclick="streamRAGChat()">Stream RAG AI Response (SSE)</button>
        </div>

        <h3>Output Console:</h3>
        <div id="output" class="box">Console ready...</div>
    </div>

    <script>
        async function performVectorSearch() {
            const q = document.getElementById('query_input').value;
            const res = await fetch('/api/search', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({query: q, top_k: 2})
            });
            const data = await res.json();
            document.getElementById('output').innerText = JSON.stringify(data, null, 2);
        }

        async function streamRAGChat() {
            const q = document.getElementById('query_input').value;
            const out = document.getElementById('output');
            out.innerText = "[STREAMING LLM RESPONSE]\n";

            const response = await fetch('/api/chat/stream', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({prompt: q})
            });

            const reader = response.body.getReader();
            const decoder = new TextDecoder("utf-8");

            while (true) {
                const { value, done } = await reader.read();
                if (done) break;
                const chunk = decoder.decode(value);
                const lines = chunk.split("\n");
                for (let line of lines) {
                    if (line.startsWith("data: ")) {
                        out.innerText += line.replace("data: ", "");
                    }
                }
            }
        }
    </script>
</body>
</html>
"""


# ------------------------------------------------------------------------------
# 3. Route Handlers
# ------------------------------------------------------------------------------
@app.route('/')
def index():
    return render_template_string(AI_DASHBOARD_HTML)

@app.route('/api/search', methods=['POST'])
def vector_search_api():
    payload = request.get_json(silent=True) or {}
    query_text = payload.get('query', '')
    top_k = int(payload.get('top_k', 2))

    query_emb = generate_simple_vector_embedding(query_text)

    # Rank documents by Cosine Similarity
    results = []
    for item in VECTOR_STORE:
        score = cosine_similarity(query_emb, item['embedding'])
        results.append({"text": item['text'], "similarity_score": score})

    results.sort(key=lambda x: x['similarity_score'], reverse=True)
    top_matches = results[:top_k]

    return jsonify({
        "query": query_text,
        "query_embedding": query_emb,
        "top_matches": top_matches
    }), 200

@app.route('/api/chat/stream', methods=['POST'])
def rag_chat_stream():
    payload = request.get_json(silent=True) or {}
    user_query = payload.get('prompt', '')

    # 1. RAG Retrieval Step
    query_emb = generate_simple_vector_embedding(user_query)
    results = []
    for item in VECTOR_STORE:
        score = cosine_similarity(query_emb, item['embedding'])
        results.append((score, item['text']))
    results.sort(reverse=True)
    best_context = results[0][1] if results else "No context found."

    # 2. Generator Function for SSE Streaming
    def generate_tokens():
        response_tokens = [
            f"Based on retrieved context ('{best_context}'): ",
            "Flask ", "applications ", "achieve ", "enterprise ", "scale ",
            "by ", "decoupling ", "components ", "and ", "leveraging ",
            "asynchronous ", "RAG ", "search ", "pipelines."
        ]
        for token in response_tokens:
            time.sleep(0.12) # Simulate LLM generation latency
            yield f"data: {token}\n\n"

    return Response(
        stream_with_context(generate_tokens()),
        mimetype='text/event-stream',
        headers={'Cache-Control': 'no-cache', 'X-Accel-Buffering': 'no'}
    )


if __name__ == '__main__':
    print("=" * 70)
    print("Starting Day 28 AI Knowledge Base Application...")
    print("AI Dashboard UI at http://127.0.0.1:5000/")
    print("=" * 70)
    app.run(host='127.0.0.1', port=5000, debug=True)
