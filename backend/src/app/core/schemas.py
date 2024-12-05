from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


def name_for_generic(params, postfix="") -> str:
    try:
        if repr(params[0]).startswith("<"):
            new_name = params[0].__name__
        else:
            arr_name = repr(params[0]).split("[")
            class_name = arr_name[1].split(".").pop().strip("]")
            new_name = f"{class_name}{arr_name[0].title()}"
    except Exception:
        new_name = repr(params[0])

    return f"{new_name}{postfix}Response"


class ResponseCommon(BaseModel):
    error_code: int | None = None
    detail: str = "ok"


class ResponseGeneric(ResponseCommon, Generic[T]):
    data: T | None

    @classmethod
    def __concrete_name__(cls, params) -> str:
        return name_for_generic(params)


class ResponseListGeneric(ResponseCommon, Generic[T]):
    data: list[T]
    total_count: int = 0

    @classmethod
    def __concrete_name__(cls, params) -> str:
        return name_for_generic(params, "List")
