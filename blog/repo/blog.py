from sqlalchemy.orm import Session
from .. import models


class BlogRepo():

    def create_Blog(request):
        return models.Blog(title=request.title, body=request.body, user_id=1)
    
    def save_new_blog(newBlog, db):
        db.add(newBlog)
        db.commit()
        db.refresh(newBlog)

    def get_all(db):
        blogs = db.query(models.Blog).all()
        return blogs

    def get_Blogs(id:int, db, first: bool = None):
        if not first:
            return db.query(models.Blog).filter(models.Blog.id == id)
        return db.query(models.Blog).filter(models.Blog.id == id).first()

    def delete_blog(blog, db: Session):
        blog.delete(synchronize_session=False)
        db.commit()

    def update_blog(blog, db, request):
       blog.update({"title": request.title, "body": request.body}, synchronize_session=False)
       db.commit()
    
    #:int