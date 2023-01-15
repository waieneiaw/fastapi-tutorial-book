from fastapi import FastAPI
from .models import Base
from .database import engine
from .routes import blog, user

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/")
def index():
    return {"data": {"name": "Test"}}


@app.get("/about")
def about():
    return {"data": {"name": "about"}}


app.include_router(blog.router)
app.include_router(user.router)
