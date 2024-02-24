from flask import Flask, render_template, request
from functools import lru_cache
import math
import os
from dotenv import load_dotenv

from colbert.infra import Run, RunConfig, ColBERTConfig
from colbert import Searcher

load_dotenv()

INDEX_NAME = os.getenv("INDEX_NAME")
INDEX_ROOT = os.getenv("INDEX_ROOT")
app = Flask(__name__)

searcher = Searcher(index=INDEX_NAME, index_root=INDEX_ROOT)
config = ColBERTConfig(root=INDEX_ROOT)
counter = {"api" : 0}

@lru_cache(maxsize=1000000)
def api_search_query(query, k):
    print(f"Query={query}")
    if k == None: k = 10
    k = min(int(k), 100)
    pids, ranks, scores = searcher.search(query, k=k)
    pids, ranks, scores = pids[:k], ranks[:k], scores[:k]
    #passages = [searcher.collection[pid] for pid in pids]
    probs = [math.exp(score) for score in scores]
    probs = [prob / sum(probs) for prob in probs]
    topk = []
    for pid, rank, score, prob in zip(pids, ranks, scores, probs):
        # I have no idea why the index is always so much greater than searcher.collection
        # manual fix just to get it to run
        searcher_len = len(searcher.collection)
        if pid > searcher_len: 
            pid = searcher_len - 1 

        text = searcher.collection[pid]            
        d = {'text': text, 'pid': pid, 'rank': rank, 'score': score, 'prob': prob}
        topk.append(d)
    topk = list(sorted(topk, key=lambda p: (-1 * p['score'], p['pid'])))
    return {"query" : query, "topk": topk}

@app.route("/api/search", methods=["GET"])
def api_search():
    if request.method == "GET":
        counter["api"] += 1
        print("API request count:", counter["api"])
        return api_search_query(request.args.get("query"), request.args.get("k"))
    else:
        return ('', 405)

if __name__ == "__main__":
    app.run("0.0.0.0", port=int(os.getenv("PORT")), debug=True)


