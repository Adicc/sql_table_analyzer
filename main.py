"""
main.py
===================
Author: Ardian Gashi

User_Story: https://jira.telekom.de/browse/SDA-7438

Summary:
	Starts the programm.
    Configures the parameters at an upper level.


Functions:
	None

"""
import logging

import analyzer
import cte_manager
import final_table_manager
import flowchart_generator as fg
import original_table_manager


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
    # FILE = r"source_scripts\calculate_mtbf.py"
    # FILE = r"source_scripts\count_affected_customers_bng.py"
    # FILE = r"source_scripts\count_affected_customers.py"
    # FILE = r"source_scripts\count_assigned_customers.py"
    FILE = r"source_scripts\get_power_outages.py"

    # extract the sql_query from a multiline_string
    sql_queries = analyzer.extract_sql_queries(FILE)
    # Turn the sql_query-string into a list
    sql_queries = [sql_query.split('\n') for sql_query in sql_queries]

    # replace the variables with the coresponding data
    sql_queries = [analyzer.replace_var_names(FILE, sql_query)
                   for sql_query in sql_queries]

    # Create the Graph:
    graphs = {}

    for sql_query in sql_queries:

        sql = sql_query

        CTEs = cte_manager.get_ctes(sql, DISPLAY_COLUMNS)
        if CTEs:
            USED_CTE = [CTEs[-1]]
        else:
            USED_CTE = None

        final_table = final_table_manager.get_final_table(
            sql, DISPLAY_COLUMNS)
        if final_table:
            original_tables = original_table_manager.get_original_tables(
                sql, final_table, DISPLAY_COLUMNS)
        else:
            original_tables = original_table_manager.get_original_tables(
                sql, None, DISPLAY_COLUMNS)

        G = fg.draw_graph(
            original_tables,
            USED_CTE,
            final_table,
            DISPLAY_COLUMNS)

        pos = fg.change_node_pos(G)

        pos = fg.set_pseudo_nodes(G, pos)

        graphs[G] = pos

    # Show the Graphs
    COUNTER = 1
    for G in graphs.keys():
        fg.show_graph(G, graphs[G], COUNTER)

        COUNTER += 1

    logging.info("The program has ended.")
    print("The program has ended.")
