from fastapi import FastAPI  # Depends converts into pydantic
from fastapi.middleware.cors import CORSMiddleware
from blog import models
from blog.database import engine
from blog.routers import blog, user, authentication
app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# migrating the table. This is happening all the time
# automigrate database changes 
# if no database table it will create it
models.Base.metadata.create_all(engine)






app.include_router(user.router)
app.include_router(authentication.router)
app.include_router(blog.router)





