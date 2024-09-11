"""
time_logging.py
===================
Author: Ardian Gashi

User_Story: https://jira.telekom.de/browse/SDA-7438

Summary:
    This module provides a decorator that logs the execution time of a function.

    The `time_logger` decorator logs the start time, end time, and duration of a
    function's execution to a log file.

Functions:
    1. time_logger(func: str)
        Decorator that logs the execution time of a function.
        Returns:
            callable: The wrapped function with added logging.

"""


import logging
import time


def time_logger(func):
    """
    Decorator that logs the execution time of a function.

    Args:
        func (callable): The function to be decorated.

    Returns:
        callable: The wrapped function with added logging.
    """
    def wrapper(*args, **kwargs):
        """
        Wrapper function that logs the start time, end time, and duration of the function execution.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            The result of the original function execution.
        """
        # Configure the logger
        logging.basicConfig(
            filename="./results.log",
            filemode="w",
            format='%(asctime)s - %(levelname)s: %(message)s',
            level=logging.INFO
        )

        # Log the start of the function
        start_time = time.time()
        logging.info(f"Function {func.__name__!r} has started")

        # Execute the function and store the result
        result = func(*args, **kwargs)

        # Log the end of the function and its duration
        end_time = time.time()
        logging.info(
            f"The function {
                func.__name__!r} took: {
                end_time -
                start_time:.4f} s")

        return result

    return wrapper


if __name__ == "__main__":
    print("time_logging.py")
