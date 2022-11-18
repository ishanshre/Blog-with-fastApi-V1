from typing import Optional, Union
from datetime import datetime, timedelta
from jose import JWTError, jwt
from blog import schemas
SECRET_KEY = "0f6c6128728d1373bae75263f23d3e96b0c486b5d551f73d5dc8a7454aaead33"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None): 
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)# encode into jwt token
    return encoded_jwt


def verify_token(token: str, credentials_exceptions):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")# sub is the data we from access_token  to create_access_token_method
        if username is None:
            raise credentials_exceptions
        token_data = schemas.TokenData(username=username)
        return token_data
    except JWTError:
        raise credentials_exceptions
    
