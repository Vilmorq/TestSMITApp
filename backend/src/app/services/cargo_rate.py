from datetime import date, datetime

from sqlalchemy import and_, delete, func, or_, select, update, desc
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.validators import Id
from app.exceptions import DateError
from app.models.cargo_rate import CargoRate
from app.schemas.cargo import CargoType
from app.schemas.cargo_rate import (
    CargoDict,
    CargoRateBase,
    CargoRateCommon,
    CargoRateForm,
)


class CargoRateService:
    @classmethod
    def _validate_and_rebuild_structure(
        cls, data: CargoDict
    ) -> dict[tuple[date, CargoType], CargoRateForm]:
        cargo_rate_forms_dict = {}
        for date_str, cargo_rates_common_list in CargoDict(data).items():
            try:
                cargo_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError as err:
                raise DateError from err
            for cargo_rate_common in cargo_rates_common_list:
                if isinstance(cargo_rate_common, dict):
                    cargo_rate_common = CargoRateCommon(**cargo_rate_common)
                cargo_rate_forms_dict[(cargo_date, cargo_rate_common.type)] = (
                    CargoRateForm(date=cargo_date, **cargo_rate_common.model_dump())
                )

        return cargo_rate_forms_dict

    @classmethod
    async def update_cargo_rates_by_structure(
        cls,
        session: AsyncSession,
        data: CargoDict,
    ):
        cargo_rate_forms_dict = cls._validate_and_rebuild_structure(data)
        exist_cargo_rate_filter = (
            and_(CargoRate.date == cargo_rate.date, CargoRate.type == cargo_rate.type)
            for cargo_rate in cargo_rate_forms_dict.values()
        )
        exist_stmt = select(CargoRate).where(or_(*exist_cargo_rate_filter))
        exist_cargo_rate_list = (await session.execute(exist_stmt)).scalars().all()
        if exist_cargo_rate_list:
            # обновляем, если значение rate изменилось
            models_to_update = []
            for exist_cargo_rate in exist_cargo_rate_list:
                exist_cargo_key = (exist_cargo_rate.date, exist_cargo_rate.type)

                if cargo_rate_from_dict := cargo_rate_forms_dict.get(exist_cargo_key):
                    del cargo_rate_forms_dict[exist_cargo_key]

                    if cargo_rate_from_dict.rate != exist_cargo_rate.rate:
                        models_to_update.append(
                            # need 'id' slot, so here some mapping
                            CargoRateBase(
                                **cargo_rate_from_dict.model_dump(),
                                id=exist_cargo_rate.id,
                            )
                        )

            if models_to_update:
                for model_to_update in models_to_update:
                    await cls.update(
                        session,
                        model_to_update.id,
                        CargoRateForm.model_validate(model_to_update),
                    )

        models_to_add = cargo_rate_forms_dict.values()
        if models_to_add:
            # с массовым инсертом сложно получить логи на каждое добавление, так что через циклы
            # session.add_all(models_to_add)
            # await session.commit()
            for model_to_add in models_to_add:
                await cls.create(session, model_to_add)

    @classmethod
    def _paginate(
        cls,
        stmt,
        limit: int | None = None,
        offset: int | None = None,
    ):
        if limit:
            stmt = stmt.limit(limit)
        if offset:
            stmt = stmt.offset(offset)
        return stmt

    @classmethod
    async def list(
        cls,
        session: AsyncSession,
        limit: int | None = None,
        offset: int | None = None,
    ) -> [list[CargoRate], int]:
        count_stmt = select(func.count(CargoRate.id))
        filtered_stmt = cls._paginate(count_stmt)
        total_count = await session.scalar(filtered_stmt)

        if not total_count:
            return [], total_count
        stmt = cls._paginate(select(CargoRate), limit, offset).order_by(
            desc(CargoRate.id)
        )

        result = await session.execute(stmt)
        cargo_list: list[CargoRate] = result.scalars().all()

        return cargo_list, total_count

    @classmethod
    async def get_by_id(cls, session: AsyncSession, cargo_rate_id: Id) -> CargoRate:
        result = await session.execute(
            select(CargoRate).where(CargoRate.id == cargo_rate_id)
        )

        return result.scalar_one_or_none()

    @classmethod
    async def get_by_date_and_type(
        cls, session: AsyncSession, date_of_dispatch: date, cargo_type: CargoType
    ) -> CargoRate | None:
        stmt = select(CargoRate).where(
            and_(CargoRate.date == date_of_dispatch, CargoRate.type == cargo_type)
        )
        result = await session.execute(stmt)

        return result.scalar_one_or_none()

    @classmethod
    async def create(
        cls, session: AsyncSession, form: CargoRateForm
    ) -> CargoRate | None:
        new_cargo_rate = CargoRate(**form.model_dump())
        try:
            session.add(new_cargo_rate)
            await session.commit()
            # TODO нужна логика логирования действия
        except SQLAlchemyError:
            await session.rollback()
            # TODO нужна логика логирования ошибки
            return None
        await session.refresh(new_cargo_rate)

        return new_cargo_rate

    @classmethod
    async def update(
        cls,
        session: AsyncSession,
        cargo_rate_id: Id,
        form: CargoRateForm,
        current_model: CargoRate | None = None,
    ) -> CargoRate | None:
        if not current_model:
            current_model = await cls.get_by_id(session, cargo_rate_id)
            if not current_model:
                return None
        stmt = (
            update(CargoRate)
            .where(CargoRate.id == cargo_rate_id)
            .values(**form.model_dump())
        )
        try:
            await session.execute(stmt)
            await session.commit()
            # TODO нужна логика логирования действия
            await session.refresh(current_model)
            return current_model
        except SQLAlchemyError:
            pass  # TODO нужна логика логирования ошибки

    @classmethod
    async def delete(cls, session: AsyncSession, cargo_rate_id: Id) -> bool | None:
        current_model = await cls.get_by_id(session, cargo_rate_id)
        if not current_model:
            return None
        try:
            await session.execute(
                delete(CargoRate).where(CargoRate.id == cargo_rate_id)
            )
            await session.commit()
            # TODO нужна логика логирования действия
            return True
        except SQLAlchemyError:
            await session.rollback()
            # TODO нужна логика логирования ошибки
            return False
