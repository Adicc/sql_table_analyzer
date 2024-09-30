"""
analyzer.py
===================
Author: Ardian Gashi

User_Story: https://jira.telekom.de/browse/SDA-7438

Summary:
	This module provides functionality to extract SQL queries from a file and
    identify and replace variable names within these queries.

Functions:
	1. extract_sql_queries(file_path: str)
	    Returns:
            sql_queries: list[str]

    2. get_var_name(sql_query: str)
        Returns:
            var_name: str | None

    3. find_var_data(file_path: str, var_name: str)
        Finds the table name corresponding to the given variable name in the AST list.
        Returns:
            var_data: str | None

    4. insert_data_into_var(sql_query: str, var_data: str, var_name: str)
        Replaces occurrences of the variable name with the table name in the SQL statement.
        Returns:
            sql_query: str

    5. replace_var_names(file_path: str, sql_query: str)
        Replaces variable names in SQL statements with corresponding table names found in the source file.
        Returns:
            sql_query: str

"""

import logging
import re

from time_logging import time_logger


#### ----------------------------------------------------------------------------------####
@time_logger
def extract_sql_queries(file_path):
    """Finds multiline strings, which contain SQL-Keywords.

    Args:
        file_path (string): The path to the file, which gets analyzed

    Returns:
        list[str]: A list with each SQL-Query as a string from the given file
    """
    # Open the file
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Regex pattern for strings that start and end with ''' or """
    string_pattern = re.compile(
        r'\'\'\'[\s\S]*?\'\'\'|\"\"\"[\s\S]*?\"\"\"',
        re.DOTALL
    )

    # Regex-pattern for SQL-Queries
    sql_pattern = re.compile(
        r'(?i)\bSELECT\b[\s\S]*?\bFROM\b'
    )

    sql_queries = []

    for match in string_pattern.finditer(content):
        # Remove the ''' from the beginning and the end
        string_content = match.group(0)[3:-3]
        if sql_pattern.search(string_content):
            sql_queries.append(string_content.strip())

    return sql_queries
#### ----------------------------------------------------------------------------------####


def get_var_name(sql_query):
    """
    Extracts the variable name enclosed in curly braces from the
    SQL statement.

    Args:
        sql_query (str): The sql-query as a string

    Returns:
        str: The extracted variable name if found, None otherwise.
    """
    for line in sql_query:
        if "{" in line:
            # Extract variable name enclosed in curly braces
            var_name = re.search(r"\{(.*?)\}", line)
            if var_name:
                var_name = var_name.group(1)
                logging.info(f"Variable name extracted: '{var_name}'")
                return var_name
    return None


def find_var_data(file_path, var_name):
    """
    Finds the table name corresponding to the given variable name in the AST list.

    Args:
        ast_list (list): The AST as a list.
        var_name (str): The variable name to find the table name for.

    Returns:
        str: The table name if found, None otherwise.
    """

    with open(file_path, "r", encoding='utf-8') as file:
        content = file.read()

    var_data = re.search(
        r'\b{}\b\s*=\s*([\'"])(.*?)(\1)'.format(var_name),
        content)
    if var_data:
        var_data = var_data.group(2)
        return var_data
    return None


def insert_data_into_var(sql_query, var_data, var_name):
    """
    Replaces occurrences of the variable name with the table name in the SQL statement.

    Args:
        func (Function): The Function object containing the SQL statement.
        table_name (str): The table name to replace the variable name with.
        var_name (str): The variable name to be replaced.
    """
    if var_name and var_data:
        for index, line in enumerate(sql_query):
            if var_name in line:
                sql_query[index] = line.replace(
                    f"{{{var_name}}}", var_data)
                logging.info(f"Variable name '{var_name}' replaced with '{
                    var_data}' in SQL statement")
    return sql_query


def replace_var_names(file_path, sql_query):
    """
    Replaces variable names in SQL statements with corresponding table names found in the source file.

    Args:
        ast_list (list): The AST as a list.
        func (Function): The Function object containing the SQL statement.
        var_name (str): The variable name to be replaced.
    """
    logging.info("Starting variable name replacement")

    var_name = get_var_name(sql_query)

    var_data = find_var_data(file_path, var_name)

    if var_name and var_data:
        sql_query = insert_data_into_var(sql_query, var_data, var_name)
        return sql_query
    if var_name and not var_data:
        logging.warning(f"No table name found for variable: '{var_name}'")
    else:
        logging.info("No variables found to replace.")
    return sql_query


##########################################################################
##########################################################################

if __name__ == "__main__":
    print("analyzer.py")
    # new line for test purpose
