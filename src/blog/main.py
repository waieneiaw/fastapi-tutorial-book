from fastapi import FastAPI
from typing import TypedDict, Dict, Union, List, Optional
from pydantic import BaseModel


class Blog(BaseModel):
    title: str
    description: str
    published_at: Optional[bool]


_JsonPremitiveValueType = Union[str, int, bool, None]
JsonKeyType = Union[str, int]
_JsonWithoutChildJsonType = Dict[
    JsonKeyType, Union[_JsonPremitiveValueType, List[_JsonPremitiveValueType]]
]

# JSON
JsonType = Dict[
    JsonKeyType,
    Union[
        _JsonPremitiveValueType,
        List[_JsonPremitiveValueType],
        _JsonWithoutChildJsonType,
        List[_JsonWithoutChildJsonType],
    ],
]

# JSONの値
JsonValueType = Union[
    _JsonPremitiveValueType,
    List[_JsonPremitiveValueType],
    JsonType,
]


# レスポンス型
OkResponseType = TypedDict(
    "ResponseType",
    # `BaseModel`を受け付けられるようにする
    {"data": Union[JsonValueType, BaseModel]},
)

app = FastAPI()


@app.get("/")
def index():
    return {"data": {"name": "Test"}}


@app.get("/about")
def about():
    return {"data": {"name": "about"}}


@app.get("/blog/category")
def category() -> JsonType:
    return {"data": ["all category"]}


@app.get("/blog")
def item(limit: int = 10, published: bool = True) -> OkResponseType:
    if published:
        return {"data": f"{limit}件"}
    else:
        return {"data": "非公開"}


@app.get("/blog/{id}")
def show(id: int) -> OkResponseType:
    return {"data": id}


@app.get("/blog/{id}/comments")
def comments(id: int, limit: Optional[str] = None) -> OkResponseType:
    return {"data": [id, limit, "comments"]}


@app.post("/blog")
def create_blog(blog: Blog) -> OkResponseType:
    return {"data": blog}
