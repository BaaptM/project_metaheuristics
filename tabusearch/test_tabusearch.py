import logging
import sys
import os
import timeit
import statistics


PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from tabusearch import ts
from graphstructure import lectureFichier
from tools import voisinageGraphe
from tools.enumGraphe import get_random_soluce

log = logging.getLogger(__name__)


def test_file_tabusearch(graph, nbk, delta_max, mu, max_eval, move_operator):
    def init_function():
        return get_random_soluce(graph.get_nbVertices(), nbk, delta_max)

    num_evaluations, best_score, best = ts.tabusearch(init_function, move_operator, graph.get_score,
                                                      max_eval, delta_max, mu)
    log.debug(best)
    return num_evaluations, best_score, best


def main(graph, nbk, delta_max, mu, max_eval, iter, move_operator, logsPath):
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    fh = logging.FileHandler(logsPath + "/tabusearch.log")
    fh.setLevel(logging.INFO)
    frmt = logging.Formatter('%(message)s')
    fh.setFormatter(frmt)
    log.addHandler(fh)

    all_num_evaluations = []
    all_best_score = []
    all_time = []
    log.info("-------RUNNING TABU SEARCH-------")
    for i in range(iter):
        start = timeit.default_timer()
        num_evaluations, best_score, best = test_file_tabusearch(graph, nbk, delta_max, mu, max_eval, move_operator)
        stop = timeit.default_timer()
        log.debug('time : %f' % (stop - start))
        all_num_evaluations.append(num_evaluations)
        all_best_score.append(best_score)
        all_time.append(stop - start)
    log.info("nbS = %d; nbK = %d; delta_max = %d; mu = %r" % (graph.get_nbVertices(), nbk, delta_max, mu))
    log.info("for %d iteration with %d max_evaluations each, "
             "\n best score found is %d,"
             "\n total time in sec : %r"
             "\n mean time in sec : %r,"
             "\n mean best_score : %r, EcT : %r"
             "\n mean num_eval : %r"
             % (iter,
                max_eval,
                min(score for score in all_best_score),
                sum(all_time),
                statistics.mean(all_time),
                statistics.mean(all_best_score), statistics.stdev(all_best_score),
                statistics.mean(all_num_evaluations)))

if __name__ == '__main__':
    from tools.voisinageGraphe import pick_gen

    if len(sys.argv) != 2:
        lectureFichier.usage(sys.argv[0])
        exit()

    reader = lectureFichier.Reader(sys.argv[1])
    graph = reader.g
    move_operator = pick_gen
    max_eval = 100
    delta_max = 3
    nbk = 3
    mu = .5
    iter = 100
    logsPath = "../logs/"

    main(graph, nbk, delta_max, mu, max_eval, iter, move_operator, logsPath)