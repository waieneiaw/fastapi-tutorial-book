from typing import TypedDict, Dict, Union, List
from pydantic import BaseModel


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
