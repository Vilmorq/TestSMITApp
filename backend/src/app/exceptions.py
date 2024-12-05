from http import HTTPStatus

from app.core.exceptions import BaseError


class FileTypeError(BaseError):
    status_code = HTTPStatus.UNSUPPORTED_MEDIA_TYPE


class DateError(BaseError):
    status_code = HTTPStatus.UNPROCESSABLE_ENTITY
    detail = "Wrong date format"
