import logging
import sys
import os
DOSSIER_COURRANT = os.path.dirname(os.path.abspath(__file__))
DOSSIER_PARENT = os.path.dirname(DOSSIER_COURRANT)
sys.path.append(DOSSIER_PARENT)
from graphstructure import graphDataStructure as gs
from graphstructure import lectureFichier as lf

from tools.enumGraphe import *

log = logging.getLogger(__name__)


def get_best_sol_enumeration(graph, objective_function, nbK, delta_max):
    # function to partition with the less interclasses weight by enumeration
    # @param graph the graph to be partitioned
    # @param nbK number of classes
    # @param delta max difference between classes % of vertex in the graph
    # @return the best solution

    # get all solutions
    potential_sols = validate_solution(getSoluces(graph.get_nbVertices(), nbK), delta_max)

    # init current_sol at the first
    current_sol = []
    # current_sol = first of potential_sols
    if(len(potential_sols) > 0):
        current_sol.append(potential_sols[0])
        current_weight = objective_function(current_sol[0])

    # evaluate all sol
    if(len(current_sol) == 0):
        log.info('no possible solutions with this delta')
    else:
        for sol in potential_sols:  # enum all valid sol
            actual_weight = objective_function(sol)
            if actual_weight < current_weight:
                del current_sol[:]
                current_sol.append(sol)
                current_weight = actual_weight
            elif actual_weight == current_weight:
                contain = True
                for classe in sol:
                    for csol in current_sol:
                        contain = classe in csol
                if not contain:
                    current_sol.append(sol)
        print('minimum weight interclass for %s Classes is %s' % (nbK, current_weight))
    return current_sol


def get_max_delta(sol):
    max_delta = 0
    for classe1 in sol:
        for classe2 in sol:
            delta = abs(len(classe1) - len(classe2))
            if max_delta < delta:
                max_delta = delta
    return max_delta


def validate_solution(solutions, delta):
    valid_sol = []
    for sol in solutions:
        if get_max_delta(sol) < delta:
            valid_sol.append(sol)
    return valid_sol

if __name__ == '__main__':
###### TEST ######

    import logging
    import sys

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    graph = gs.Graph()

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
    #print(get_best_sol_enumeration(graph,graph.get_weight_inter,2 ,0))

    reader = lf.Reader('../fichiersGraphes/dixSommets.txt')
    reader.readFile()
    import timeit

    start = timeit.default_timer()

    print(get_best_sol_enumeration(reader.g, reader.g.get_weight_inter, 2, 2))

    stop = timeit.default_timer()

    print(stop - start)




