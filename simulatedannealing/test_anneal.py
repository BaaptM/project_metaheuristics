import os
import sys
import logging

DOSSIER_COURRANT = os.path.dirname(os.path.abspath(__file__))
DOSSIER_PARENT = os.path.dirname(DOSSIER_COURRANT)
sys.path.append(DOSSIER_PARENT)

from tools import enumGraphe, voisinageGraphe
from hillclimb import hc
from simulatedannealing import sa
from graphstructure import lectureFichier
from tools.enumGraphe import get_random_soluce



log = logging.getLogger(__name__)
#reader = lectureFichier.Reader('/net/stockage/nferon/data/cinquanSommets.txt')
reader = lectureFichier.Reader('../../fichiersGraphes/dixSommets.txt')

reader.readFile()
graph = reader.g
max_evaluations = 100
nbK = 3
delta_max = 3
start_temp = 100
alpha = .95
mu = .5
iter = 100

def test_file_sa():
    def init_function():
        #num_evaluations, best_score, best = hc.hillclimb(init_function_hillclimbing, voisinageGraphe.pick_gen, graph.get_weight_inter, max_evaluations, delta_max)
        #return best
        return get_random_soluce(graph.get_nbVertices(), nbK, delta_max)

    def init_function_hillclimbing():
        return get_random_soluce(graph.get_nbVertices(), nbK, delta_max)


    num_evaluations, best_score, best, temp = sa.anneal(init_function, voisinageGraphe.pick_gen, graph.get_score, max_evaluations, start_temp, alpha, delta_max, mu)
    log.debug(best)
    return num_evaluations, best_score, best, temp

if __name__ == '__main__':
    import logging
    import sys
    import timeit
    import statistics

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    fh = logging.FileHandler('simulated_annealing.log')
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
        num_evaluations, best_score, best, temperature = test_file_sa()
        stop = timeit.default_timer()
        log.debug('time : %f' % (stop - start))
        all_temp.append(temperature)
        all_num_evaluations.append(num_evaluations)
        all_best_score.append(best_score)
        all_time.append(stop - start)
    log.info("nbS = %d; nbK = %d; delta_max = %d; mu = %r; start_temp = %r; alpha = %r" % (graph.get_nbVertices(), nbK, delta_max, mu, start_temp, alpha))
    log.info("\n for %d iteration with %d max_evaluations each,"
             "\n best score found is %d,"
             "\n total time in sec : %r"
             "\n mean time in sec : %r,"
             "\n mean best_score : %r, EcT : %r"
             "\n mean num_eval : %r,"
             "\n mean end temperature : %r"%
                                        (iter,
                                        max_evaluations,
                                        min(score for score in all_best_score),
                                        sum(all_time),
                                        statistics.mean(all_time),
                                        statistics.mean(all_best_score),
                                        statistics.stdev(all_best_score),
                                        statistics.mean(all_num_evaluations),
                                        statistics.mean(all_temp)))




