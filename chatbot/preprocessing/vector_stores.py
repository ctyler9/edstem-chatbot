from langchain.document_loaders import JSONLoader 
from langchain.document_loaders.merge import MergedDataLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS 

from typing import Union
import os 

from vars import ANONDATA_ROOT, EMBEDDINGS_PATH

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

    text_splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=0)
    documents = text_splitter.split_documents(raw_documents)
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")     
    FAISS.from_documents(documents, embeddings, persist_directory=outpath)

    return "success", None

if __name__ == "__main__":

    inpath_list = [os.path.join(ANONDATA_ROOT, x) for x in os.listdir(ANONDATA_ROOT)]

    create_embeddings(inpath_list, EMBEDDINGS_PATH)



