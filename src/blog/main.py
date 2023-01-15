from fastapi import FastAPI
from .models import Base
from .database import engine
from .routes import blog, user, auth

app = FastAPI()


@app.get("/")
def index():
    return {"data": {"name": "Test"}}


@app.get("/about")
def about():
    return {"data": {"name": "about"}}


app.include_router(auth.router)
app.include_router(blog.router)
app.include_router(user.router)

Base.metadata.create_all(bind=engine)
