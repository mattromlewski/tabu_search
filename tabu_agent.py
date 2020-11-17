import numpy as np
from typing import List

from cost_map import CostMap
from tabu_list import TabuList

class TabuAgent:
    '''
    Wrapper for current solution and neighbouring solutions. 
    '''
    def __init__(self, initial_solution, tabu_tenure, max_iterations):
        self._solution = initial_solution
        self._neighbours = []   
        self._neighbour_values = []
        self._neighbour_swapped_components = []
        self._tabu_list = TabuList(tabu_tenure)
        self._max_iterations = max_iterations
        self._best_solution_value = 0
        self._flows = CostMap("data/Flow.csv")
        self._distances = np.array(CostMap("data/Distance.csv").get_cost_matrix())

    def mutate_cost_map(self, neighbour_idx):
        '''
        Copies the current cost map, swaps two rows and two colums, and returns the modified array
        Useful for both creating temporary flow matrices and for updating the master flow matrix
        '''
        mut_cost_map = [row[:] for row in self._flows.get_cost_matrix()]
        # need to determine which row each of the swapped components occupy in the solution matrix
        component_a, component_b = self._neighbour_swapped_components[neighbour_idx]
        print("pair: {}   component_a: {}".format(self._neighbour_swapped_components[neighbour_idx], component_a))
        component_a_idx = self._solution.index(component_a)  # This is the cost row and column occupied by component_a
        component_b_idx = self._solution.index(component_b)
        # Need to swap rows at the two indices above
        temp = mut_cost_map[component_a_idx]
        mut_cost_map[component_a_idx] = mut_cost_map[component_b_idx]
        mut_cost_map[component_b_idx] = temp
        # Now columns
        for i in range(0, len(mut_cost_map)):
            temp = mut_cost_map[i][component_a_idx]
            mut_cost_map[i][component_a_idx] = mut_cost_map[i][component_b_idx]
            mut_cost_map[i][component_b_idx] = temp
        return mut_cost_map

    def calculate_cost(self, neighbour_idx):
        swapped = self._neighbour_swapped_components[neighbour_idx]
        neighbour_cost_map = np.array(self.mutate_cost_map(neighbour_idx))
        cost = np.sum(np.multiply(neighbour_cost_map, self._distances))/2.0
        return cost

    def mutate_solution(self, position_1, position_2) -> List[int]:
        neighbour = list(self._solution)
        neighbour[position_1] = self._solution[position_2]
        neighbour[position_2] = self._solution[position_1]
        return neighbour

    def generate_neighbours(self):
        self._neighbours = []
        solution_idx = 0
        for i in range(0, len(self._solution)-1):
            for j in range(0,i):
                self._neighbours.append(self.mutate_solution(i, j))
                self._neighbour_swapped_components.append((i,j))
                self._neighbour_values.append(self.calculate_cost(solution_idx))
                solution_idx += 1

    def select_best_neighbour(self):
        '''
        Rank based on cost value, choose best neighbour solution that is not in the tabu list
        Return best neighbour's index  
        '''
        print(self._neighbour_values)
        ranking = sorted(self._neighbour_values)
        # search for first occuring swapped pair that does not occur in the tabu list:
        searching = True
        for val in ranking:
            # find index of next best neighbour to obtain the swapped pair
            neighbour_idx = self._neighbour_values.index(val)
            swapped_pair = self._neighbour_swapped_components[neighbour_idx]
            # check if tabu
            if swapped_pair in self._tabu_list.get_recency_memory():
                print("Swapped pair {} has a tabu value of {}".format(
                    swapped_pair, self._tabu_list.get_recency_memory()[swapped_pair]
                ))
            else:
                return neighbour_idx

    

if __name__ == "__main__":
    agent = TabuAgent([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19],10,1000)
    init_cost = np.sum(np.multiply(np.array(agent._flows.get_cost_matrix()), agent._distances))/2.0
    print("initial cost ={}".format(init_cost))
    agent.generate_neighbours()
    best_idx = agent.select_best_neighbour()
    print("Best neighbour index: {} cost: {}".format(best_idx,agent._neighbour_values[best_idx]))