

 # SQL Flowchart Generator
 
### _Create a visualistaion of your SQL-Queries_

> With this flowchart generator you can visualize the relations of your
tables in the SQL-Queries of your python scripts.


## Table of Contents
- [Installation and Usage](#installation-and-usage)
	- [Dependencies](#dependencies)
	- [Usage](#usage)
- [File Descriptions](#file-descriptions)
  - [analyzer.py](#analyzerpy)
  - [cleaner.py](#cleanerpy)
  - [cte_manager.py](#cte-managerpy)
  - [final_table_manager.py](#final-table-managerpy)
  - [flowchart_generator.py](#flowchart-generatorpy)
  - [main.py](#mainpy)
  - [time_logging.py](#time-loggingpy)
  - [original_table_manager.py](#original-table-managerpy)
- [Features](#features)
- [Creators](#creators)
- [License](#license)

## Installation and Usage

### Dependencies

#### Python version:

- Python 3.11.8

Run this in your terminal to install the necessary libraries:

> python3 -m pip install -r [requirements.txt](requirements.txt)

### Usage

To use the programm you'll have to:

1. Open the [main.py](#mainpy) file.

3. **Change** the string of the `FILE` variable to the **path** of your file

	- remember to use the **raw** string format:

		> FILE = **r**"C:your\file\path\here"

4. Run [main.py](#mainpy).

5. Your graph(s) will be saved in the `graphs` folder.

## File Descriptions

#### [analyzer.py](analyzer.py)

_This module provides functionality to extract SQL queries from a file and identify and replace variable names within these queries._

#### [cleaner.py](cleaner.py)

_This module provides functionality to clean and format columns of a table object.
The primary function in this module, `clean_columns`, modifies the column format to ensure it is clean and readable._

#### [cte_manager.py](cte_manager.py)

_This module provides functionality to detect and process Common Table Expressions (CTEs) in SQL queries.
It includes functions to check for the presence of CTEs and extract their names and columns._

#### [final_table_manager.py](final_table_manager.py)

Finds the table in wich all data gets inserted into.
Creates an instance of the FinalTable class
wich stores the relevant data of the table of the SQL-query
in which the data gets inserted into

#### [flowchart_generator.py](flowchart_generator.py)

Manages everything, that has to do with the creation of the flowchart:

- logical connection of the nodes
- whether to display the columns of each table (default = True)
- positioning of the nodes
- configuring the graph's characteristics (e.g. node color, background color)
	- `base_size`: is used to calculate the necassary node size (change this for an easy way to manipulate the node size)
	- `node_size`: uses `base_size` to calculate the nessacary node size (change the values for a more complex manipulation of the node size)
- setting the properties of the graph as a picture and saving it
for the remaining parameters I used the variable names networkx also used:
	> `node_color`, `node_shape`, `with_labels`, `font_size`, `font_color`

For further information on what you can change the parameters to, check out the `networkx` documentation:
https://networkx.org/documentation/stable/reference/generated/networkx.drawing.nx_pylab.draw_networkx.html

#### [main.py](main.py)

_Running this file will start the program.
Here you can pass the path to your python file and decide if you want to display the columns of the table._

#### [time_logging.py](time_logging.py)

_This module provides a decorator for logging the execution time of functions._

#### [original_table_manager.py](original_table_manager.py)

_Finds the table from wich all data gets extracted from.
Creates an instance of the OriginalTable class wich stores the relevant data of the source table in the SQL-query._

## Features

1. Create a .png file which shows the relation of the used tables in the used SQL-Querys

2. Deactivate/ activate the display of the column names

	- **Change** the `DISPLAY_COLUMNS` variable to `False` **if you dont want to include the column names** in your result picture:

		> DISPLAY_COLUMNS = **False**
		- To reactivate the column names, change the value back to `True`:
		> DISPLAY_COLUMNS = **True**

3. Modify the display settings

    - for this you'll have to change the code of the `show_graph` function in [flowchart_generator.py](#flowchart-generatorpy)

## Creators
Ardian Gashi
- ardian.gashi@telekom.de
- https://yam-united.telekom.com/pages/predictive-maintenance-daa/apps/content/startseite

## License

This project is licensed under the MIT License with an additional clause restricting commercial use - see the [LICENSE](LICENSE.md) file for details.

