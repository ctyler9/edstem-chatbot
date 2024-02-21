import json
import os

from ragatouille import RAGPretrainedModel

from dotenv import dotenv_values
env_vars = dotenv_values(".env")

RAG = RAGPretrainedModel.from_pretrained("colbert-ir/colbertv2.0")

def get_forum_post():
    headers = []
    out = []
    anon_data_root = env_vars["anondata_root"]
    for file in os.listdir(anon_data_root):
        if file.endswith(".json"):
            data = json.load(os.path.join(anon_data_root, file))

def get_syllabus():
    syllabus_path = env_vars.get("syllabus_path")
    if not syllabus_path:
        return

    with open(syllabus_path, 'r') as file:
        file_contents = file.read()
         
    return [file_contents]

    
index_path = RAG.index(index_name="syllabus", collection=get_syllabus())

