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
        
        # build dictionary for fast cost lookup by a tuple of the objects
        self._cost_dict = {}
        i = 0
        for row in self._cost_matrix:
            #print(row)
            for j in range(0, i):
                self._cost_dict[(i,j)] = row[j]
            i += 1

    def get_cost_dict(self):
        return self._cost_dict

if __name__ == "__main__":
    map = CostMap("data/Flow.csv")
    print(map.get_cost_dict())