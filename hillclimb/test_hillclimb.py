import logging
import random

import hillclimb as hc
from graphstructure.lectureFichier import *
from tools.enumGraphe import *
from tools.voisinageGraphe import *

log = logging.getLogger(__name__)

def objective_function(i):
    return i


max_evaluations = 500


def test_simple_hillclimb():
    """
    test whether given simple move_operator that just increments the number given
        best == the max number of evaluations
    """

    def move_operator(i):
        yield i + 1

    def init_function():
        return 1

    log.info("-------test_simple_hillclimb()-------")

    num_evaluations, best_score, best = hc.hillclimb(init_function, move_operator, objective_function,
                                                            max_evaluations)

    assert num_evaluations == max_evaluations
    assert best == max_evaluations
    assert best_score == max_evaluations


def test_peak_hillclimb():
    '''
    check we hit the peak value and stop
    '''

    def move_operator(i):
        if i < 100:
            yield i + 1

    def init_function():
        return 1

    log.info("-------test_peak_hillclimb()-------")

    num_evaluations, best_score, best = hc.hillclimb(init_function, move_operator, objective_function,
                                                            max_evaluations)

    assert num_evaluations <= max_evaluations
    assert num_evaluations == 100
    assert best == 100
    assert best_score == 100


def test_file_hillcimb(graph, nbK, max_evaluations):
    def init_function():
        return random.choice(getSoluces(graph.get_nbVertices(), nbK))
        #return [[0,1,2,3,4,5,6,7],[8,9,10,11,12,13,14,15,16,17,18,19]]

    num_evaluations, best_score, best = hc.hillclimb(init_function, pick_gen, graph.get_weight_inter,
                                                     max_evaluations)
    log.info(best)
    log.info(graph.get_weight_inter(best))


def test_file_hillcimb_restart(graph, nbK, max_evaluations):
    def init_function():
        return random.choice(getSoluces(graph.get_nbVertices(), nbK))

    num_evaluations, best_score, best = hc.hillclimb_and_restart(init_function, pick_gen, graph.get_weight_inter,
                                                     max_evaluations)
    log.info(best)
    log.info(graph.get_weight_inter(best))


if __name__ == '__main__':
    import logging
    import sys

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    #test_simple_hillclimb()
    #test_peak_hillclimb()
    reader = Reader('../../fichiersGraphes/vingtSommets.txt')
    reader.readFile()
    test_file_hillcimb(reader.g, 2, 5000)
    #test_file_hillcimb_restart(reader.g, 2, 10000)

