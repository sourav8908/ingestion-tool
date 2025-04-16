import csv
from typing import List

def read_from_csv(file_path: str) -> List[List[str]]:
    """Reads data from a CSV file and returns a list of rows."""
    data = []
    try:
        with open(file_path, mode='r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                data.append(row)
    except Exception as e:
        raise RuntimeError(f"Failed to read file {file_path}: {str(e)}")
    return data

def write_to_csv(file_path: str, data: List[List[str]], delimiter: str = ','):
    """Writes a list of rows to a CSV file."""
    try:
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file, delimiter=delimiter)
            writer.writerows(data)
    except Exception as e:
        raise RuntimeError(f"Failed to write to file {file_path}: {str(e)}")
