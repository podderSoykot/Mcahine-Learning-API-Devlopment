from fastapi import FastAPI, HTTPException, status,Depends
from pydantic import BaseModel
from typing import List, Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
from typing import Optional
import datetime
from fastapi import Depends
from . import models
from app.database import engine ,get_db
from sqlalchemy.orm import Session


# Database model
models.Base.metadata.create_all(bind=engine)




app = FastAPI()

from typing import Optional
from datetime import datetime

class Post(BaseModel):
    id: Optional[int]=None
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None
    created_at: Optional[datetime]=None



def close_connection(conn):
    if conn is not None:
        conn.close()
        print("Connection closed.")

while True:
    try:
        # Replace with your actual database credentials
        conn = psycopg2.connect(
            host="localhost",
            database="products",  # Replace with your actual database name
            user="postgres",
            password="admin",
            cursor_factory=RealDictCursor
        )
        print("Connected to the database successfully!")
        break
    except Exception as e:
        print(f"Connecting to the database failed.")
        print("Error:", e)
        # Exiting the application if connection to the database fails
        exit()
        time.sleep(3)  # Add a delay before retrying connection

def get_cursor():
    return conn.cursor()




@app.get("/")
async def root():
    return {"message": "Root endpoint working"}



#testing purpose

@app.get("/sqlalchemy")
def test_post(db: Session=Depends(get_db)):
    posts=db.query(models.Post).all()
    return {"data": posts}





@app.get("/show_all_posts/", response_model=None)
async def show_all_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}
    # try:
    #     cursor = get_cursor()
    #     cursor.execute("SELECT * FROM post")  # Corrected table name
    #     posts = cursor.fetchall()
    #     return posts
    # except Exception as e:
    #     # Handle exceptions, e.g., connection errors, query errors
    #     raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    # finally:
    #     # Ensure to close the cursor
    #     cursor.close()

#ok
# @app.post("/posts/create", status_code=status.HTTP_201_CREATED)
# def create_post(post: Post):
#     cursor = get_cursor()  # Get the cursor
#     try:
#         cursor.execute("INSERT INTO post(title, content, published) VALUES (%s, %s, %s) RETURNING *",
#                        (post.title, post.content, post.published))
#         new_post = cursor.fetchone()  
#         conn.commit()
#         return {"data": new_post}
#     except Exception as e:
#         conn.rollback()
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
#     finally:
#         cursor.close()

@app.post("/posts/create", status_code=status.HTTP_201_CREATED)
async def create_post(post: Post,db: Session=Depends(get_db)):
    try:
        db_post = models.Post(**post.dict())
        db.add(db_post)
        db.commit()
        db.refresh(db_post)  # This ensures the newly created post is fully populated including auto-generated fields
        return {"data": db_post}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


#ok
@app.get("/posts/{post_id}", response_model=Post)
async def get_post(post_id: int):
    cursor = get_cursor()
    try:
        cursor.execute("SELECT * FROM post WHERE id = %s", (post_id,))
        post = cursor.fetchone()
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        return post
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    finally:
        cursor.close()


#ok
@app.delete("/posts/delete/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int):
    cursor = get_cursor()
    try:
        cursor.execute("DELETE FROM post WHERE id = %s", (str(post_id),))  
        if cursor.rowcount == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {post_id} not found")
        else:
            conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    finally:
        cursor.close()


@app.put("/posts/update/{id}", response_model=Post)
async def update_post(id: int, post: Post):
    cursor = get_cursor()
    try:
        cursor.execute(
            "UPDATE post SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *",
            (post.title, post.content, post.published, id)
        )
        updated_post = cursor.fetchone()
        if not updated_post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} not found")
        conn.commit()
        return updated_post
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    finally:
        cursor.close()

