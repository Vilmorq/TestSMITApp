from pydantic import BaseModel

from app.core.db import Base


# TODO mb finally use SQLModel...
def convert_orm_to_schema(
    data: list[Base] | Base, schema: type[BaseModel]
) -> list[BaseModel] | BaseModel:
    if not schema.__pydantic_core_schema__.get("config", {}).get("from_attributes"):
        raise ValueError("Set from_attributes True to schema")
    if isinstance(data, list):
        return [schema.model_validate(mdl) for mdl in data]
    return schema.model_validate(data)
