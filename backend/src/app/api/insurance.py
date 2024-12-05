from datetime import date
from http import HTTPStatus

from fastapi import APIRouter, Depends, Request

from app.core.decorators import prepare_response_generic
from app.core.dependiences import get_global_session
from app.core.exceptions import NotFoundError
from app.core.schemas import ResponseGeneric
from app.schemas.cargo import CargoType
from app.services.insurance import InsuranceService

router = APIRouter(
    dependencies=[
        Depends(get_global_session),
    ]
)


@router.get(
    "/calculate", status_code=HTTPStatus.OK, response_model=ResponseGeneric[float]
)
@prepare_response_generic(schema=float, exceptions_if_none=NotFoundError)
async def calculate_insurance_value(
    request: Request, cargo_type: CargoType, value: int, date_of_dispatch: date
):
    return await InsuranceService.calculate_insurance_value(
        request.state.session,
        date_of_dispatch,
        cargo_type,
        value,
    )
