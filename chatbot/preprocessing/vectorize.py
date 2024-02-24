import os

from ragatouille import RAGPretrainedModel

from dotenv import dotenv_values
env_vars = dotenv_values(".env")

RAG = RAGPretrainedModel.from_pretrained("colbert-ir/colbertv2.0")

def get_files():
    header = []
    out = []
    anon_data_root = env_vars["class_files"]
    for file in os.listdir(anon_data_root):
        with open(os.path.join(anon_data_root, file)) as fp:
            file_contents = fp.read()
            
            header.append(file)
            out.append(file_contents)
    
    return out

def get_file():
    syllabus_path = env_vars.get("class_files")
    if not syllabus_path:
        return

    with open(syllabus_path, 'r') as file:
        file_contents = file.read()
         
    return [file_contents]



if __name__ == "__main__":
    print(len(get_files()))
    #index_path = RAG.index(index_name="class_files", collection=get_files())

