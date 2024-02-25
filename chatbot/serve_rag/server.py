from flask import Flask, request
from functools import lru_cache
import os
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)
counter = {"api" : 0}

# RAG IMPORT 
import dspy

# set up llm and retrieval model
ollama_model = dspy.OllamaLocal(model="mistral:7b", max_tokens=500)
colbertv2_class_data = dspy.ColBERTv2(url='http://localhost:8893/api/search')
dspy.settings.configure(lm=ollama_model, rm=colbertv2_class_data, compiled_lm=True)

class GenerateAnswer(dspy.Signature):
    """Answer questions as a TA giving hints""" 

    context = dspy.InputField(desc="will contain either the instructions of the question or the code for the autograder to grade the question")
    question = dspy.InputField()
    answer = dspy.OutputField(desc="give a response as a hint without revealing the direct answer to students")

class RAG(dspy.Module):
    def __init__(self, num_passages=3):
        super().__init__()

        self.retrieve = dspy.Retrieve(k=num_passages)
        self.generate_answer = dspy.ChainOfThought(GenerateAnswer)

    def forward(self, question):
        context = self.retrieve(question).passages
        prediction = self.generate_answer(context=context, question=question)
        return dspy.Prediction(context=context, answer=prediction.answer)


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
    app.run("0.0.0.0", port=int(os.getenv("PORT")))


