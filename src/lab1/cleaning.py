from __future__ import annotations

import pandas

COLUMNS_TO_KEEP: tuple[str, ...] = (
    "show_id",
    "type",
    "title",
    "cast",
    "country",
    "release_year",
    "rating",
    "duration",
    "listed_in"
)


def clean_dataset(raw_data_frame: pandas.DataFrame) -> pandas.DataFrame:
    data_frame: pandas.DataFrame = raw_data_frame[list(COLUMNS_TO_KEEP)].copy()

    data_frame = data_frame.dropna(subset=["show_id"])

    data_frame = format_column_types(data_frame)

    return data_frame


def format_column_types(data_frame: pandas.DataFrame) -> pandas.DataFrame:
    data_frame["show_id"] = data_frame["show_id"].astype("string")
    data_frame["type"] = data_frame["type"].astype("string")
    data_frame["title"] = data_frame["title"].astype("string")
    data_frame["cast"] = (
        data_frame["cast"]
        .fillna("")
        .astype("string")
        .apply(lambda value: [actor.strip() for actor in value.split(",")] if value else [])
    )
    data_frame["country"] = data_frame["country"].astype("string")
    data_frame["release_year"] = pandas.to_datetime(
        data_frame["release_year"],
        format="%Y",
        errors="coerce"
    )

    data_frame["rating"] = data_frame["rating"].astype("string")

    data_frame["duration_minutes"] = (
        data_frame["duration"]
        .fillna("")
        .astype("string")
        .str.replace(" min", "", regex=False)
    )

    data_frame["duration_minutes"] = pandas.to_numeric(
        data_frame["duration_minutes"],
        errors="coerce"
    )

    return data_frame
