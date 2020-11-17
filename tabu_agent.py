from typing import List

from cost_map import CostMap

class TabuAgent:
    '''
    Wrapper for current solution and neighbouring solutions. 
    '''
    def __init__(self, initial_solution, tabu_tenure, max_iterations):
        self._solution = initial_solution
        self._neighbours = []   
        self._neighbour_values = []
        self._neighbour_swapped_components = []
        self._tabu_tenure = tabu_tenure
        self._max_iterations = max_iterations
        self._best_solution_value = 0
        
        self._flows = CostMap("data/Flow.csv")
        self._distances = CostMap("data/Distance.csv")

    def calculate_cost

    def mutate_solution(self, position_1, position_2) -> List[int]:
        neighbour = list(self._solution)
        neighbour[position_1] = self._solution[position_2]
        neighbour[position_2] = self._solution[position_1]
        return neighbour

    def generate_neighbours(self):
        self._neighbours = []
        for i in range(0, len(self._solution)-1):
            for j in range(i+1):
                self._neighbours.append(self.mutate_solution(i, j))


