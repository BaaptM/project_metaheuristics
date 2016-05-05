import os 
import sys
import logging
import timeit
import statistics

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from graphstructure import lectureFichier
from tabusearch.ts import tabusearch
from itertools import repeat
from tools.enumGraphe import get_random_soluce
from multiprocessing import Pool, cpu_count

log = logging.getLogger(__name__)


def doWork(iter, graph, move_operator, max_evaluations, delta_max, mu, nbk):

    def init_function():
        return get_random_soluce(graph.get_nbVertices(), nbk, delta_max)


    log.debug('Start process number : %d' %iter)
    start = timeit.default_timer()
    num_evaluations, best_score, best = tabusearch(init_function, move_operator, graph.get_score,
                                                  max_evaluations, delta_max, mu)
    stop = timeit.default_timer()
    log.debug('time : %f' % (stop - start))
    return num_evaluations, best_score, best, (stop - start)


def main(graph, nbk, delta_max, mu, max_eval, iter, move_operator, logsPath):

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    fh = logging.FileHandler(logsPath + "/mproc_tabusearch.log")
    fh.setLevel(logging.INFO)
    frmt = logging.Formatter('%(message)s')
    fh.setFormatter(frmt)
    log.addHandler(fh)

    all_num_evaluations = []
    all_best_score = []
    all_time = []

    nb_proc = cpu_count()
    pool = Pool(processes=nb_proc)
    startWork = timeit.default_timer()
    results = pool.starmap(doWork, zip(range(iter), repeat(graph), repeat(move_operator), repeat(max_eval),
                                       repeat(delta_max), repeat(mu), repeat(nbk)))
    stopWork = timeit.default_timer()
    timeWork = (stopWork - startWork)

    actual_best_score = sys.maxsize

    log.info("-------MULTI_PROC TABUSEARCH-------")
    for result in results:
        num_evaluations, best_score, best, time = result
        if best_score < actual_best_score:
            actual_best = best
            actual_best_score = best_score
        all_num_evaluations.append(num_evaluations)
        all_best_score.append(best_score)
        all_time.append(time)
    log.info("Running on %d proc" % nb_proc)
    log.info("nbS = %d; nbK = %d; delta_max = %d; mu = %r; move_operator= %s" % (graph.get_nbVertices(), nbk, delta_max, mu, move_operator.__name__))
    log.info("for %d iteration with %d max_evaluations each, "
             "\n total time in sec : %r"
             "\n best score found is %d,"
             "\n mean time in sec : %r,"
             "\n mean best_score : %r, EcT : %r"
             "\n mean num_eval : %r"
             % (iter,
                max_eval,
                timeWork,
                min(score for score in all_best_score),
                statistics.mean(all_time),
                statistics.mean(all_best_score), statistics.stdev(all_best_score),
                statistics.mean(all_num_evaluations)))

if __name__ == '__main__':
    from tools.voisinageGraphe import pick_gen, swap_gen, sweep_gen

    if len(sys.argv) != 2:
        lectureFichier.usage(sys.argv[0])
        exit()

    reader = lectureFichier.Reader(sys.argv[1])
    graph = reader.g
    max_evaluations = 100
    delta_max = 3
    nbk = 3
    iter = 100
    mu = .5
    move_operator = pick_gen
    logsPath = "../logs/"

    main(graph, nbk, delta_max, mu, max_evaluations, iter, move_operator, logsPath)