from functools import wraps
from typing import Any, Callable

from pydantic import BaseModel

from app.core.schemas import ResponseGeneric
from app.core.utils import convert_orm_to_schema


def prepare_response_generic(
    schema: Any,
    exceptions_if_none: type[BaseException] | None = None,
) -> Callable[[...], Any]:
    """
    A decorator for a function in the router to reduce the copy-paste effect

    Example of usage:

    ------ BEFORE -----

    @router.get(
        "/{cargo_rate_id}",
        response_model=ResponseGeneric[CargoRateBase],
        status_code=HTTPStatus.OK,
        summary="Get cargo rate",
    )
    async def get_cargo_rate(
        request: Request,
        cargo_rate_id: int = Path_id(),
    ):
        cargo_rate = await CargoRateService.get_by_id(request.state.session, cargo_rate_id)
        if cargo_rate is None:
            raise NotFoundError()
        return ResponseGeneric[CargoRateBase](data=cargo_rate)

    ------ AFTER -------

    @router.get(
        "/{cargo_rate_id}",
        response_model=ResponseGeneric[CargoRateBase],
        status_code=HTTPStatus.OK,
        summary="Get cargo rate",
    )
    @prepare_response_generic(schema=CargoRateBase, exceptions_if_none=NotFoundError)
    async def get_cargo_rate(
        request: Request,
        cargo_rate_id: int = Path_id(),
    ):
        return await CargoRateService.get_by_id(request.state.session, cargo_rate_id)

    :param schema: schema for generic response
    :param exceptions_if_none: raise this then response is None
    :return: func
    """

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            response = await func(*args, **kwargs)
            if exceptions_if_none and response is None:
                raise exceptions_if_none()
            if isinstance(response, BaseModel):
                response = convert_orm_to_schema(response, schema)
            return ResponseGeneric[schema](data=response)

        return wrapper

    return decorator
