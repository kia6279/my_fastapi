from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
import time
from . import models
from .  database import engine, get_db



models.Base.metadata.create_all(bind=engine)





app = FastAPI()



class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int]= None


while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='kia6279', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful!")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error:", error)
        time.sleep(3)



my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 2}, {"title": "title of post 2", "content": "content of post 2", "id": 1}]


def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p
        
def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

@app.get('/')
async def root():
    return {"message": "Hello Welcome to my fastapi blog"}


### CRUD OPERATIONS


@app.get('/posts')
def get_post(db: Session = Depends(get_db)):

    post = db.query(models.Post).all()
    
    return {"data": post}


@app.post("/posts")
def create_posts(post: Post, db: Session = Depends(get_db)):

    new_post = models.Post(**post.dict())

    db.add(new_post)
    db.commit()
    db.refreash(new_post)
    


   
    return {"data": post}


@app.get("/post/latest")
def get_latest():
    post = my_posts[len(my_posts) -1]
    return {"latest": post}


@app.get("/posts/{id}")
def get_post(id: int, db:Session = Depends(get_db)):
    print(id)
    post = find_post(id)

    post = db.query(models.Post).filter(models.Post.id == id).first()


    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, message = f"Post with  id: {id} was not found")
        
    print(post)
    return {"post_detail": post}



@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id==id).first()

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, details = f"Post with the id: {id} does not exist")
    

    post.delete(synchronize_session=False)
    db.commit()


    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post, db: Session = Depends(get_db)):
    print(post)

    post = db.query(models.Post).filter(models.Post.id == id).first()

    
    if post == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, details = f"Post with the id: {id} does not exist")

    post.update(post.dict(), synchronize_session = False)
    return {"data": post}


    return {"message": "The post is successfully updated"}


    