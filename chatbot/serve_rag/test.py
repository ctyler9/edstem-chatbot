from rag import RAG 


if __name__ == "__main__":
    rag = RAG()
    query = "for HW3Q4 Hi I tried, changing the datatype to decimal for 4.4 but still getting this error and when change the output to decimaltype gradescope is crashing, can you pls check my submission and tell me what I am doing wrong:"

    pred = rag(query)

    # Print the contexts and the answer.
    print(f"Question: {query}")
    print(f"Predicted Answer: {pred.answer}")
    print(f"Context: {pred.context}")

