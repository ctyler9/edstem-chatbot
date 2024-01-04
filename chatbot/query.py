from langchain import embeddings
from langchain.vectorstores import Chroma 
from langchain.embeddings import HuggingFaceEmbeddings

from vars import CHROMA_PATH    

embeddings = HuggingFaceEmbeddings()
g_db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)
g_db.get() 

def similarity_search(query):
    docs = g_db.similarity_search(query)
    return docs


if __name__ == "__main__":
    query = "I am having issues with Question1 on HW3.. how do I proceed?"

    print(similarity_search(query))
