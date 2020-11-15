class TabuList:
    '''
    Memory object for tabu search.
    Recency memory to avoid permutations with pairs of components 
    used recently.

    Frequency memory to penalize permutations with the pairs 
    of components used frequently.
    '''

    def __init__(self):
        self._recency_mem = {}
        self._frequency_mem = {}
