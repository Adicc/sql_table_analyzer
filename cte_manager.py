"""
cte_manager.py
===================
Author: Ardian Gashi

User_Story: https://jira.telekom.de/browse/SDA-7438

Summary:
	This module provides functionality to detect and process Common Table Expressions (CTEs)
    in SQL queries.

    It includes functions to check for the presence of CTEs,
    extract their names and columns, and clean the extracted data.

Functions:
    1. check_for_ctes(sql: list[str])
        Checks if the SQL query contains any CTEs.
        Returns:
            bool: True if CTEs are detected, False otherwise.

    2. get_cte_name_values(sql: list[str])
        Returns the name of all CTEs and their corresponding indexes.
        Returns:
            list[tuple[int, str]]: A list of tuples containing index and name of CTEs.

    3. get_cte_columns(CTE_index: int, sql: list[str], display_colums=True)
        Returns all columns of the given CTE.
        Returns:
            list[str]: A list of columns for the corresponding CTE.

    4. get_ctes(sql: list[str], display_colums=True)
        Processes the SQL query to extract all Common Table Expressions (CTEs).
        Returns:
            list[CTE]: A list of CTE objects extracted from the SQL query.
"""

import re
import logging

from time_logging import time_logger
import cleaner


class CTE:
    """
    Represents a Common Table Expression (CTE).

    Attributes:
        index (int): The line index of the CTE in the SQL query.
        name (str): The name of the CTE.
        columns (list[str]): A list of columns within the CTE.
    """

    def __init__(self, index: int, name: str, columns: list[str]):
        self.index = index
        self.name = name
        self.columns = columns

### ------------------------------------------------------------------------------###


@time_logger
def check_for_ctes(sql: list[str]) -> bool:
    """
    Checks if the SQL query contains any CTEs.

    Args:
        sql (list[str]): A list of every line in a SQL query.

    Returns:
        bool: True if CTEs are detected, False otherwise.
    """
    for line in sql:
        if " WITH" in line.upper():
            logging.info("CTE detected in SQL")
            return True
    logging.critical("No CTE detected in SQL")
    return False


def get_cte_name_values(sql: list[str]) -> list[tuple[int, str]]:
    """
    Returns the name of all CTEs and their corresponding indexes.

    Args:
        sql (list[str]): A list of every line in a SQL query.

    Returns:
        list[tuple[int, str]]: A list of tuples containing index and name of CTEs.
    """
    cte_name_values = []
    pattern = re.compile(r'\b(\w+)\s+AS\b')
    for index, line in enumerate(sql):
        if bool(re.search(r" AS\s*\(", line)):
            match = pattern.search(line)
            if match:
                cte_name = match.group(1)
                cte_index = index
                cte_name_values.append((cte_index, cte_name))
                logging.info(f"Found CTE '{cte_name}' at index {cte_index}")
    return cte_name_values


def get_cte_columns(
        cte_index: int,
        sql: list[str],
        display_colums=True) -> list[str]:
    """
    Returns all columns of the given CTE.

    Args:
        sql (list[str]): A list of every line in a SQL query.
        CTE_index (int): The index of the list "sql" where the name of the CTE is located.

    Returns:
        list[str]: A list of columns for the corresponding CTE.
    """
    if display_colums:
        columns = []
        for index in range(cte_index, len(sql)):
            line = sql[index]
            if "FROM" in line:
                break
            columns.append(line)

        missing_select = True
        cte_columns = []
        for item in columns:
            if "SELECT" in item:
                missing_select = False
            if not missing_select:
                cte_columns.append(item)

        return cte_columns

    return []


### ------------------------------------------------------------------------------###


def get_ctes(sql: list[str], display_colums=True) -> list[CTE]:
    """
    Processes the SQL query to extract all Common Table Expressions (CTEs).

    Args:
        sql (list[str]): A list of every line in a SQL query.

    Returns:
        list[CTE]: A list of CTE objects extracted from the SQL query.
    """

    if check_for_ctes(sql):
        ctes = []
        cte_values = get_cte_name_values(sql)
        for cte_index, cte_name in cte_values:
            columns = get_cte_columns(cte_index, sql, display_colums)
            cte = CTE(cte_index, cte_name, columns)
            cte = cleaner.clean_columns(cte)
            ctes.append(cte)
        return ctes

    logging.error("No CTEs found, returning default CTE.")
    return None


### ------------------------------------------------------------------------------###


if __name__ == "__main__":
    print("cte_manager.py")
