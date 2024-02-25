from flask import Flask, request
from functools import lru_cache
import math
import os
from dotenv import load_dotenv

from ragatouille import RAGPretrainedModel

load_dotenv()

INDEX_NAME = os.getenv("INDEX_NAME")
INDEX_ROOT = os.getenv("INDEX_ROOT")
app = Flask(__name__)

counter = {"api" : 0}
RAG = RAGPretrainedModel.from_index(os.path.join(INDEX_ROOT, INDEX_NAME))

@lru_cache(maxsize=1000000)
def api_search_query(query, k):
    print(f"Query={query}")
    if k == None: 
        k = 10
    k = min(int(k), 100)
    results = RAG.search(query=query, k=k)
    
    updated_keys = []
    for adict in results:
        new_dict = {}
        # new_dict = {'text': text, 'pid': pid, 'rank': rank, 'score': score, 'prob': prob}
        # old_dict = {"content": "text of the relevant passage", "score": 0.123456, "rank": 1, "document_id": "x"}

        new_dict["text"] = adict["content"]
        new_dict["score"] = adict["score"]
        new_dict["pid"] = adict["document_id"]
        new_dict["rank"] = adict["rank"]
        updated_keys.append(new_dict) 

    # Transform scores into probabilities
    scores = [result["score"] for result in updated_keys]
    probs = [math.exp(score) for score in scores]
    total_prob = sum(probs)
    probs = [prob / total_prob for prob in probs]

    # Assign probabilities to each result
    for i in range(len(updated_keys)):
        updated_keys[i]["prob"] = probs[i]

    sorted_results = sorted(updated_keys, key=lambda x: (-x["score"], x["pid"]))

    return {"query" : query, "topk": sorted_results}

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


