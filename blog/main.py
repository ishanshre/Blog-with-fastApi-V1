from fastapi import FastAPI  # Depends converts into pydantic
from . import models
from .database import engine
from .routers import blog, user, authentication
app = FastAPI()


# migrating the table. This is happening all the time
# automigrate database changes 
# if no database table it will create it
models.Base.metadata.create_all(engine)






app.include_router(user.router)
app.include_router(authentication.router)
app.include_router(blog.router)





