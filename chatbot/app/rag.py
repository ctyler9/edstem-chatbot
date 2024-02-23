import sys 
import os 
import dspy


ollama_model = dspy.OpenAI(api_base='http://localhost:11434/v1/', api_key='ollama', model='mistral:7b-instruct-v0.2-q6_K', stop='\n\n', model_type='chat')
colbertv2_class_data = dspy.ColBERTv2(url='http://20.102.90.50:2017/wiki17_abstracts')

dspy.settings.configure(lm=ollama_model, rm=colbertv2_class_data)


class GenerateAnswer(dspy.Signature):
    """Answer questions as a teach giving hints""" 

    context = dspy.InputField(desc="will contain either the instructions of the question or the code for the autograder to grade the question")
    question = dspy.InputField()
    answer = dspy.OutputField(desc="give a response as a hint without revealing the direct answer to students")

class RAG(dsyp.Module):
    def __init__(self, num_passages=3):
        super().__init__()

        self.retrieve = dspy.Retrieve(k=num_passages)
        self.generate_answer = dspy.ChainOfThought(GenerateAnswer)

    def forward(self, question):
        context = self.retrieve(question).passages
        prediction = self.generate_answer(context=context, question=question)
        return dspy.Prediction(context=context, answer=prediction.answer)


if __name__ == "__main__":
    query = "for HW3Q4 Hi I tried, changing the datatype to decimal for 4.4 but still getting this error and when change the output to decimaltype gradescope is crashing, can you pls check my submission and tell me what I am doing wrong:"

    rag = RAG()

    pred = rag(query)

    # Print the contexts and the answer.
    print(f"Question: {query}")
    print(f"Predicted Answer: {pred.answer}")
    print(f"Retrieved Contexts (truncated): {[c[:200] + '...' for c in pred.context]}")


