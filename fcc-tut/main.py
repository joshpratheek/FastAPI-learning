from fastapi import FastAPI
from fastapi.params import Body

app= FastAPI()

@app.get("/")
def root():
    return {"msg" : "hello world"}


@app.get("/posts")
def get_posts():
    return {"data" : "These are your posts"}

@app.post("/createposts")
def create_post(payload: dict = Body(...)):
    print(payload)
    return {"msg" : "Post Created"}