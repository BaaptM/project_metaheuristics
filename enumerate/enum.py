import logging
from tools import enumGraphe

log = logging.getLogger(__name__)


def get_best_sol_enumeration(graph, objective_function, nbK, delta_max, mu):
    # function to partition with the less interclasses weight by enumeration
    # @param graph the graph to be partitioned
    # @param nbK number of classes
    # @param delta max difference between classes % of vertex in the graph
    # @return the best solution

    # get all solutions
    potential_sols = enumGraphe.validate_solution(enumGraphe.getSoluces(graph.get_nbVertices(), nbK), delta_max)

    # init current_sol at the first
    current_sol = []
    # current_sol = first of potential_sols
    if(len(potential_sols) > 0):
        current_sol.append(potential_sols[0])
        current_weight = objective_function(current_sol[0], mu)

    # evaluate all sol
    if(len(current_sol) == 0):
        log.debug('no possible solutions with this delta')
    else:
        for sol in potential_sols:  # enum all valid sol
            actual_weight = objective_function(sol, mu)
            if actual_weight < current_weight:
                del current_sol[:]
                current_sol.append(sol)
                current_weight = actual_weight
            elif actual_weight == current_weight:
                contain = True  #check if the sol is already in current_sol in another classes position
                for classe in sol:
                    for csol in current_sol:
                        contain = classe in csol
                if not contain:
                    current_sol.append(sol)
        log.debug('minimum weight interclass for %s Classes is %s' % (nbK, current_weight))
    return current_weight, current_sol






