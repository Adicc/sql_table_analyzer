import logging

import analyzer
# import cte_manager
# import final_table_manager
# import flowchart_generator as fg
# import original_table_manager


if __name__ == "__main__":

    print("The program has started.")

    logging.basicConfig(
        filename="./results.log",
        filemode="w",
        format='%(asctime)s - %(levelname)s: %(message)s',
        level=logging.INFO)

    logging.info("The program has started.")

    DISPLAY_COLUMNS = True

    # Insert your file path here:
    FILE = r"source_scripts\test_file.py"

    # extract the sql_query from a multiline_string
    sql_queries = analyzer.extract_sql_queries(FILE)
    # Turn the sql_query-string into a list
    sql_queries = [sql_query.split('\n') for sql_query in sql_queries]

    # replace the variables with the coresponding data
    sql_queries = [analyzer.replace_var_names(FILE, sql_query)
                   for sql_query in sql_queries]
    

    print(sql_queries)