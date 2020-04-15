from ortools.algorithms import pywrapknapsack_solver



solver = pywrapknapsack_solver.KnapsackSolver(
    pywrapknapsack_solver.KnapsackSolver.
    KNAPSACK_MULTIDIMENSION_BRANCH_AND_BOUND_SOLVER, 'KnapsackExample')


def KnapsackGG(weights,values,capacities):
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
    return packed_items


if __name__ == '__main__':

    values = [
        360.2, 83.6, 59.5, 130.2, 431.1,

    ]
    weights = [[
        7.4, 0.9, 30.6, 22.3, 80.7,
    ]]
    capacities = [50.6]

    print(KnapsackGG(weights,values,capacities))
