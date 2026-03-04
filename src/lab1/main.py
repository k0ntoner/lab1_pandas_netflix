from __future__ import annotations

import pandas

from lab1.analysis_task2 import (
    task_2_1_total_rows,
    task_2_2_numeric_metrics,
    task_2_3_categories_and_text,
    task_2_4_ranges_and_slices,
    task_2_5_combined_filters,
    task_2_6_group_comparison,
    task_2_7_complex_filter_and_plot,
)
from lab1.cleaning import clean_dataset
from lab1.config import RAW_DATASET_FILE_PATH, TASK_2_CONFIGURATION_FILE_PATH
from lab1.io import load_csv_dataset
from lab1.task2_configuration import load_task2_configuration


def main() -> None:
    raw_data_frame: pandas.DataFrame = load_csv_dataset(RAW_DATASET_FILE_PATH)

    processed_data_frame: pandas.DataFrame = clean_dataset(raw_data_frame)

    task2_configuration = load_task2_configuration(TASK_2_CONFIGURATION_FILE_PATH)

    task_2_1_total_rows(processed_data_frame)
    task_2_2_numeric_metrics(processed_data_frame, task2_configuration.task_2_2)
    task_2_3_categories_and_text(processed_data_frame, task2_configuration.task_2_3)
    task_2_4_ranges_and_slices(processed_data_frame, task2_configuration.task_2_4)
    task_2_5_combined_filters(processed_data_frame, task2_configuration.task_2_5)
    task_2_6_group_comparison(processed_data_frame, task2_configuration.task_2_6)
    task_2_7_complex_filter_and_plot(processed_data_frame, task2_configuration.task_2_7)


if __name__ == "__main__":
    main()
