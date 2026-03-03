from __future__ import annotations

import pandas

from lab1.task2_configuration import (
    Task2_2Configuration,
    Task2_3Configuration,
    Task2_4Configuration,
    Task2_5Configuration,
    Task2_6Configuration,
    Task2_7Configuration,
)


def task_2_1_total_rows(processed_data_frame: pandas.DataFrame) -> None:
    """
    TASK 2.1

    Calculates total number of rows after cleaning/casting.

    Args:
        processed_data_frame (pandas.DataFrame): Cleaned dataset.

    Returns:
        None
    """
    print("\nTASK 2.1 — Total rows after cleaning")
    print("Total rows:", len(processed_data_frame))


def task_2_2_numeric_metrics(processed_data_frame: pandas.DataFrame, configuration: Task2_2Configuration) -> None:
    """
    TASK 2.2

    Numeric metric: duration_minutes (movies only, NaN for TV shows).
    1) Filter rows where duration_minutes > threshold.
    2) Count filtered rows.
    3) Average of another numeric column for filtered subset: release_year as year number.
    4) Print 10 show_id with the largest duration_minutes.

    Args:
        processed_data_frame (pandas.DataFrame): Cleaned dataset.
        configuration (Task2_2Configuration): Task-specific configuration.

    Returns:
        None
    """
    duration_threshold_minutes: int = configuration.duration_threshold_minutes

    filtered_data_frame: pandas.DataFrame = processed_data_frame[
        processed_data_frame["duration_minutes"].notna()
        & (processed_data_frame["duration_minutes"] > duration_threshold_minutes)
        ].copy()

    filtered_rows_count: int = len(filtered_data_frame)

    average_release_year: float = float(filtered_data_frame["release_year"].dt.year.mean())

    top_10_by_duration: pandas.DataFrame = (
        filtered_data_frame.sort_values(by="duration_minutes", ascending=False)
        .head(10)[["show_id", "duration_minutes"]]
    )

    print("\nTASK 2.2 — Numeric metrics")
    print("Filter: duration_minutes >", duration_threshold_minutes)
    print("Filtered rows:", filtered_rows_count)
    print("Average release year (filtered subset):", average_release_year)
    print("Top 10 by duration_minutes (show_id + duration_minutes):")
    print(top_10_by_duration.to_string(index=False))


def task_2_3_categories_and_text(processed_data_frame: pandas.DataFrame, configuration: Task2_3Configuration) -> None:
    """
    TASK 2.3

    1) Exact match by country: country == exact_country_name
    2) Partial match by substring in listed_in: contains(listed_in_substring)
    3) Count rows that satisfy both.
    4) Share of rows that satisfy (1) but not (2).
    5) Count rows that satisfy neither (1) nor (2).

    Args:
        processed_data_frame (pandas.DataFrame): Cleaned dataset.
        configuration (Task2_3Configuration): Task-specific configuration.

    Returns:
        None
    """
    exact_country_name: str = configuration.exact_country_name
    listed_in_substring: str = configuration.listed_in_substring

    country_series: pandas.Series = processed_data_frame["country"].fillna("").astype("string").str.strip()
    listed_in_series: pandas.Series = processed_data_frame["listed_in"].fillna("").astype("string")

    condition_country: pandas.Series = country_series.eq(exact_country_name)
    condition_listed_in: pandas.Series = listed_in_series.str.contains(listed_in_substring, case=False, na=False)

    count_country: int = int(condition_country.sum())
    count_listed_in: int = int(condition_listed_in.sum())
    count_both: int = int((condition_country & condition_listed_in).sum())

    count_country_only: int = int((condition_country & ~condition_listed_in).sum())
    share_country_only: float = (count_country_only / count_country) if count_country > 0 else 0.0

    count_neither: int = int((~condition_country & ~condition_listed_in).sum())

    print("\nTASK 2.3 — Categories and text")
    print("Count where country ==", exact_country_name, ":", count_country)
    print("Count where listed_in contains", listed_in_substring, ":", count_listed_in)
    print("Count where both conditions are true:", count_both)
    print("Share where country condition is true but substring condition is false:", share_country_only)
    print("Count where neither condition is true:", count_neither)


def task_2_4_ranges_and_slices(processed_data_frame: pandas.DataFrame, configuration: Task2_4Configuration) -> None:
    """
    TASK 2.4

    1) Count rows where release_year == specific_release_year.
    2) Count rows where release_year in [range_start; range_end] using a single complex condition.
    3) Check if count from (1) is greater than count from (2).

    Args:
        processed_data_frame (pandas.DataFrame): Cleaned dataset.
        configuration (Task2_4Configuration): Task-specific configuration.

    Returns:
        None
    """
    specific_release_year: int = configuration.specific_release_year
    range_start: int = configuration.release_year_range_start
    range_end: int = configuration.release_year_range_end

    release_year_numbers: pandas.Series = processed_data_frame["release_year"].dt.year

    count_specific_year: int = int((release_year_numbers == specific_release_year).sum())
    count_in_range: int = int(((release_year_numbers >= range_start) & (release_year_numbers <= range_end)).sum())

    is_specific_year_bigger: bool = count_specific_year > count_in_range

    print("\nTASK 2.4 — Ranges and slices")
    print("Count where release_year ==", specific_release_year, ":", count_specific_year)
    print("Count where release_year in range", f"[{range_start}; {range_end}]:", count_in_range)
    print("Is specific-year count greater than range count:", is_specific_year_bigger)


def task_2_5_combined_filters(processed_data_frame: pandas.DataFrame, configuration: Task2_5Configuration) -> None:
    """
    TASK 2.5

    Defines "significant" records:
        duration_minutes >= significant_duration_threshold_minutes
        AND cast_size >= significant_cast_size_threshold

    Then:
        - prints top-5 by duration_minutes
        - calculates median cast_size for top-10 sorted by release_year (another metric)

    Args:
        processed_data_frame (pandas.DataFrame): Cleaned dataset.
        configuration (Task2_5Configuration): Task-specific configuration.

    Returns:
        None
    """
    significant_duration_threshold_minutes: int = configuration.significant_duration_threshold_minutes
    significant_cast_size_threshold: int = configuration.significant_cast_size_threshold

    cast_size_series: pandas.Series = processed_data_frame["cast"].apply(len)

    significant_data_frame: pandas.DataFrame = processed_data_frame[
        processed_data_frame["duration_minutes"].notna()
        & (processed_data_frame["duration_minutes"] >= significant_duration_threshold_minutes)
        & (cast_size_series >= significant_cast_size_threshold)
        ].copy()

    significant_data_frame["cast_size"] = cast_size_series.loc[significant_data_frame.index].astype("Int64")

    top_5_by_duration: pandas.DataFrame = significant_data_frame.sort_values(by="duration_minutes",
                                                                             ascending=False).head(5)

    top_10_by_release_year: pandas.DataFrame = (
        significant_data_frame.sort_values(by="release_year", ascending=False)
        .head(10)
    )

    median_cast_size_top_10: float = float(top_10_by_release_year["cast_size"].median())

    print("\nTASK 2.5 — Combined filters and evaluations")
    print(
        "Significant subset size (duration_minutes >= "
        + str(significant_duration_threshold_minutes)
        + " AND cast_size >= "
        + str(significant_cast_size_threshold)
        + "):",
        len(significant_data_frame),
    )
    print("Top 5 by duration_minutes:")
    print(top_5_by_duration[["show_id", "title", "duration_minutes", "cast_size"]].to_string(index=False))
    print("Median cast_size for top 10 sorted by release_year:", median_cast_size_top_10)


def task_2_6_group_comparison(processed_data_frame: pandas.DataFrame, configuration: Task2_6Configuration) -> None:
    """
    TASK 2.6

    Compares two groups (countries):
        - creates 2 DataFrames (country A and country B)
        - builds a new DataFrame with:
            category_name, total_records, average_value
      where average_value is average release year number.

    Args:
        processed_data_frame (pandas.DataFrame): Cleaned dataset.
        configuration (Task2_6Configuration): Task-specific configuration.

    Returns:
        None
    """
    group_country_a: str = configuration.group_country_a
    group_country_b: str = configuration.group_country_b

    country_series: pandas.Series = processed_data_frame["country"].fillna("").astype("string").str.strip()

    group_a_data_frame: pandas.DataFrame = processed_data_frame[country_series.eq(group_country_a)].copy()
    group_b_data_frame: pandas.DataFrame = processed_data_frame[country_series.eq(group_country_b)].copy()

    comparison_data_frame: pandas.DataFrame = pandas.DataFrame(
        {
            "category_name": [group_country_a, group_country_b],
            "total_records": [len(group_a_data_frame), len(group_b_data_frame)],
            "average_value": [
                group_a_data_frame["release_year"].dt.year.mean(),
                group_b_data_frame["release_year"].dt.year.mean(),
            ],
        }
    )

    print("\nTASK 2.6 — Group comparison")
    print(comparison_data_frame.to_string(index=False))


def task_2_7_complex_filter_and_plot(processed_data_frame: pandas.DataFrame,
                                     configuration: Task2_7Configuration) -> None:
    """
    TASK 2.7

    Complex filter with AND, OR, NOT:
        ((Movie AND duration_minutes >= threshold) OR (TV Show AND listed_in contains documentary_substring))
        AND NOT (rating contains exclude_rating_substring)

    Plot:
        Bar chart: number of titles per release year.

    Args:
        processed_data_frame (pandas.DataFrame): Cleaned dataset.
        configuration (Task2_7Configuration): Task-specific configuration.

    Returns:
        None
    """
    duration_threshold_minutes: int = configuration.duration_threshold_minutes
    exclude_rating_substring: str = configuration.exclude_rating_substring
    documentary_substring: str = configuration.documentary_substring

    type_series: pandas.Series = processed_data_frame["type"].fillna("").astype("string")
    rating_series: pandas.Series = processed_data_frame["rating"].fillna("").astype("string")
    listed_in_series: pandas.Series = processed_data_frame["listed_in"].fillna("").astype("string")

    is_movie: pandas.Series = type_series.eq("Movie")
    is_tv_show: pandas.Series = type_series.eq("TV Show")

    is_long_movie: pandas.Series = processed_data_frame["duration_minutes"].notna() & (
            processed_data_frame["duration_minutes"] >= duration_threshold_minutes
    )

    is_documentary: pandas.Series = listed_in_series.str.contains(documentary_substring, case=False, na=False)

    is_not_excluded_rating: pandas.Series = ~rating_series.str.contains(exclude_rating_substring, case=False, na=False)

    complex_filtered_data_frame: pandas.DataFrame = processed_data_frame[
        ((is_movie & is_long_movie) | (is_tv_show & is_documentary)) & is_not_excluded_rating
        ].copy()

    print("\nTASK 2.7 — Complex filter and plot")
    print("Complex filter result rows:", len(complex_filtered_data_frame))

    releases_per_year: pandas.Series = (
        processed_data_frame["release_year"].dt.year
        .dropna()
        .astype(int)
        .value_counts()
        .sort_index()
    )

    plot_axes = releases_per_year.plot(kind="bar", title="Number of Netflix titles by release year")
    plot_axes.set_xlabel("Release year")
    plot_axes.set_ylabel("Number of titles")
