import io
import json
from http import HTTPStatus

from fastapi import APIRouter, Depends, File, Request, UploadFile
from fastapi.params import Body

from app.core.decorators import prepare_response_generic
from app.core.dependiences import get_global_session
from app.core.exceptions import BadRequestError, NotFoundError
from app.core.schemas import ResponseGeneric, ResponseListGeneric
from app.core.utils import convert_orm_to_schema
from app.core.validators import Path_id, Query_limit, Query_offset
from app.exceptions import FileTypeError
from app.schemas.cargo_rate import (
    CargoDict,
    CargoRateBase,
    CargoRateForm,
)
from app.services.cargo_rate import CargoRateService

router = APIRouter(
    dependencies=[
        Depends(get_global_session),
    ]
)


@router.post(
    "/update_by_json", status_code=HTTPStatus.OK, response_model=ResponseGeneric[bool]
)
async def update_cargo_rates_by_json(request: Request, file: UploadFile = File(...)):
    if file.content_type != "application/json":
        raise FileTypeError(
            detail="Bad file type. It's not json file.",
        )
    await CargoRateService.update_cargo_rates_by_structure(
        request.state.session, json.load(io.BytesIO(await file.read()))
    )
    return ResponseGeneric[bool](data=True)


@router.post(
    "/update_by_dict", status_code=HTTPStatus.OK, response_model=ResponseGeneric[bool]
)
async def update_cargo_rates_by_dict(
    request: Request,
    data: CargoDict = Body(...),
):
    await CargoRateService.update_cargo_rates_by_structure(request.state.session, data)
    return ResponseGeneric[bool](data=True)


@router.get(
    "/",
    response_model=ResponseListGeneric[CargoRateBase],
    status_code=HTTPStatus.OK,
    summary="Get cargo rate list",
)
async def get_cargo_cate_list(
    request: Request,
    offset: int | None = Query_offset(),
    limit: int | None = Query_limit(default=100),
):
    cargo_rate_list, total_count = await CargoRateService.list(
        request.state.session, limit, offset
    )
    return ResponseListGeneric[CargoRateBase](
        data=convert_orm_to_schema(cargo_rate_list, CargoRateBase),
        total_count=total_count,
    )


@router.post(
    "/",
    response_model=ResponseGeneric[CargoRateBase],
    status_code=HTTPStatus.CREATED,
    summary="Create cargo rate",
)
@prepare_response_generic(schema=CargoRateBase, exceptions_if_none=BadRequestError)
async def create_cargo_rate(request: Request, cargo_rate_form: CargoRateForm):
    return await CargoRateService.create(request.state.session, cargo_rate_form)


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


@router.put(
    "/{cargo_rate_id}",
    response_model=ResponseGeneric[CargoRateBase],
    status_code=HTTPStatus.OK,
    summary="Update cargo rate",
)
@prepare_response_generic(schema=CargoRateBase, exceptions_if_none=BadRequestError)
async def update_cargo_rate(
    request: Request,
    cargo_rate_form: CargoRateForm,
    cargo_rate_id: int = Path_id(),
):
    return await CargoRateService.update(
        request.state.session, cargo_rate_id, cargo_rate_form
    )


@router.delete(
    "/{cargo_rate_id}",
    response_model=ResponseGeneric[bool],
    status_code=HTTPStatus.OK,
    summary="Delete cargo rate",
)
@prepare_response_generic(schema=bool, exceptions_if_none=BadRequestError)
async def delete_cargo_rate(
    request: Request,
    cargo_rate_id: int = Path_id(),
):
    return await CargoRateService.delete(request.state.session, cargo_rate_id)
