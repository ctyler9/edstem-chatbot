from fastapi import FastAPI, Query
from query import similarity_search 

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/similarity_search")
def process_query(query: str = Query(..., title="Query", description="Your query string")):

    return similarity_search(query)

if __name__ == "__main__":
    import uvicorn

    # Run the server using Uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

