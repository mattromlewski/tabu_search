from tabu_agent import TabuAgent

if __name__ == "__main__":
    initial_solutions = [
        [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19],
        [0,1,2,3,4,5,16,7,8,19,10,11,12,13,14,15,6,17,18,9],
        [0,1,4,3,2,5,16,7,8,19,10,11,12,13,14,15,6,17,18,9],
        [5,1,2,3,4,0,16,7,8,19,10,11,12,13,14,15,6,17,18,9],
        [14,1,2,3,4,5,16,7,8,19,10,11,12,13,0,15,6,17,18,9],
        [0,1,2,3,4,12,16,7,8,19,10,11,5,13,14,15,6,17,18,9],
        [18,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,0,19],
        [0,11,2,13,4,5,6,7,8,9,10,1,12,3,14,15,16,17,18,19],
        [0,1,2,3,14,5,6,7,8,9,10,11,12,13,4,15,16,17,18,19],
        [0,1,2,13,4,5,6,17,8,9,10,11,12,3,14,15,16,7,18,19],
        [0,1,2,3,4,5,16,7,8,19,10,11,12,13,14,15,6,17,18,9]
    ]
    first_run = True
    min_costs = []
    overall_min = None
    for initial_solution in initial_solutions:
        agent = TabuAgent(initial_solution,10,1000)
        min_cost = agent.tabu_search()
        print(min_cost)
        if not first_run:
            if min_cost < min_min:
                min_min = min_cost
        else:
            min_min = min_cost
            first_run = False
        min_costs.append(min_cost)

    print("Best solution from each run {}".format(min_costs))
    print("Best solution out of all runs {}".format(min_min))