"""
cleaner.py
===================
Author: Ardian Gashi

User_Story: https://jira.telekom.de/browse/SDA-7438

Summary:
	This module provides functionality to clean and format columns of a table object.
    The primary function in this module, `clean_columns`, modifies the column format
    to ensure it is clean and readable.


Functions:
	1. clean_columns(table: CTE | FinalTable | OriginalTable):
        Cleans and formats the columns of the given Table object.

        The function will return the Table object with cleaned and formatted
        columns.
        The Table object should have 'name' and 'columns' attributes.
        The columns should be a list of strings.


		Returns:
			CTE | FinalTable | OriginalTable : The tables with the formatted columns

"""


import logging
from time_logging import time_logger


@time_logger
def clean_columns(table):
    """
    Changes the format of the Table to look clean and readable.

    Args:
        table (Table): The name and the columns of a Table object.
                      Also the index of the Table in an Abstract Syntax Tree.

    Returns:
        Table: The given Table object with columns in the right format.
    """

    logging.info(f"Cleaning columns for table '%s'", table.name)

    # Remove 'SELECT' keyword and strip each line
    table.columns = [line.replace('SELECT', '').strip()
                     for line in table.columns]
    logging.info(
        f"Removed 'SELECT' keyword and stripped lines for table '{
            table.name}'")

    # Split lines at ',' and flatten the list
    new_string_list = []
    for line in table.columns:
        new_string_list.extend(line.split(','))

    table.columns = [line.strip() for line in new_string_list]
    table.columns = "\n".join(table.columns)

    logging.info(f"Cleaned columns for table '{table.name}'")

    return table


# ------------------------------------------------------------------------
if __name__ == "__main__":
    print("cleaner.py")
