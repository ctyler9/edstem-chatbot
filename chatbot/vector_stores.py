from langchain.document_loaders import JSONLoader 
from langchain.document_loaders.merge import MergedDataLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma

from typing import Union
import os 

from vars import ANONDATA_ROOT, CHROMA_PATH

## References 
#https://python.langchain.com/docs/modules/data_connection/retrievers/multi_vector
#https://python.langchain.com/docs/modules/data_connection/document_loaders/json
#https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF#provided-files
#https://huggingface.co/TheBloke/LLaMa-7B-GGML/blob/main/llama-7b.ggmlv3.q2_K.bin
#https://stackoverflow.com/questions/76232375/langchain-chroma-load-data-from-vector-database
#https://python.langchain.com/docs/integrations/text_embedding/huggingfacehub

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

    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    documents = text_splitter.split_documents(raw_documents)
    embeddings = HuggingFaceEmbeddings()     
    Chroma.from_documents(documents, embeddings, persist_directory=outpath)

    return "success", None

if __name__ == "__main__":

    inpath_list = [os.path.join(ANONDATA_ROOT, x) for x in os.listdir(ANONDATA_ROOT)]

    create_embeddings(inpath_list, CHROMA_PATH)



