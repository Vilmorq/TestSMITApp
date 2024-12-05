from http import HTTPStatus

from fastapi import HTTPException, Request


class BaseError(Exception):
    status_code: HTTPStatus = HTTPStatus.INTERNAL_SERVER_ERROR
    detail: str = ""

    def __init__(
        self, detail: str | None = None, status_code: HTTPStatus | None = None
    ):
        if status_code:
            self.status_code = status_code
        if detail or not self.detail:
            self.detail = detail or self.status_code.phrase


class NotFoundError(BaseError):
    status_code = HTTPStatus.NOT_FOUND


class BadRequestError(BaseError):
    status_code = HTTPStatus.BAD_REQUEST


def source_exception_handlers(request: Request, exc: BaseError):
    raise HTTPException(status_code=exc.status_code.value, detail=exc.detail)


exception_handlers = {
    BaseError: source_exception_handlers,
}
