import logging
import sys
import os

DOSSIER_COURRANT = os.path.dirname(os.path.abspath(__file__))
DOSSIER_PARENT = os.path.dirname(DOSSIER_COURRANT)
sys.path.append(DOSSIER_PARENT)
log = logging.getLogger(__name__)

import enumerate as enum
from graphstructure import graphDataStructure as gs
from graphstructure import lectureFichier as lf
from tools.enumGraphe import *

reader = lf.Reader('../fichiersGraphes/dixSommets.txt')
reader.readFile()


if __name__ == '__main__':
###### TEST ######

    import logging
    import sys

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    import timeit
    nbK = 3
    delta_max = 3
    mu = 0
    start = timeit.default_timer()
    sol = enum.get_best_sol_enumeration(reader.g, reader.g.get_score, nbK, delta_max, mu)
    stop = timeit.default_timer()
    log.info(sol)
    log.info("\n nbS = %d; nbK = %d; delta_max = %d" % (reader.g.get_nbVertices(), nbK, delta_max))
    log.info('time : %f' % (stop - start))
