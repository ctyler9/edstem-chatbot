from colbert.data import Queries
from colbert.infra import Run, RunConfig, ColBERTConfig
from colbert import Searcher
from dotenv import load_dotenv
import os 

load_dotenv()

INDEX_NAME = os.getenv("INDEX_NAME")
INDEX_ROOT = os.getenv("INDEX_ROOT")
CLASS_FILES = os.getenv("class_files")

if __name__=='__main__':
    with Run().context(RunConfig(nranks=1, experiment="class_data")):

        config = ColBERTConfig(
            root=INDEX_ROOT,
        )
        searcher = Searcher(index="class_data", config=config)
        queries = Queries(CLASS_FILES)
        ranking = searcher.search_all(queries, k=100)
        #ranking.save("msmarco.nbits=2.ranking.tsv")
        print(ranking)
