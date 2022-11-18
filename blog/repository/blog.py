from fastapi import HTTPException, status
from blog import models
def get_all(db):
    blogs = db.query(models.Blog).all()
    return blogs

def get_detail(id, db):
    blog = db.query(models.Blog).filter(models.Blog.id ==id).first()
    if not blog:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"detail":f"Blog with id {id} not avaliable"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    return blog

def update(id, request, db):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    blog.update(request.dict())
    db.commit()
    return "Updated"

def create(request, db, user):
    user_obj = db.query(models.User).filter(models.User.username == user.username).first()
    new_blog = models.Blog(title=request.title, body=request.body, is_published=request.is_published, author_id=user_obj.id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog
 

def delete(id, db):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"blog with id {id} does not exist")
    
    blog.delete(synchronize_session=False)
    db.commit()
    return {"detail":f"Blog with id {id} deleted successfully"}