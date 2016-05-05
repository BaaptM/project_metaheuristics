import os
import sys
import logging
import timeit
import statistics

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from hillclimb import hc
from simulatedannealing import sa
from graphstructure import lectureFichier
from tools.enumGraphe import get_random_soluce

log = logging.getLogger(__name__)


def test_file_sa(graph, nbk, delta_max, mu, temp, alpha, max_eval, move_operator):
    def init_function_hillclimb():
        num_evaluations, best_score, best = hc.hillclimb(init_function_hillclimb, move_operator, graph.get_score, max_eval, delta_max, mu)
        return best

    def init_function():
        return get_random_soluce(graph.get_nbVertices(), nbk, delta_max)

    num_evaluations, best_score, best, temp = sa.anneal(init_function, move_operator, graph.get_score, max_eval, temp, alpha, delta_max, mu)
    log.debug(best)
    return num_evaluations, best_score, best, temp


def main(graph, nbk, delta_max, mu, temp, alpha, max_eval, iter, move_operator, logsPath):

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    fh = logging.FileHandler(logsPath + "/simulated_annealing.log")
    fh.setLevel(logging.INFO)
    frmt = logging.Formatter('%(message)s')
    fh.setFormatter(frmt)
    log.addHandler(fh)

    all_num_evaluations = []
    all_best_score = []
    all_time = []
    all_temp = []
    global temps
    log.info("-------RUNNING SIMULATED ANNEALING-------")
    for i in range(iter):
        start = timeit.default_timer()
        num_evaluations, best_score, best, temperature = test_file_sa(graph, nbk, delta_max, mu, temp, alpha, max_eval, move_operator)
        stop = timeit.default_timer()
        log.debug('time : %f' % (stop - start))
        all_temp.append(temperature)
        all_num_evaluations.append(num_evaluations)
        all_best_score.append(best_score)
        all_time.append(stop - start)
    log.info("nbS = %d; nbK = %d; delta_max = %d; mu = %r; start_temp = %r; alpha = %r" % (graph.get_nbVertices(), nbk, delta_max, mu, temp, alpha))
    log.info("\n for %d iteration with %d max_evaluations each,"
             "\n best score found is %d,"
             "\n total time in sec : %r"
             "\n mean time in sec : %r,"
             "\n mean best_score : %r, EcT : %r"
             "\n mean num_eval : %r,"
             "\n mean end temperature : %r"%
                                        (iter,
                                        max_eval,
                                        min(score for score in all_best_score),
                                        sum(all_time),
                                        statistics.mean(all_time),
                                        statistics.mean(all_best_score),
                                        statistics.stdev(all_best_score),
                                        statistics.mean(all_num_evaluations),
                                        statistics.mean(all_temp)))

if __name__ == '__main__':
    from tools.voisinageGraphe import pick_gen

    if (len(sys.argv) != 2):
        lectureFichier.usage(sys.argv[0])
        exit()

    reader = lectureFichier.Reader(sys.argv[1])
    graph = reader.g
    max_eval = 100
    move_operator = pick_gen
    nbk = 3
    delta_max = 3
    temp = 100
    alpha = .95
    mu = .5
    iter = 100
    logsPath = "../logs/"

    main(graph, nbk, delta_max, mu, temp, alpha, max_eval, iter, move_operator, logsPath)