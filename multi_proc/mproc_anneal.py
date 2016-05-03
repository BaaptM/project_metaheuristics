import os
import sys
import logging

DOSSIER_COURRANT = os.path.dirname(os.path.abspath(__file__))
DOSSIER_PARENT = os.path.dirname(DOSSIER_COURRANT)
sys.path.append(DOSSIER_PARENT)

from graphstructure import lectureFichier
from hillclimb import hc
from multiprocessing import Pool,cpu_count
from tools import voisinageGraphe, enumGraphe
from simulatedannealing import sa

log = logging.getLogger(__name__)

reader = lectureFichier.Reader('/net/stockage/nferon/data/cinquanteSommets.txt')
reader.readFile()
graph = reader.g

#todo pass in command line parameters
max_evaluations = 100
delta_max = 3
start_temp = 100
alpha = .95

nbK = 10
nb_proc = cpu_count()
nb_iterations = 100


def init_function():
    num_evaluations, best_score, best = hc.hillclimb(init_function_hillclimbing, voisinageGraphe.pick_gen, graph.get_weight_inter, max_evaluations, delta_max)
    return best

def init_function_hillclimbing():
    while True:
        sol = enumGraphe.get_random_soluce(graph.get_nbVertices(), nbK)
        if enumGraphe.get_max_delta(sol) <= delta_max:
            break
    return sol
    # return [[0,1,2,3,4,5,6,7],[8,9,10,11,12,13,14,15,16,17,18,19]]


def doWork(num_iteration):
    #todo level the logging info
    log.info('Start process number : %d' % num_iteration)
    start = timeit.default_timer()
    num_evaluations, best_score, best, temp = sa.anneal(init_function, voisinageGraphe.pick_gen, graph.get_weight_inter, max_evaluations, start_temp, alpha, delta_max)
    stop = timeit.default_timer()
    log.info('time : %f' % (stop - start))
    return num_evaluations, best_score, best, temp, (stop - start)


if __name__ == '__main__':
    import logging
    import sys
    import timeit
    import statistics

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    all_num_evaluations = []
    all_best_score = []
    all_time = []
    all_temp = []

    pool = Pool(processes=nb_proc)
    results = pool.map(doWork, range(nb_iterations))

    actual_best_score = sys.maxsize
    best = None

    for result in results:
        num_evaluations, best_score, best, temp, time = result
        if best_score < actual_best_score:
            actual_best = best
            actual_best_score = best_score
        all_temp.append(temp)
        all_num_evaluations.append(num_evaluations)
        all_best_score.append(best_score)
        all_time.append(time)

    log.info("\n nbS = %d; nbK = %d; delta_max = %d" % (graph.get_nbVertices(), nbK, delta_max))
    log.info("\n for %d iteration, best score found is %d,"
             "\n mean time : %f,"
             "\n mean best_score : %f, EcT : %f"
             "\n mean num_eval : %f,"
             "\n mean end temperature : %f" % (nb_iterations, min(score for score in all_best_score),
                                               statistics.mean(all_time),
                                               statistics.mean(all_best_score),
                                               statistics.stdev(all_best_score),
                                               statistics.mean(all_num_evaluations),
                                               statistics.mean(all_temp)))
    log.info("\n Best sol is %s score : %d" %(actual_best, actual_best_score))
