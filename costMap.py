# Mathew Romlewski November 2020
import csv

class CostMap:

    def __init__(self, file_path):

        self._cost_matrix = []
        with open(file_path) as csvfile:
            reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC) # change contents to floats
            for row in reader: # each row is a list
                self._cost_matrix.append(row)
        print(self._cost_matrix)

if __name__ == "__main__":
    map = CostMap("data/Flow.csv")