import logging
import sys
import os
import timeit

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from enumerate import enum
from graphstructure import lectureFichier as lf

log = logging.getLogger(__name__)


def test_enum(graph, nbk, delta_max, mu):
    return enum.get_best_sol_enumeration(graph, graph.get_score, nbk, delta_max, mu)


def main(graph, nbk, delta_max, mu, logsPath):

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    fh = logging.FileHandler(logsPath + "/enumerate.log")
    fh.setLevel(logging.INFO)
    frmt = logging.Formatter('%(message)s')
    fh.setFormatter(frmt)
    log.addHandler(fh)

    start = timeit.default_timer()
    (weight, sol) = test_enum(graph, nbk, delta_max, mu)
    stop = timeit.default_timer()
    log.debug(sol)
    log.info("-------ENUMERATE-------")
    log.info("nbS = %d; nbK = %d; delta_max = %d; mu = %r" % (graph.get_nbVertices(), nbk, delta_max, mu))
    log.info("best score is : %d,"
             "\n total time : %r" % (weight, (stop - start)))

if __name__ == '__main__':
    if len(sys.argv) != 2:
        lf.usage(sys.argv[0])
        exit()
    reader = lf.Reader(sys.argv[1])
    graph = reader.g
    nbk = 3
    delta_max = 3
    mu = 1
    logsPath = "../logs"

    main(graph, nbk, delta_max, mu, logsPath)