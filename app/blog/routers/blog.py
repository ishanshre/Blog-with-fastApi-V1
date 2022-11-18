from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from blog import schemas, oauth2
from blog.repository import blog
from blog.database import get_db

router = APIRouter(
    tags=['Blogs'], # defning tags here instead of router.get()
    prefix="/blog" # url prefix
)

@router.get("/", response_model=List[schemas.ListBlog])
def post_list(db: Session = Depends(get_db)):
    return blog.get_all(db)
    

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.ListBlog)
def post_detail(id, db: Session = Depends(get_db)):
    return blog.get_detail(id, db)


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def post_update(id, request: schemas.Blog, db: Session = Depends(get_db), get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog.update(id, request, db)


@router.post("/post-create", status_code=status.HTTP_201_CREATED)
def post_create(request: schemas.Blog, db: Session = Depends(get_db), get_current_user: schemas.User = Depends(oauth2.get_current_user)): # convert session of database into type recognized by pydantic
    return blog.create(request, db, get_current_user)


@router.delete("/{id}/post-delete", status_code=status.HTTP_204_NO_CONTENT)
def post_delete(id, db: Session = Depends(get_db), get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog.delete(id, db)