import logging
import sys
import os
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
from enumerate import enum
from graphstructure import lectureFichier as lf

log = logging.getLogger(__name__)
reader = lf.Reader('../fichiersGraphes/dixSommets.txt')
#reader = lf.Reader('/net/stockage/nferon/data/cinquanteSommets.txt')
reader.readFile()


if __name__ == '__main__':
###### TEST ######

    import logging
    import sys

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    import timeit
    nbK = 3
    delta_max = 3
    mu = 1
    start = timeit.default_timer()
    sol = enum.get_best_sol_enumeration(reader.g, reader.g.get_score, nbK, delta_max, mu)
    stop = timeit.default_timer()
    log.info(sol)
    log.info("\n nbS = %d; nbK = %d; delta_max = %d; mu = %d" % (reader.g.get_nbVertices(), nbK, delta_max, mu))
    log.info('time : %f' % (stop - start))
