from fastapi import Path, Query
from pydantic import conint

MAX_INT = (2**31) - 1

Id = conint(ge=1, le=MAX_INT)


def Query_limit(
    default: int | None = 100, ge: int = 0, le: int = 1000, **kwargs
) -> Query:
    return Query(**{"default": default, "ge": ge, "le": le}, **kwargs)


def Query_offset(default: int = 0, ge: int = 0, le: int = MAX_INT, **kwargs) -> Query:
    return Query(**{"default": default, "ge": ge, "le": le}, **kwargs)


def Query_sort(default: int = "", max_length: int = 100, **kwargs) -> Query:
    regex_pattern = r"^[a-zA-Z_]+:(asc|desc)$"
    return Query(
        **{"default": default, "max_length": max_length, "pattern": regex_pattern},
        **kwargs,
    )


def Path_id(default: int = ..., ge: int = 1, le: int = MAX_INT, **kwargs) -> Query:
    return Path(**{"default": default, "ge": ge, "le": le}, **kwargs)
