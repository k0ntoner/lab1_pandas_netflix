from __future__ import annotations

from pathlib import Path

PROJECT_ROOT: Path = Path(__file__).resolve().parents[2]

DATA_RAW_DIRECTORY: Path = PROJECT_ROOT / "data" / "raw"
DATA_PROCESSED_DIRECTORY: Path = PROJECT_ROOT / "data" / "processed"

RAW_DATASET_FILE_NAME: str = "netflix_titles.csv"
RAW_DATASET_FILE_PATH: Path = DATA_RAW_DIRECTORY / RAW_DATASET_FILE_NAME

CLEANED_DATASET_FILE_NAME: str = "netflix_cleaned.parquet"
CLEANED_DATASET_FILE_PATH: Path = DATA_PROCESSED_DIRECTORY / CLEANED_DATASET_FILE_NAME

DATA_CONFIG_DIRECTORY: Path = PROJECT_ROOT / "data" / "config"
TASK_2_CONFIGURATION_FILE_PATH: Path = DATA_CONFIG_DIRECTORY / "task2_configuration.csv"
