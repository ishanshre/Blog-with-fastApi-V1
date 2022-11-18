from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    username: str
    email: str
    password: str


class ShowUser(BaseModel):
    username: str
    email: str
    class Config():
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class Login(BaseModel):
    username: str
    password: str

class Blog(BaseModel):
    title: str
    body: str
    is_published: Optional[bool]  


class ListBlog(BaseModel):
    title: str
    body: str
    author: ShowUser
    class Config():
        orm_mode = True