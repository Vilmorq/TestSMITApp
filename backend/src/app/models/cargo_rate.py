from datetime import date

from sqlalchemy import (
    Date,
    Enum,
    Float,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base
from app.schemas.cargo import CargoType


class CargoRate(Base):
    __tablename__ = "cargo_rates"
    __table_args__ = (
        UniqueConstraint(
            "type",
            "date",
            name="ix_cargo_rates_type_date",
        ),
    )

    id: Mapped[int] = mapped_column(
        autoincrement=True,
        nullable=False,
        unique=True,
        primary_key=True,
        init=False,
    )
    type: Mapped[CargoType] = mapped_column(Enum(CargoType), nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    rate: Mapped[float] = mapped_column(Float, nullable=False)
