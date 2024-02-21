from ragatouille import RAGPretrainedModel

query = "for HW3Q4 Hi I tried, changing the datatype to decimal for 4.4 but still getting this error and when change the output to decimaltype gradescope is crashing, can you pls check my submission and tell me what I am doing wrong:"
RAG = RAGPretrainedModel.from_index(".ragatouille/colbert/indexes/syllabus")
results = RAG.search(query)

print(results)
