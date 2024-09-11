"""
flowchart_generator.py
===================
Author: Ardian Gashi

User_Story: https://jira.telekom.de/browse/SDA-7438

Summary:
	Manages everything, that has to do with the creation of the flowchart:
    - logical connection of the nodes
    - whether to display the columns of each table (default = True)
    - positioning of the nodes
    - configuring the graph's characteristics (e.g. node color, background color)
    - setting the properties of the graph as a picture and saving it


Functions:
    1. draw_graph(original_tables: list[OriginalTable], used_cte: CTE | None,
                    final_table: FinalTable | None, display_columns: bool)

        Draws a directed graph representing the relationships between the tables
        which are used and created in the SQL-query.
        Returns:
            nx.DiGraph: A directed graph representing the table relationships.

    2. assign_levels(graph: nx.DiGraph)
        Assigns a 'level' on the x-axis to nodes in a directed graph based on their connections.

        If, for example, node A and node B connect to node C, then node A and node B are
        both on the same 'level' (on the same x-axis). Node C would be one level higher
        because it chronologically comes after node A and node B.

        Returns:
            list[list[str]]: A list of lists, where each inner list represents a level of nodes.

    3. set_node_pos(levels: list[list[str]])
        Sets the positions of nodes in a graph based on their assigned levels.

        Changes the x-value for each node based on the nodes level number.
        Changes the y-value for each node based on the node count in the nodes level.
        Returns:
            dict[str, Tuple[int, int]]: A dictionary mapping nodes to their positions.

    4. change_node_pos(graph: nx.DiGraph):
        Changes the positions of nodes in a graph to achieve a flowchart form.

        Uses assign_levels() and set_node_pos() to calculate the position of the nodes.
        Returns:
            dict[str, Tuple[int, int]]: A dictionary mapping nodes to their new positions.

    5. set_pseudo_nodes(graph: nx.DiGraph, pos: dict[str, Tuple[int, int]]):
        Adds invisible pseudo nodes to the graph and updates their positions to form
        a bounding box around the existing nodes.
        This is needed to save the graph as a picture correctly.
        Returns:
            dict[str, Tuple[int, int]]: Updated positions including the pseudo nodes.

    6. show_graph(graph: nx.DiGraph, pos: dict[str, Tuple[int, int]], counter: int):
        Creates and saves a graphical representation of the graph.
        Returns:
            None

"""
import logging
import matplotlib.pyplot as plt
import networkx as nx
from time_logging import time_logger


#### ----------------------------------------------------------------------------------####

@time_logger
def draw_graph(original_tables, used_cte, final_table, display_columns=True):
    """
    Draws a directed graph representing the relationships between the tables
    wich are used and created in the SQL-query.

    Args:
        original_tables (list): A list of original table objects.
        used_cte (list): A list containing a single CTE object.
        final_table (list): A list containing a single final table object.

    Returns:
        nx.DiGraph: A directed graph representing the table relationships.
    """
    graph = nx.DiGraph()

    colon = ""

    if display_columns:
        colon = ":"

    # Add final table and CTE nodes and edge
    if final_table and used_cte:
        final_table_label = f"{
            final_table.name}{colon} \n\n{
            final_table.columns}"
        graph.add_node(final_table_label)

        used_cte = used_cte[0]
        used_cte_label = f"{used_cte.name}{colon} \n\n{used_cte.columns}"
        graph.add_node(used_cte_label)

        graph.add_edge(used_cte_label, final_table_label)

    elif final_table and not used_cte:
        final_table_label = f"{
            final_table.name}{colon} \n\n{
            final_table.columns}"
        graph.add_node(final_table_label)

    # Add original table nodes and edges
    for original_table in original_tables:
        original_table_label = f"{
            original_table.name}{colon} \n\n{
            original_table.columns}"
        graph.add_node(original_table_label)
        if final_table and used_cte:
            graph.add_edge(original_table_label, used_cte_label)
        elif final_table and not used_cte:
            graph.add_edge(original_table_label, final_table)

    logging.info("Graph created successfully.")

    return graph


@time_logger
def assign_levels(graph):
    """
    Assigns a 'level' on the x-axis to nodes in a directed graph based on their connections.

    Args:
        graph (nx.DiGraph): A directed graph representing table relationships.

    Returns:
        list: A list of lists, where each inner list represents a level of nodes.
    """
    levels = []
    adjdict = graph.adj
    adjdict_copy = adjdict.copy()

    for key in adjdict:
        key_exists = any(key in level for level in levels)

        if not key_exists:
            node_list = [key]
            adjdict_copy.pop(key, None)

            for second_key in list(adjdict_copy.keys()):
                if adjdict[key] == adjdict_copy[second_key]:
                    node_list.append(second_key)

            levels.append(node_list)

    levels.reverse()

    logging.info("Levels assigned successfully.")
    return levels


@time_logger
def set_node_pos(levels):
    """
    Sets the positions of nodes in a graph based on their assigned levels.

    Args:
        levels (list): A list of lists, where each inner list represents a level of nodes.

    Returns:
        dict: A dictionary mapping nodes to their positions.
    """
    pos_dict = {}

    for level_number, level in enumerate(levels):
        level_size = len(level)

        if level_size % 2 == 1:
            # Odd number of nodes
            first_node_pos = 0
            pos_dict[level[0]] = (level_number, first_node_pos)
            for i, node in enumerate(level[1:], start=1):
                if i % 2 == 0:
                    pos_dict[node] = (level_number, first_node_pos + i // 2)
                else:
                    pos_dict[node] = (
                        level_number, first_node_pos - (i + 1) // 2)
        else:
            # Even number of nodes
            first_node_pos = 0.5
            second_node_pos = -0.5
            pos_dict[level[0]] = (level_number, first_node_pos)
            pos_dict[level[1]] = (level_number, second_node_pos)
            for i, node in enumerate(level[2:], start=1):
                if i % 2 == 0:
                    pos_dict[node] = (level_number, first_node_pos + i // 2)
                else:
                    pos_dict[node] = (
                        level_number, second_node_pos - (i + 1) // 2)

    logging.info("Node positions calculated successfully.")
    return pos_dict


def change_node_pos(graph):
    """
    Changes the positions of nodes in a graph based on their levels.

    Args:
        graph (nx.DiGraph): A directed graph representing table relationships.

    Returns:
        dict: A dictionary mapping nodes to their new positions.
    """
    levels = assign_levels(graph)
    pos = set_node_pos(levels)

    logging.info("Node positions changed successfully.")
    return pos


@time_logger
def set_pseudo_nodes(graph, pos):
    """
    Adds pseudo nodes to the graph and updates their positions to form
    a bounding box around the existing nodes.
    This is needed to save the graph as a picture correctly.

    Args:
        graph (nx.Graph): The graph to which pseudo nodes will be added.
        pos (dict): A dictionary mapping nodes to their positions.

    Returns:
        dict: Updated positions including the pseudo nodes.
    """
    # Add pseudo nodes to the graph
    pseudo_nodes = [" ", "  ", "   ", "    "]
    graph.add_nodes_from(pseudo_nodes)

    def find_max_and_min_values(pos):
        """
        Finds the maximum and minimum x and y values in the positions dictionary.

        Args:
            pos (dict): A dictionary mapping nodes to their positions.

        Returns:
            dict: Updated positions including the pseudo nodes.
        """
        max_x = max(pos.values(), key=lambda p: p[0])[0]
        max_y = max(pos.values(), key=lambda p: p[1])[1]
        min_x = min(pos.values(), key=lambda p: p[0])[0]
        min_y = min(pos.values(), key=lambda p: p[1])[1]

        padding = 0.5
        upper_left_corner = (min_x - padding, max_y + padding)
        upper_right_corner = (max_x + padding, max_y + padding)
        lower_left_corner = (min_x - padding, min_y - padding)
        lower_right_corner = (max_x + padding, min_y - padding)

        pos[" "] = upper_left_corner
        pos["  "] = upper_right_corner
        pos["   "] = lower_left_corner
        pos["    "] = lower_right_corner

        return pos

    # Update positions with pseudo nodes
    pos = find_max_and_min_values(pos)

    logging.info("Pseudo nodes set successfully.")
    return pos


@time_logger
def show_graph(graph, pos, counter):
    """
    Creates and saves a graphical representation of the graph.

    Args:
        G (networkx.DiGraph): The directed graph created by NetworkX.
        pos (dict): Contains the position of each node of the graph.
        counter (int): A counter for naming the saved graph image.
    """
    # Node properties
    base_size = 25
    node_size = [
        len(node_label) *
        base_size ** 2 /
        2.5 for node_label in graph.nodes()]
    node_color = "none"
    node_shape = 'o'
    # For debugging:
    # alpha = 0

    # Label properties
    font_size = 7
    font_color = "k"
    with_labels = True
    # For debugging:
    # bbox = {"alpha": 0.1, "color": "blue"}

    # Figure size
    width = len(graph.nodes()) * 2
    height = len(graph.nodes()) * 2
    plt.figure(figsize=(width, height))

    # Draw graph on figure
    nx.draw(
        graph,
        pos,
        node_size=node_size,
        node_color=node_color,
        node_shape=node_shape,
        with_labels=with_labels,
        font_size=font_size,
        font_color=font_color
    )

    # Show the graph as a matlotlib window:
    # fig_manager = plt.get_current_fig_manager()
    # fig_manager.window.showMaximized()
    # plt.show()  # Uncomment this line if you want to display the graph

    plt.savefig(
        f"graphs/Graph{counter}.png",
        bbox_inches="tight",
        dpi=150,
        transparent=False)
    logging.info(f"Graph successfully saved as: 'Graph{counter}.png'")


if __name__ == "__main__":
    print("flowchart_generator.py")
