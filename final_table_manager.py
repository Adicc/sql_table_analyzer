"""
finale_table_manager.py
===================
Author: Ardian Gashi

User_Story: https://jira.telekom.de/browse/SDA-7438

Summary:
	Finds the table in wich all data gets inserted into.
    Creates an instance of the FinalTable class in which the following gets stored:
    - position in the SQL-query
    - table name
    - column names


Functions:
	1. find_final_table_name(sql: list[str])
	    Finds the name of the final table in the SQL query.
        Returns:
            str: The name of the final table if found, otherwise None.

    2. get_final_table_index(sql)
        Finds the index of the final table name in the SQL query.
        Returns:
            int: The index of the final table if found, otherwise None.

    3. get_final_table_columns(table_index: int, sql: List[str], display_colums: bool):
        Returns all columns of the final table.
        Returns:
            list[str]: A list of columns for the final table.

    4. get_final_table(sql: List, display_colums: bool):
        Processes the SQL query to extract the final table details.
        Returns:
            FinalTable: An object containing the final table details.

"""
import re
import logging
import cleaner

from time_logging import time_logger


class FinalTable:
    """Stores the relevant data of the table of the SQL-query
        in wich the data gets inserted into:
        - index in the SQL-query
        - table name
        - columns
    """

    def __init__(self, index, name, columns):
        self.index = index
        self.name = name
        self.columns = columns

    def __len__(self):
        return len(self.name)

### ------------------------------------------------------------------------------###


def find_final_table_name(sql):
    """
    Finds the name of the final table in the SQL query.

    Args:
        sql (list): A list of every line in a SQL query.

    Returns:
        str: The name of the final table if found, otherwise None.
    """
    pattern = re.compile(r'INSERT OVERWRITE .*(ocean_fs_prod\.\S+)')
    for index, line in enumerate(sql):
        match = pattern.search(line)
        if "INSERT OVERWRITE" in line and match:
            final_table_name = match.group(1)
            logging.info(
                f"Found final table name '{final_table_name}' at line {index}")
            return final_table_name
        if "INSERT OVERWRITE" in line and not match:
            final_table_name = sql[index + 1].strip()
            logging.info(f"Found final table name '{
                final_table_name}' at line {index + 1}")
            return final_table_name

    logging.warning("Final table name not found in SQL.")
    return None


def get_final_table_index(sql):
    """
    Finds the index of the final table name in the SQL query.

    Args:
        sql (list): A list of every line in a SQL query.

    Returns:
        int: The index of the final table if found, otherwise None.
    """
    for line in reversed(sql):
        if "FROM" in line:
            index = sql.index(line)
            logging.info(f"Found final table index at line {index}")
            return index

    logging.warning("Final table index not found in SQL.")
    return None


def get_final_table_columns(table_index, sql, display_colums=True):
    """
    Returns all columns of the final table.

    Args:
        table_index (int): The index of the list "sql" where the final table is located.
        sql (list): A list of every line in a SQL query.

    Returns:
        list: A list of columns for the final table.
    """
    if display_colums:
        unfiltered_columns = []
        line = sql[table_index]

        # Add all lines until the SELECT statement (from bottom to top)
        while "SELECT" not in line.upper():
            table_index -= 1
            line = sql[table_index].lstrip()
            unfiltered_columns.append(line)

        # Remove SELECT and other characters
        filtered_columns = []
        for column in unfiltered_columns:
            if "SELECT" in column.upper():
                column = column.split("SELECT", 1)[1]
            filtered_columns.append(column.strip())

        filtered_columns.reverse()
        filtered_columns = [col.replace(',', '').strip()
                            for col in filtered_columns]

        if len(filtered_columns) == 1:
            filtered_columns = filtered_columns[0].split()

        return filtered_columns
    return []

### ------------------------------------------------------------------------------###


@time_logger
def get_final_table(sql, display_colums=True):
    """
    Processes the SQL query to extract the final table details.

    Args:
        sql (list): A list of every line in a SQL query.

    Returns:
        FinalTable: An object containing the final table details.
    """

    name = find_final_table_name(sql)
    index = get_final_table_index(sql)
    if name is None or index is None:
        logging.error("Failed to find final table details.")
        return None

    columns = get_final_table_columns(index, sql, display_colums)
    final_table = FinalTable(index, name, columns)
    final_table = cleaner.clean_columns(final_table)

    return final_table


if __name__ == "__main__":
    print("final_table_manager.py")
