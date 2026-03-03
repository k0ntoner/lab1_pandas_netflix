from __future__ import annotations

from pathlib import Path

import pandas


def load_csv_dataset(dataset_path: Path) -> pandas.DataFrame:
    return pandas.read_csv(dataset_path)


def save_parquet_dataset(data_frame: pandas.DataFrame, dataset_path: Path) -> None:
    dataset_path.parent.mkdir(parents=True, exist_ok=True)
    data_frame.to_parquet(dataset_path, index=False)


def load_parquet_dataset(dataset_path: Path) -> pandas.DataFrame:
    return pandas.read_parquet(dataset_path)
