from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.cargo import CargoType
from app.services.cargo_rate import CargoRateService


class InsuranceService:
    @classmethod
    async def calculate_insurance_value(
        cls,
        session: AsyncSession,
        date_of_dispatch: date,
        cargo_type: CargoType,
        value: int,
    ) -> float:
        if cargo_rate := await CargoRateService.get_by_date_and_type(
            session, date_of_dispatch, cargo_type
        ):
            return cargo_rate.rate * value
