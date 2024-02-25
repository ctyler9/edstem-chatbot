import dspy

# set up llm and retrieval model
ollama_model = dspy.OllamaLocal(model="mistral:7b", max_tokens=500)
colbertv2_class_data = dspy.ColBERTv2(url='http://localhost:8893/api/search')
dspy.settings.configure(lm=ollama_model, rm=colbertv2_class_data)

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

def compile_rag():
    from dspy.datasets import HotPotQA

    # Load the dataset.
    dataset = HotPotQA(train_seed=1, train_size=20, eval_seed=2023, dev_size=50, test_size=0)

    # Tell DSPy that the 'question' field is the input. Any other fields are labels and/or metadata.
    trainset = [x.with_inputs('question') for x in dataset.train]

    from dspy.teleprompt import BootstrapFewShot

    # Validation logic: check that the predicted answer is correct.
    # Also check that the retrieved context does actually contain that answer.
    def validate_context_and_answer(example, pred, trace=None):
        answer_EM = dspy.evaluate.answer_exact_match(example, pred)
        answer_PM = dspy.evaluate.answer_passage_match(example, pred)
        return answer_EM and answer_PM

    # Set up a basic teleprompter, which will compile our RAG program.
    teleprompter = BootstrapFewShot(metric=validate_context_and_answer)

    # Compile!
    compiled_rag = teleprompter.compile(RAG(), trainset=trainset)

    return compiled_rag



if __name__ == "__main__":
    rag = RAG()
    query = "for HW3Q4 Hi I tried, changing the datatype to decimal for 4.4 but still getting this error and when change the output to decimaltype gradescope is crashing, can you pls check my submission and tell me what I am doing wrong:"

    pred = rag(query)

    # Print the contexts and the answer.
    print(f"Question: {query}")
    print(f"Predicted Answer: {pred.answer}")
    print(f"Context: {pred.context}")
    #print(f"Retrieved Contexts (truncated): {[c[:200] + '...' for c in pred.context]}")

#    c_rag = compile_rag()
#    c_rag.save(path="chatbot_module.json")



