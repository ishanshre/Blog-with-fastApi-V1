from typing import Optional, Union
from datetime import datetime, timedelta
from jose import JWTError, jwt, ExpiredSignatureError
from blog import schemas
from fastapi import HTTPException, status
SECRET_KEY = "0f6c6128728d1373bae75263f23d3e96b0c486b5d551f73d5dc8a7454aaead33"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None): 
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire, "scope":"access_token"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)# encode into jwt token
    return encoded_jwt


def decode_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        if (payload["scope"] == 'access_token'):
            return payload['sub']
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Scope for Token is Invalid")
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")


def encode_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=1)
    to_encode.update({
        "exp":expire,
        "scope":"refresh_token",
    })
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def refresh_token(refresh_token):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=ALGORITHM)
        if (payload["scope"] == "refresh_token"):
            new_token = create_access_token(payload)
            return new_token
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh Token Expired")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")



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
    
