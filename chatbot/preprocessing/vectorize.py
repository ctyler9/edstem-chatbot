from langchain_community.document_loaders import JSONLoader 
from langchain_community.document_loaders.merge import MergedDataLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS 
from langchain_community.embeddings import HuggingFaceInstructEmbeddings

import os 
from typing import Union
from dotenv import dotenv_values

env_vars = dotenv_values(".env")

ANONDATA_ROOT, EMBEDDINGS_PATH  = env_vars["anondata_root"], env_vars["embedding_path_out"]

def create_json_loader(file_path: str):
    loader = JSONLoader(
        file_path=file_path,
        jq_schema=".[] | {threadPost, comments}",
        text_content=False)

    return loader

def create_embeddings(inpath: Union[str, list], outpath: str):
    # Load the document, split it into chunks, embed each chunk and load it into the vector store.
    if type(inpath) == str:
        raw_documents = create_json_loader(inpath)
    elif type(inpath) == list:
        raw_documents = MergedDataLoader(loaders=[create_json_loader(x) for x in inpath])
    else:
        return "error", None

    raw_documents = raw_documents.load()

    text_splitter = RecursiveCharacterTextSplitter()
    documents = text_splitter.split_documents(raw_documents)
    embeddings = HuggingFaceInstructEmbeddings(
        query_instruction="You are a bot programmed to help students for a class. You are referring to prior threads asked by students and answered by TA. You are tasked to represent the most relevant query for retrieval given the students question: ",
        model_name= "intfloat/e5-mistral-7b-instruct",
        model_kwargs = {"device": "gpu"},
        encode_kwargs = {"normalize_embeddings": True, "low_cpu_mem_usage": True},
    )

    FAISS.from_documents(documents, embeddings, persist_directory=outpath)

    return "success", None

if __name__ == "__main__":
    inpath_list = [os.path.join(ANONDATA_ROOT, x) for x in os.listdir(ANONDATA_ROOT)]
    create_embeddings(inpath_list, EMBEDDINGS_PATH)



