from typing import Union
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def index(limit, published):
    if published:
        return {"data": f'{limit} published blogs from the db'}
    else:
        return {"data": f'{limit} blogs from the db'}

@app.get("/blog/unpublished")
def unpublish():
    return {"data": "unpublished blogs"}

@app.get("/blog/{id}")
def showBlogWithID(id: int):
    return { "data": id}

@app.get("/blog/{id}/comments")
def showComments(id):
    return {"data": {"1","2","3", "4"} }

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}