import os
import sys
import logging
import timeit
import statistics

from tools import voisinageGraphe

DOSSIER_COURRANT = os.path.dirname(os.path.abspath(__file__))
DOSSIER_PARENT = os.path.dirname(DOSSIER_COURRANT)
sys.path.append(DOSSIER_PARENT)

from graphstructure import lectureFichier
from hillclimb import hc
from itertools import repeat
from multiprocessing import Pool,cpu_count
from simulatedannealing import sa
from tools.enumGraphe import get_random_soluce
from tools.voisinageGraphe import pick_gen

log = logging.getLogger(__name__)

def doWork(iter, graph, move_operator, max_evaluations, delta_max, mu,  temp, alpha, nbk):
    def init_function():
        num_evaluations, best_score, best = hc.hillclimb(init_function_hillclimbing, move_operator, graph.get_score, max_evaluations, delta_max, mu)
        return best


    def init_function_hillclimbing():
        return get_random_soluce(graph.get_nbVertices(), nbk, delta_max)

    log.debug('Start process number : %d' % iter)
    start = timeit.default_timer()
    num_evaluations, best_score, best, temp = sa.anneal(init_function, move_operator, graph.get_score, max_evaluations, temp, alpha, delta_max, mu)
    stop = timeit.default_timer()
    log.debug('time : %f' % (stop - start))
    return num_evaluations, best_score, best, temp, (stop - start)


def main(graph, nbk, delta_max, mu,  temp, alpha, max_eval, iter, move_operator, logsPath):

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    fh = logging.FileHandler(logsPath + "/mproc_simulated-annealing.log")
    fh.setLevel(logging.INFO)
    frmt = logging.Formatter('%(message)s')
    fh.setFormatter(frmt)
    log.addHandler(fh)

    all_num_evaluations = []
    all_best_score = []
    all_time = []
    all_temp = []

    nb_proc = cpu_count()
    pool = Pool(processes=nb_proc)
    log.info("-------MULTI_PROC SIMULATED ANNEALING-------")
    startWork = timeit.default_timer()
    results = pool.starmap(doWork, zip(range(iter), repeat(graph), repeat(move_operator), repeat(max_eval), repeat(delta_max), repeat(mu), repeat(temp), repeat(alpha), repeat(nbk)))
    stopWork = timeit.default_timer()
    timeWork = (stopWork - startWork)

    actual_best_score = sys.maxsize
    for result in results:
        num_evaluations, best_score, best, temp, time = result
        if best_score < actual_best_score:
            actual_best = best
            actual_best_score = best_score
        all_temp.append(temp)
        all_num_evaluations.append(num_evaluations)
        all_best_score.append(best_score)
        all_time.append(time)

    log.info("Running on %d proc" % nb_proc)
    log.info("nbS = %d; nbK = %d; delta_max = %d; mu = %r; start_temp = %r; alpha = %r" % (graph.get_nbVertices(), nbk, delta_max, mu, temp, alpha))
    log.info("for %d iteration with %d max_evaluations each, "
             "\n best score found is %d,"
             "\n total time in sec : %r"
             "\n mean time in sec : %r,"
             "\n mean best_score : %r, EcT : %r"
             "\n mean num_eval : %r,"
             "\n mean end temperature : %r" % (iter,
                                               max_eval,
                                               min(score for score in all_best_score),
                                               timeWork,
                                               statistics.mean(all_time),
                                               statistics.mean(all_best_score),
                                               statistics.stdev(all_best_score),
                                               statistics.mean(all_num_evaluations),
                                               statistics.mean(all_temp)))

if __name__ == '__main__':
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
    temp=100
    alpha=0.95
    move_operator = pick_gen
    logsPath = "../logs/"

    main(graph, nbk, delta_max, mu, temp, alpha, max_evaluations, iter, move_operator, logsPath)


