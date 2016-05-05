import logging
import sys
import os

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from tabusearch import ts
from graphstructure import lectureFichier
from tools import voisinageGraphe
from tools.enumGraphe import get_random_soluce

log = logging.getLogger(__name__)

def test_file_tabusearch():
    def init_function():
        return get_random_soluce(graph.get_nbVertices(), nbK, delta_max)

    num_evaluations, best_score, best = ts.tabusearch(init_function, voisinageGraphe.pick_gen, graph.get_score,
                                                     max_evaluations, delta_max, mu)
    log.debug(best)
    return num_evaluations, best_score, best

if __name__ == '__main__':
    import logging
    import sys
    import timeit
    import statistics

    if len(sys.argv) != 2:
        lectureFichier.usage(sys.argv[0])
        exit()

    reader = lectureFichier.Reader(sys.argv[1])
    graph = reader.g
    max_evaluations = 100
    delta_max = 3
    nbK = 3
    mu = .5
    iter = 100

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    fh = logging.FileHandler('tabusearch.log')
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
        num_evaluations, best_score, best = test_file_tabusearch()
        stop = timeit.default_timer()
        log.debug('time : %f' % (stop - start))
        all_num_evaluations.append(num_evaluations)
        all_best_score.append(best_score)
        all_time.append(stop - start)
    log.info("nbS = %d; nbK = %d; delta_max = %d; mu = %r" % (graph.get_nbVertices(), nbK, delta_max, mu))
    log.info("for %d iteration with %d max_evaluations each, "
             "\n best score found is %d,"
             "\n total time in sec : %r"
             "\n mean time in sec : %r,"
             "\n mean best_score : %r, EcT : %r"
             "\n mean num_eval : %r"
             % (iter,
                max_evaluations,
                min(score for score in all_best_score),
                sum(all_time),
                statistics.mean(all_time),
                statistics.mean(all_best_score), statistics.stdev(all_best_score),
                statistics.mean(all_num_evaluations)))

