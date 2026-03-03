from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas


@dataclass(frozen=True)
class Task2_2Configuration:
    duration_threshold_minutes: int


@dataclass(frozen=True)
class Task2_3Configuration:
    exact_country_name: str
    listed_in_substring: str


@dataclass(frozen=True)
class Task2_4Configuration:
    specific_release_year: int
    release_year_range_start: int
    release_year_range_end: int


@dataclass(frozen=True)
class Task2_5Configuration:
    significant_duration_threshold_minutes: int
    significant_cast_size_threshold: int


@dataclass(frozen=True)
class Task2_6Configuration:
    group_country_a: str
    group_country_b: str


@dataclass(frozen=True)
class Task2_7Configuration:
    duration_threshold_minutes: int
    exclude_rating_substring: str
    documentary_substring: str


@dataclass(frozen=True)
class Task2Configuration:
    task_2_2: Task2_2Configuration
    task_2_3: Task2_3Configuration
    task_2_4: Task2_4Configuration
    task_2_5: Task2_5Configuration
    task_2_6: Task2_6Configuration
    task_2_7: Task2_7Configuration


def load_task2_configuration(configuration_file_path: Path) -> Task2Configuration:
    configuration_table: pandas.DataFrame = pandas.read_csv(configuration_file_path)

    if "key" not in configuration_table.columns or "value" not in configuration_table.columns:
        raise ValueError("Configuration CSV must contain columns: key,value")

    configuration_map: dict[str, str] = _build_configuration_map(configuration_table)

    return Task2Configuration(
        task_2_2=Task2_2Configuration(
            duration_threshold_minutes=_get_int(configuration_map, "task_2_2.duration_threshold_minutes"),
        ),
        task_2_3=Task2_3Configuration(
            exact_country_name=_get_str(configuration_map, "task_2_3.exact_country_name"),
            listed_in_substring=_get_str(configuration_map, "task_2_3.listed_in_substring"),
        ),
        task_2_4=Task2_4Configuration(
            specific_release_year=_get_int(configuration_map, "task_2_4.specific_release_year"),
            release_year_range_start=_get_int(configuration_map, "task_2_4.release_year_range_start"),
            release_year_range_end=_get_int(configuration_map, "task_2_4.release_year_range_end"),
        ),
        task_2_5=Task2_5Configuration(
            significant_duration_threshold_minutes=_get_int(configuration_map,
                                                            "task_2_5.significant_duration_threshold_minutes"),
            significant_cast_size_threshold=_get_int(configuration_map, "task_2_5.significant_cast_size_threshold"),
        ),
        task_2_6=Task2_6Configuration(
            group_country_a=_get_str(configuration_map, "task_2_6.group_country_a"),
            group_country_b=_get_str(configuration_map, "task_2_6.group_country_b"),
        ),
        task_2_7=Task2_7Configuration(
            duration_threshold_minutes=_get_int(configuration_map, "task_2_7.duration_threshold_minutes"),
            exclude_rating_substring=_get_str(configuration_map, "task_2_7.exclude_rating_substring"),
            documentary_substring=_get_str(configuration_map, "task_2_7.documentary_substring"),
        ),
    )


def _build_configuration_map(configuration_table: pandas.DataFrame) -> dict[str, str]:
    configuration_map: dict[str, str] = {}

    for _, row in configuration_table.iterrows():
        key_value: str = str(row["key"]).strip()
        value_value: str = str(row["value"]).strip()
        configuration_map[key_value] = value_value

    return configuration_map


def _get_str(configuration_map: dict[str, str], key: str) -> str:
    if key not in configuration_map:
        raise ValueError("Missing configuration key: " + key)
    return configuration_map[key]


def _get_int(configuration_map: dict[str, str], key: str) -> int:
    raw_value: str = _get_str(configuration_map, key)
    try:
        return int(raw_value)
    except ValueError as exception:
        raise ValueError("Configuration key '" + key + "' must be an integer, got: " + raw_value) from exception
