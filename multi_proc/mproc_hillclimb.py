import os 
import sys
import logging

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from graphstructure import lectureFichier
from hillclimb.hc import hillclimb
from tools import enumGraphe
from multiprocessing import Pool, cpu_count
from tools.voisinageGraphe import pick_gen

log = logging.getLogger(__name__)
reader = lectureFichier.Reader('../../fichiersGraphes/dixSommets.txt')
#reader = lectureFichier.Reader('/net/stockage/nferon/data/cinquanteSommets.txt')
reader.readFile()
graph = reader.g

max_evaluations = 100
delta_max = 3
nbK = 3
nb_proc = cpu_count()
iter = 100
mu = .5

def init_function():
    while True:
        sol = enumGraphe.get_random_soluce(graph.get_nbVertices(), nbK, delta_max)
        if enumGraphe.get_max_delta(sol) <= delta_max:
            break
    return sol
    # return [[0,1,2,3,4,5,6,7],[8,9,10,11,12,13,14,15,16,17,18,19]]


def doWork(num_iteration):
    log.debug('Start process number : %d' %num_iteration)
    start = timeit.default_timer()
    num_evaluations, best_score, best = hillclimb(init_function, pick_gen, graph.get_score,
                                                  max_evaluations, delta_max, mu)
    stop = timeit.default_timer()
    log.debug('time : %f' % (stop - start))
    return num_evaluations, best_score, best, (stop - start)


if __name__ == '__main__':
    import logging
    import sys
    import timeit
    import statistics

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    fh = logging.FileHandler('mproc_hillclimbing.log')
    fh.setLevel(logging.INFO)
    frmt = logging.Formatter('%(message)s')
    fh.setFormatter(frmt)
    log.addHandler(fh)

    all_num_evaluations = []
    all_best_score = []
    all_time = []

    pool = Pool(processes=nb_proc)
    startWork = timeit.default_timer()
    results = pool.map(doWork, range(iter))
    stopWork = timeit.default_timer()
    timeWork = (stopWork - startWork)

    actual_best_score = sys.maxsize

    log.info("-------MULTI_PROC HILLCLIMB-------")
    for result in results:
        num_evaluations, best_score, best, time = result
        if best_score < actual_best_score:
            actual_best = best
            actual_best_score = best_score
        all_num_evaluations.append(num_evaluations)
        all_best_score.append(best_score)
        all_time.append(time)
    log.info("Running on %d proc" % nb_proc)
    log.info("nbS = %d; nbK = %d; delta_max = %d; mu = %r" % (graph.get_nbVertices(), nbK, delta_max, mu))
    log.info("for %d iteration with %d max_evaluations each, "
             "\n total time in sec : %r"
             "\n best score found is %d,"
             "\n mean time in sec : %r,"
             "\n mean best_score : %r, EcT : %r"
             "\n mean num_eval : %r"
             % (iter,
                max_evaluations,
                timeWork,
                min(score for score in all_best_score),
                statistics.mean(all_time),
                statistics.mean(all_best_score), statistics.stdev(all_best_score),
                statistics.mean(all_num_evaluations)))
