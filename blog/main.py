from fastapi import FastAPI, Depends, status, Response, HTTPException
from . import schemas, models
from .database import SessionLocal, engine
from sqlalchemy.orm import Session
from typing import List

app = FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.post('/blog', status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    print(new_blog)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog



@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT)
def deleteBlog(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with {id} not found')
    blog.delete(synchronize_session=False)
    db.commit()
    return {'done'}



@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with {id} not found')
    blog.update({"title": request.title, "body": request.body}, synchronize_session=False)
    db.commit()
    return 'updated'



@app.get('/blog', response_model=List[schemas.ShowBlog])
def get_All_BLogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs



@app.get('/blog/{id}', status_code=200, response_model=schemas.ShowBlog)
def get_All_BLogs(id, db: Session = Depends(get_db), response: Response = None):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with id {id} is not available')
    return blog


# #
# # Stopped Video at 2:07:03
# #