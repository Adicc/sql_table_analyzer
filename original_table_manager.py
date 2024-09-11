"""
original_table_manager.py
===================
Author: Ardian Gashi

User_Story: https://jira.telekom.de/browse/SDA-7438

Summary:
	Finds the table from which all data gets extracted from.
    Creates an instance of the OriginalTable class in which the following gets stored:
    - position in the SQL-query
    - table name
    - column names


Functions:
    1. get_original_table_columns(original_table_index: int, sql: list[str],
        display_colums: bool)
        Extracts the columns of a source table from the SQL script.
        Returns:
            list[str]: A list of column names in the correct format for the original table.

    2. get_original_tables(sql: list[str], final_table: FinalTable | None, display_columns: bool):
        Extracts the source tables and their columns from the provided SQL script.
        Returns:
            list[OriginalTable]: A list of OriginalTable (source table) objects containing
                                    the index, name, and columns of each original table.
"""
import re
import logging

import cleaner
from time_logging import time_logger


class OriginalTable:
    """Stores the relevant data of the source table in a SQL-query:
        - index in the SQL-query
        - table name
        - columns
    """

    def __init__(self, index, name, columns):
        self.index = index
        self.name = name
        self.columns = columns

### ------------------------------------------------------------------------------###


def get_original_table_columns(
        original_table_index,
        sql,
        display_colums=True):
    """
    Extracts the columns of a 'original table' from the SQL script.

    Args:
        original_table_index (int): The index of the original table in the SQL script.
        sql (list of str): The list of SQL script lines.

    Returns:
        list of str: A list of column names in the correct format for the original table.
    """
    if display_colums:
        unfiltered_columns = []
        line = sql[original_table_index]

        # Add all lines until the SELECT statement (from bottom to top)
        while "SELECT" not in line:
            original_table_index -= 1
            line = sql[original_table_index].lstrip()
            unfiltered_columns.append(line)

        # Remove SELECT and other characters
        for column in unfiltered_columns[:]:
            if "SELECT" in column.upper():
                splitter = column.split("SELECT")
                unfiltered_columns.remove(column)
                column = splitter[1]
                unfiltered_columns.append(column)

        # Clean and process columns
        unfiltered_columns.reverse()
        unfiltered_columns = [''.join(column_name.split(','))
                              for column_name in unfiltered_columns]
        unfiltered_columns = [column_name.strip()
                              for column_name in unfiltered_columns]

        if len(unfiltered_columns) == 1:
            splitter = unfiltered_columns[0].split()
            unfiltered_columns = list(splitter)

        logging.info(f"Extracted columns for table at index {
            original_table_index}: {unfiltered_columns}")

        return unfiltered_columns

    return []

### ------------------------------------------------------------------------------###


@time_logger
def get_original_tables(sql, final_table, display_columns=True):
    """
    Extracts original tables and their columns from the provided SQL script.

    Args:
        sql (list[str]): The list of SQL script lines.
        final_table (OriginalTable or None): The final table to exclude from the search.
                                            Can be None.
        display_columns (bool): Whether to display columns or not. Default is True.

    Returns:
        list[OriginalTable]: A list of OriginalTable objects containing the index,
                            name, and columns of each original table.
    """

    final_table_name = final_table.name if final_table else None
    original_tables = []

    for index, element in enumerate(sql):
        match = re.search(r'ocean_fs_prod\.\S+', element)
        if match and (not final_table_name or final_table_name not in element):
            original_table_name = match.group()
            original_table_index = index

            logging.info(f"Found original table '{
                original_table_name}' at index {original_table_index}")

            columns = get_original_table_columns(
                original_table_index, sql, display_columns)
            table = OriginalTable(
                original_table_index,
                original_table_name,
                columns)
            table = cleaner.clean_columns(table)
            original_tables.append(table)
        else:
            logging.warning("No original tables found!")

    return original_tables


# ---------------------------------------------------------------------------------


if __name__ == "__main__":
    print("original_table_manager.py")
