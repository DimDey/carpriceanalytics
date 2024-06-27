import csv
import os
from typing import List


class CsvLogger:
    def __init__(self, path, columns: List[str]):
        self.path = path
        self.__columns = columns

        if not os.path.exists(self.path):
            with open(self.path, 'a', newline='', encoding='utf-8') as file:
                w = csv.writer(file)
                w.writerow(self.__columns)

    def save(self, data):
        print(data)
        """Saving data to file."""
        with open(self.path, 'a', newline='', encoding='utf-8') as file:
            row_data = []
            w = csv.writer(file)
            for column in self.__columns:
                value = getattr(data, column, None)
                row_data.append(value)

            w.writerow(row_data)
