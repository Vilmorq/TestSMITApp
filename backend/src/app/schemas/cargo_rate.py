from datetime import date
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, constr

from app.core.validators import Id
from app.schemas.cargo import CargoType


class CargoRateCommon(BaseModel):
    type: CargoType = Field(alias="cargo_type")
    rate: Annotated[float, Field(strict=True, gt=0)]

    model_config = ConfigDict(populate_by_name=True)


class CargoRateForm(CargoRateCommon):
    date: date


class CargoRateBase(CargoRateForm):
    id: Id

    model_config = ConfigDict(from_attributes=True)


CargoDict = dict[
    constr(
        pattern=r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$"
    ),  # date pattern for YYYY-MM-DD
    list[CargoRateCommon],
]
