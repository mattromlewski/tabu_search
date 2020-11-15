

class TabuAgent:
    '''
    Wrapper for current solution and neighbouring solutions. 
    '''
    def __init__(self, initial_solution, tabu_tenure, max_iterations):
        self._solution = initial_solution
        self._neighbours = []   
        self._tabu_tenure = tabu_tenure
        self._max_iterations = max_iterations
        self._best_solution_value = 0

    def mutate_solution(current_solution, position_1, position_2):
        

    def generate_neighbours(self):

