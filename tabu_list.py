class TabuList:
    '''
    Memory object for tabu search.
    Recency memory to avoid permutations with pairs of components 
    used recently.

    Frequency memory to penalize permutations with the pairs 
    of components used frequently.
    '''

    def __init__(self, tabu_tenure):
        self._recency_mem = {}
        self._frequency_mem = {}
        self._tabu_tenure = tabu_tenure

    def reset_tabu_tenure(self, chosen_solution):
        self._recency_mem[chosen_solution] = self._tabu_tenure

    def decrement_tabu(self):
        for key, val in self._recency_mem.items():
            if self._recency_mem[key] > 0:
                self._recency_mem[key] = val-1
    
    def get_recency_memory(self):
        return dict(self._recency_mem)

if __name__ == "__main__":
    # test
    tabu = TabuList(5)
    tabu.reset_tabu_tenure((5,4))
    print(tabu.get_recency_memory())
    tabu.decrement_tabu()
    print(tabu.get_recency_memory())
    tabu.decrement_tabu()
    tabu.reset_tabu_tenure((5,3))
    print(tabu.get_recency_memory())
    tabu.decrement_tabu()
    print(tabu.get_recency_memory())