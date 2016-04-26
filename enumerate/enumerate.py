from graphDataStructure import *
from tools.enumGraphe import *


def get_best_sol_enumeration(graph, objective_function, nbK, delta):
    # function to partition with the less interclasses weight by enumeration
    # @param graph the graph to be partitioned
    # @param nbK number of classes
    # @param delta max difference between classes % of vertex in the graph
    # @return the best solution

    # get all solutions
    potentiel_sols = getSoluces(graph.get_nbVertices(), nbK)

    # init current_sol at the first
    current_sol = []
    # current_sol = potentiel_sols
    current_sol.append(potentiel_sols[0])
    current_weight = objective_function(current_sol[0])

    # evaluate all sol
    for sol in potentiel_sols[1:]:  # enum all valid sol
        actual_weight = objective_function(sol)
        if actual_weight < current_weight:
            current_sol.clear()
            current_sol.append(sol)
            current_weight = actual_weight
        elif actual_weight == current_weight:
            current_sol.append(sol)
    print('minimum weight interclass for %s Classes is %s' % (nbK, current_weight))
    return current_sol

if __name__ == '__main__':
###### TEST ######
    graph = Graph()

    graph.add_vertex('a')
    graph.add_vertex('b')
    graph.add_vertex('c')
    graph.add_vertex('d')
    graph.add_vertex('e')
    graph.add_vertex('f')

    graph.add_edge('a', 'b', 1)
    graph.add_edge('a', 'c', 2)
    graph.add_edge('a', 'e', 3)
    graph.add_edge('b', 'f', 4)
    graph.add_edge('b', 'd', 5)
    graph.add_edge('c', 'd', 4)
    graph.add_edge('c', 'b', 3)
    graph.add_edge('d', 'e', 2)
    graph.add_edge('e', 'f', 1)

    #### ENUM WITH get_sol FUNCTION ####
    print(get_best_sol_enumeration(graph,graph.get_weight_inter,3 ,10))


