from ortools.algorithms import pywrapknapsack_solver



def knapsackGG(weights,values,capacities):
    #************************************************************************
    # Purpose: using Knapsack from google ortool to select shot
    # Inputs:
    # - weights: a list of duration of shots
    # - values: a list of shot score
    # - capacities: the duration that you want to summary
    # Output: a list of index of selected shot
    # Author: Dungmn
    #************************************************************************
    solver = pywrapknapsack_solver.KnapsackSolver(
        pywrapknapsack_solver.KnapsackSolver.
        KNAPSACK_MULTIDIMENSION_BRANCH_AND_BOUND_SOLVER, 'KnapsackExample')
    solver.Init(values, weights, capacities)
    computed_value = solver.Solve()
    packed_items = []
    packed_weights = []
    total_weight = 0

    for i in range(len(values)):
        if solver.BestSolutionContains(i):
            packed_items.append(i)
            packed_weights.append(weights[0][i])
            total_weight += weights[0][i]
    return total_weight,packed_items


if __name__ == '__main__':

    values = [2.1, 2.4, 2.05, 2.05, 2.25, 2.35, 1.65, 1.75, 1.55, 1.75, 3.15, 2.1, 1.95, 2.1, 2.35, 3.3, 1.25, 1.1, 1.15, 1.1, 1.9, 2.15, 1.95, 1.8, 2.1, 2.1, 2.2, 2.1, 2.85, 2.85, 1.85, 1.05,
    1.2, 2.35, 2.5, 2.95, 2.45, 2.5, 2.5, 2.75, 2.5, 2.65, 2.55, 2.45, 1.7, 1.7, 1.5, 1.5, 1.75, 1.65, 1.75, 1.75, 2.8, 2.15, 2.25, 2.05, 1.95, 1.9, 2.15, 2.45, 2.6, 3.65, 3.65, 3.6, 2.0, 1.9, 2.1, 1.95, 2.0,
    2.1, 2.3, 2.25, 1.05, 1.05, 1.0, 1.1, 1.1, 1.1, 1.05, 2.35, 2.2, 2.2, 2.6, 2.5, 2.5, 2.3, 2.5, 1.75, 1.1, 1.15, 1.2, 1.9, 1.95, 1.9, 2.0, 1.45, 1.1, 1.1, 1.15, 1.15, 1.15, 1.1, 1.1, 2.4, 2.25, 1.95, 2.0, 2.0,
    2.05, 2.0, 2.25, 2.55, 2.3, 2.45, 2.05, 2.05, 2.05]
    weights = [[2.0022, 2.0021, 2.0022, 2.0021, 2.0022, 2.0021, 2.0022, 2.0021, 2.0022, 2.0021, 2.0022, 2.0021, 2.0022, 2.0021, 2.0022, 2.0021,
2.0022, 2.0021, 2.0022, 2.0021, 2.0022, 2.0021, 2.0022, 2.0021, 2.0022, 2.0021, 2.0022, 2.0021, 2.0022, 2.0021, 2.0022, 2.0021, 2.0022, 2.0021, 2.0022, 2.0021, 2.0022, 2.0021, 2.0022, 2.0021, 2.0022, 2.0022, 2.0021, 2.0022, 2.0021, 2.0022, 2.0021, 2.0022,
2.0021, 2.0022, 2.0021, 2.0022, 2.0021, 2.0022, 2.0021, 2.0022, 2.0021, 2.0022, 2.0021, 2.0022, 2.0021, 2.0022, 2.0021, 2.0022, 2.0021, 2.0022, 2.0021, 2.0022, 2.0021, 2.0022, 2.0021, 2.0022, 2.0021, 2.0022, 2.0021, 2.0022, 2.0021, 2.0022, 2.0021, 2.0022,
2.0021, 2.0022, 2.0022, 2.0021, 2.0022, 2.0021, 2.0022, 2.0021, 2.0022, 2.0021, 2.0022, 2.0021, 2.0022, 2.0021, 2.0022, 2.0021, 2.0022, 2.0021, 2.0022, 2.0021, 2.0022, 2.0021, 2.0022, 2.0021, 2.0022, 2.0021, 2.0022, 2.0021, 2.0022, 2.0021, 2.0022, 2.0021,
2.0022, 2.0021, 2.0022, 2.0021, 1.6685]]
    capacities = [30.0901]

    print(knapsackGG(weights,values,capacities))
