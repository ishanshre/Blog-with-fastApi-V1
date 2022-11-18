from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from blog import schemas, database
from blog.repository import user
from blog import oauth2

router = APIRouter(
    tags=['Users'],
    prefix="/user"
)

@router.post("/", response_model=schemas.ShowUser)
def create_user(request: schemas.User, db: Session = Depends(database.get_db)):
    return user.create(request, db)


@router.get("/{username}", response_model=schemas.ShowUser, status_code=status.HTTP_200_OK)
def user_get(username: str,db: Session = Depends(database.get_db), get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    return user.get_user(username, db)