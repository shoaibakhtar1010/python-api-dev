from fastapi import FastAPI,Response,status,HTTPException
from fastapi.param_functions import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
app = FastAPI()
import time

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    
# connect to postgres database
while True:
    try:
        conn = psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='Poijkl#123',cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection successful")
        break
    except Exception as e:
        print("Could not connect to database")
        print("Error: ",e)
        time.sleep(2)

@app.get("/")
async def root():
    """
    The root of the API, this will return a simple message saying Hello World.

    :return: A dict with a key of "message" and a value of "Hello World"
    """
    return {"message": "Hello shoaibakhtar shaikh"}


my_posts = [{
    "title": "title of post 1","content": "content of post 1","id": 1},
    {"title": "title of post 2","content": "content of post 2","id": 2}]

@app.get("/posts")
def get_posts():
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    
    return {"data": posts}

@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0,100000)
    my_posts.append(post_dict)
    return {"data": post_dict} #{payload}
      

@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    post = [post for post in my_posts if post["id"] == id]
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id {id} not found"}
    return {"post": post}

@app.delete("/posts/{id}")
def delete_post(id: int):
    #implementing logic to delete post with id = id
    # find the index in array that has required id
    index = None
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            index = i
            break
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} not found")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = None
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            index = i
            break
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} not found")
    post_dict = post.dict()
    post_dict['id']=id
    my_posts[index] = post_dict
    return {"data": post_dict}