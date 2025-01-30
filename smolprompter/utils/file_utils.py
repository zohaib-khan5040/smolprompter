import pandas as pd
import os


def read_csv(file_path: str) -> pd.DataFrame:
    """
    Reads a CSV file and returns a pandas DataFrame.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        pd.DataFrame: DataFrame containing the contents of the CSV file.
    """
    assert os.path.exists(file_path), f"File not found: {file_path}"
    return pd.read_csv(file_path)


def write_to_csv(file_path: str, data_frame: pd.DataFrame):
    """
    Writes a pandas DataFrame to a CSV file.

    Args:
        file_path (str): Path to the CSV file.
        data_frame (pd.DataFrame): DataFrame to be written to the CSV file.
    """
    data_frame.to_csv(file_path, index=False)


def read_txt(file_path: str) -> list:
    """
    Reads a text file and returns the lines as a list of strings.

    Args:
        file_path (str): Path to the text file.

    Returns:
        list: List of strings representing the lines in the text file.
    """
    assert os.path.exists(file_path), f"File not found: {file_path}"
    with open(file_path, 'r') as file:
        return file.readlines()


def write_to_txt(file_path: str, lines: list):
    """
    Writes a list of strings to a text file.

    Args:
        file_path (str): Path to the text file.
        lines (list): List of strings to be written to the text file.
    """
    with open(file_path, 'w') as file:
        file.writelines(lines)


def append_to_txt(file_path: str, lines: list):
    """
    Appends a list of strings to an existing text file.

    Args:
        file_path (str): Path to the text file.
        lines (list): List of strings to be appended to the text file.
    """
    with open(file_path, 'a') as file:
        file.writelines(lines)
