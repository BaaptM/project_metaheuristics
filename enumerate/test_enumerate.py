import logging
import sys
import os

import enumerate as enum
from graphstructure import graphDataStructure as gs
from graphstructure import lectureFichier as lf
from tools.enumGraphe import *

DOSSIER_COURRANT = os.path.dirname(os.path.abspath(__file__))
DOSSIER_PARENT = os.path.dirname(DOSSIER_COURRANT)
sys.path.append(DOSSIER_PARENT)
log = logging.getLogger(__name__)

reader = lf.Reader('../fichiersGraphes/dixSommets.txt')
reader.readFile()


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
    #sol = random.choice(getSoluces(reader.g.get_nbVertices(), 3))
    #print(sol, get_max_delta(sol))



    import timeit
    nbK = 3
    delta_max = 3
    start = timeit.default_timer()
    sol = enum.get_best_sol_enumeration(reader.g, reader.g.get_weight_inter, nbK, delta_max)
    stop = timeit.default_timer()
    log.info(sol)
    log.info("\n nbS = %d; nbK = %d; delta_max = %d" % (graph.get_nbVertices(), nbK, delta_max))
    log.info('time : %f' % (stop - start))