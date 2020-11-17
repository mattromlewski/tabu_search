# Mathew Romlewski November 2020
import csv

class CostMap:
    '''
    Wrapper for CSV data which encodes the QAP flows and distances
    Main goal - provide fast cost lookup given a pair of objects or sites
    '''
    def __init__(self, file_path):

        # build matrix from CSV
        self._cost_matrix = []
        with open(file_path) as csvfile:
            reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC) # change contents to floats
            for row in reader: # each row is a list
                self._cost_matrix.append(row)

    def get_cost_matrix(self):
        return self._cost_matrix

    

if __name__ == "__main__":
    map = CostMap("data/Flow.csv")
    print(map.get_cost_dict())