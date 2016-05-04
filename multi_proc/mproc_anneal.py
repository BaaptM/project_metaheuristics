import os
import sys
import logging

from tools import voisinageGraphe

DOSSIER_COURRANT = os.path.dirname(os.path.abspath(__file__))
DOSSIER_PARENT = os.path.dirname(DOSSIER_COURRANT)
sys.path.append(DOSSIER_PARENT)

from graphstructure import lectureFichier
from hillclimb import hc
from multiprocessing import Pool,cpu_count
from simulatedannealing import sa
from tools.enumGraphe import get_random_soluce
from tools import voisinageGraphe

log = logging.getLogger(__name__)

reader = lectureFichier.Reader('../../fichiersGraphes/dixSommets.txt')
#reader = lectureFichier.Reader('/net/stockage/nferon/data/cinquanteSommets.txt')
reader.readFile()
graph = reader.g

#todo pass in command line parameters
max_evaluations = 100
delta_max = 3
start_temp = 100
alpha = .95

nbK = 10
nb_proc = cpu_count()
iter = 100
mu = .5


def init_function():
    num_evaluations, best_score, best = hc.hillclimb(init_function_hillclimbing, voisinageGraphe.pick_gen, graph.get_score, max_evaluations, delta_max, mu)
    return best


def init_function_hillclimbing():
    return get_random_soluce(graph.get_nbVertices(), nbK, delta_max)


def doWork(num_iteration):
    log.debug('Start process number : %d' % num_iteration)
    start = timeit.default_timer()
    num_evaluations, best_score, best, temp = sa.anneal(init_function, voisinageGraphe.pick_gen, graph.get_score, max_evaluations, start_temp, alpha, delta_max, mu)
    stop = timeit.default_timer()
    log.debug('time : %f' % (stop - start))
    return num_evaluations, best_score, best, temp, (stop - start)


if __name__ == '__main__':
    import logging
    import sys
    import timeit
    import statistics

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    fh = logging.FileHandler('mproc_sim-anneal.log')
    fh.setLevel(logging.INFO)
    frmt = logging.Formatter('%(message)s')
    fh.setFormatter(frmt)
    log.addHandler(fh)

    all_num_evaluations = []
    all_best_score = []
    all_time = []
    all_temp = []

    pool = Pool(processes=nb_proc)
    log.info("-------MULTI_PROC SIMULATED ANNEALING-------")
    startWork = timeit.default_timer()
    results = pool.map(doWork, range(iter))
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
    log.info("nbS = %d; nbK = %d; delta_max = %d; mu = %r; start_temp = %r; alpha = %r" % (graph.get_nbVertices(), nbK, delta_max, mu, start_temp, alpha))
    log.info("for %d iteration with %d max_evaluations each, "
             "\n best score found is %d,"
             "\n total time in sec : %r"
             "\n mean time in sec : %r,"
             "\n mean best_score : %r, EcT : %r"
             "\n mean num_eval : %r,"
             "\n mean end temperature : %r" % (iter,
                                               max_evaluations,
                                               min(score for score in all_best_score),
                                               timeWork,
                                               statistics.mean(all_time),
                                               statistics.mean(all_best_score),
                                               statistics.stdev(all_best_score),
                                               statistics.mean(all_num_evaluations),
                                               statistics.mean(all_temp)))