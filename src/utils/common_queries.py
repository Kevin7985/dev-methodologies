from typing import Any

from sqlalchemy import Column, bindparam, func, select, text


def build_jsonb_filter(jsonb_column: Column[Any], sought_values: list[str]):
    sought_values = [str(uuid) for uuid in sought_values]
    jsonb_filter = text(f"({jsonb_column.name} ?| :sought_values)").bindparams(
        bindparam("sought_values", sought_values)
    )
    return jsonb_filter


def build_json_agg_subquery(jsonb_column: Column[Any], joined_model: Any, agg_column: Column[Any]):
    warehouses_subquery = (  # noqa: ECE001
        select(func.json_agg(agg_column))
        .select_from(joined_model)
        .where(func.jsonb_contains(jsonb_column, func.jsonb_build_array(joined_model.guid)))
        .scalar_subquery()
    )
    return warehouses_subquery
