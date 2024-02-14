from langchain.llms import HuggingFacePipeline 
from langchain.prompts import PromptTemplate
from langchain.embeddings import HuggingFaceEmbeddings
from presidio_analyzer.nlp_engine.transformers_nlp_engine import transformers

from vars import EMBEDDINGS_PATH 

text_generation_pipeline = transformers.pipeline(
    model=model
