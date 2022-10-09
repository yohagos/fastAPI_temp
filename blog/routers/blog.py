from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import schemas
from ..database import get_db
from ..repo.blog import BlogRepo

router = APIRouter(
    prefix='/blog',
    tags=["blog"]
)

@router.post('', status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = BlogRepo.create_Blog(request)
    BlogRepo.save_new_blog(new_blog, db)
    return new_blog

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def deleteBlog(id, db: Session = Depends(get_db)):
    blog = BlogRepo.get_Blogs(id, db, False)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with {id} not found')
    BlogRepo.delete_blog(blog, db)
    return 'done'

@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = BlogRepo.get_Blogs(id, db)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with {id} not found')
    BlogRepo.update_blog(blog, db, request)
    return 'updated'

@router.get('', response_model=List[schemas.ShowBlog])
def get_All_BLogs(db: Session = Depends(get_db)):
    return BlogRepo.get_all(db) 

@router.get('/{id}', status_code=200, response_model=schemas.ShowBlog)
def get_BLogs(id, db: Session = Depends(get_db)):
    blog = BlogRepo.get_Blogs(id, db)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with id {id} is not available')
    return blog