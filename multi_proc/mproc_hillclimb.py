import os 
import sys
import logging

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from graphstructure import lectureFichier
from hillclimb.hc import hillclimb
from enumerate import enum
from multiprocessing import Pool, cpu_count
from tools.voisinageGraphe import pick_gen

log = logging.getLogger(__name__)
reader = lectureFichier.Reader('/net/stockage/nferon/data/cinquanteSommets.txt')
reader.readFile()
graph = reader.g

max_evaluations = 100
delta_max = 3
nbK = 10
nb_proc = cpu_count()
nb_iterations = 100


def init_function():
    while True:
        sol = enum.get_random_soluce(graph.get_nbVertices(), nbK)
        if enum.get_max_delta(sol) <= delta_max:
            break
    return sol
    # return [[0,1,2,3,4,5,6,7],[8,9,10,11,12,13,14,15,16,17,18,19]]


def doWork(num_iteration):
    log.info('Start process number : %d' %num_iteration)
    start = timeit.default_timer()
    num_evaluations, best_score, best = hillclimb(init_function, pick_gen, graph.get_weight_inter,
                                                  max_evaluations, delta_max)
    stop = timeit.default_timer()
    log.info('time : %f' % (stop - start))
    return num_evaluations, best_score, best, (stop - start)


if __name__ == '__main__':
    import logging
    import sys
    import timeit
    import statistics

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    all_num_evaluations = []
    all_best_score = []
    all_time = []

    pool = Pool(processes=nb_proc)
    results = pool.map(doWork, range(nb_iterations))

    actual_best_score = sys.maxsize
    best = None

    for result in results:
        num_evaluations, best_score, best, time = result
        if best_score < actual_best_score:
            actual_best = best
            actual_best_score = best_score
        all_num_evaluations.append(num_evaluations)
        all_best_score.append(best_score)
        all_time.append(time)

    log.info("\n nbS = %d; nbK = %d; delta_max = %d"%(graph.get_nbVertices(),nbK,delta_max))
    log.info("\n for 100 iteration, "
             "\n best score found is %d,"
             "\n mean time : %f,"
             "\n mean best_score : %f, EcT : %f"
             "\n mean num_eval : %f"
             %(min(score for score in all_best_score),
               statistics.mean(all_time),
               statistics.mean(all_best_score), statistics.stdev(all_best_score),
               statistics.mean(all_num_evaluations)))
    log.info("\n Best sol is %s score : %d" %(actual_best, actual_best_score))
