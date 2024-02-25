from flask import Flask, request
from functools import lru_cache
import os
from dotenv import load_dotenv

from rag import RAG

load_dotenv()

app = Flask(__name__)
counter = {"api" : 0}

rag = RAG()

@lru_cache(maxsize=1000000)
def api_search_query(query):
    pred = rag(query)

    return {"query": query, "answer": pred.answer, "context": pred.context}


@app.route("/api/search", methods=["GET"])
def api_search():
    if request.method == "GET":
        counter["api"] += 1
        print("API request count:", counter["api"])
        return api_search_query(request.args.get("query"))
    else:
        return ('', 405)

if __name__ == "__main__":
    app.run("0.0.0.0", port=int(os.getenv("PORT")), debug=True)


