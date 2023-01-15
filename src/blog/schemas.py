from pydantic import BaseModel


class Blog(BaseModel):
    title: str
    body: str

    class Config:
        orm_mode = True


class ShowBlog(BaseModel):
    id: int
    title: str
    body: str

    class Config:
        orm_mode = True
