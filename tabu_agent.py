import numpy as np
import random
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
        self._min_solution_cost = 3000
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
        # print("pair: {}   component_a: {}".format(self._neighbour_swapped_components[neighbour_idx], component_a))
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
        # get frequency penalty 
        cost += self._tabu_list.get_frequency_penalty(swapped)
        return cost 

    def mutate_solution(self, position_1, position_2) -> List[int]:
        neighbour = list(self._solution)
        neighbour[position_1] = self._solution[position_2]
        neighbour[position_2] = self._solution[position_1]
        return neighbour

    def generate_neighbours(self):
        self._neighbours = []
        self._neighbour_swapped_components = []
        self._neighbour_values = []
        neighbour_idx = 0
        for i in range(0, len(self._solution)-1):
            for j in range(0,i):
                self._neighbours.append(self.mutate_solution(i, j))
                self._neighbour_swapped_components.append((i,j))
                self._neighbour_values.append(self.calculate_cost(neighbour_idx))
                neighbour_idx += 1

    def select_best_neighbour(self):
        '''
        Rank based on cost value, choose best neighbour solution that is not in the tabu list
        (optional: check aspiration criteria)
        Return best neighbour's index  
        '''
        ranking = sorted(self._neighbour_values)
        # search for first occuring swapped pair that does not occur in the tabu list:
        searching = True
        i = 0
        for val in ranking:
            # find index of next best neighbour to obtain the swapped pair
            neighbour_idx = self._neighbour_values.index(val)
            swapped_pair = self._neighbour_swapped_components[neighbour_idx]
            # check if tabu
            if swapped_pair in self._tabu_list.get_recency_memory() and self._tabu_list.get_recency_memory()[swapped_pair] > 0:
                # Check aspiration criteria
                # Criterion 1: best seen solution
                # if val < self._min_solution_cost:
                #     print("Used aspiration criteria - best overall solution for val {}".format(val))
                #     return neighbour_idx
                # Criterion 2: best solution in the neighbourhood
                # if i == 0:
                #     print("Used aspiration criteria - best solution in neighbourhood {}".format(val))
                #     return neighbour_idx
                pass
            else:
                # print("Swapped pair {} has a cost of of {}".format( swapped_pair, val))
                return neighbour_idx
            i += 1

    def tabu_search(self):
        # algorithm implementation
        iter = 0
        while iter < self._max_iterations:
            self._tabu_list.decrement_tabu()
            self.generate_neighbours()
            best_neighbour_idx = self.select_best_neighbour()
            self._tabu_list.reset_tabu_tenure(self._neighbour_swapped_components[best_neighbour_idx])
            self._solution = self._neighbours[best_neighbour_idx]
            self._flows.set_cost_matrix(self.mutate_cost_map(best_neighbour_idx))
            if self._neighbour_values[best_neighbour_idx] < self._min_solution_cost:
                self._min_solution_cost = self._neighbour_values[best_neighbour_idx]
            iter += 1
            # Update frequency memory
            self._tabu_list.increment_frequency_memory(
                self._neighbour_swapped_components[best_neighbour_idx]
                )

            # change tabu tenure dynamically
            # if iter % 10 == 0:
            #     self._tabu_list.set_tabu_tenure(random.randrange(3,15))
        return self._min_solution_cost


if __name__ == "__main__":
    agent = TabuAgent([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19],10,1000)
    init_cost = np.sum(np.multiply(np.array(agent._flows.get_cost_matrix()), agent._distances))/2.0
    print("initial cost ={}".format(init_cost))
    min_cost = agent.tabu_search()
    print(min_cost)