from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from random import randint

app= FastAPI()

class Post(BaseModel):
    title : str
    content : str
    published : bool = True
    rating : Optional[int] = None

my_posts = [{"id": 1, "title": "title of post 1", "content": "content of post 1"},
            {"id": 2, "title": "favorite foods", "content": "I like pizza"}
        ]

def find_post(id: int):
    for post in my_posts:
        if post["id"] == id:
            return post


def find_index_post(id: int):
    for index, post in enumerate(my_posts):
        if post["id"] == id:
            return index 

@app.get("/")
def root():
    return {"msg" : "hello world"}


@app.get("/posts")
def get_posts():
    return {"data" : my_posts}


@app.post("/posts", status_code = 201)
def create_post(post: Post):
    post_dict = post.model_dump()
    post_dict["id"] = randint(1,100000)
    my_posts.append(post_dict)
    return {"new_post": post_dict}


@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)

    if post is None:
        raise HTTPException(
            status_code = 404, 
            detail = f"Post with id {id} not found"
        )

    return {"post_details" : post}


@app.delete("/posts/{id}", status_code = 204)  #204 - No content
def delete_post(id: int):
    post_index = find_index_post(id)

    if post_index is None:
            raise HTTPException(
                status_code = 404,
                detail = f"Post with id {id} not found"
            )

    my_posts.pop(post_index)

    
@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    post_index = find_index_post(id)

    if post_index is None:
                raise HTTPException(
                    status_code = 404,
                    detail = f"Post with id {id} not found"
                )

    post_dict = post.model_dump()
    post_dict["id"] = id
    my_posts[post_index] = post_dict
    
    return {"updated_post" : my_posts[post_index]} 
