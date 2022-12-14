from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from blog import schemas, database, models, hashing, token
router = APIRouter(
    tags=['Authentication']
)

@router.post("/login")
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.username == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sorry, username does not exist!")
    if not hashing.Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Password")
    access_token = token.create_access_token(data={"sub": user.username})
    refresh_token = token.encode_refresh_token(data={"sub": user.username})
    return {
        "access_token": access_token, 
        "refresh_token": refresh_token,
        "token_type":"bearer", 
        "username":user.username
    }


@router.post("/token/new")
def getNewToken(refresh_token: str):
    new_access_token = token.refresh_token(refresh_token=refresh_token)
    data = {
        "access_token":new_access_token,
        "refresh_token":refresh_token
    }
    return data