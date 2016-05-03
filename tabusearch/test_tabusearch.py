import logging
import sys
import os

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from tabusearch import ts
from graphstructure import lectureFichier
from tools import voisinageGraphe, enumGraphe

log = logging.getLogger(__name__)

#reader = lectureFichier.Reader('../fichiersGraphes/cinquanteSommets.txt')
reader = lectureFichier.Reader('/net/stockage/nferon/data/cinquanteSommets.txt')
reader.readFile()
graph = reader.g
max_evaluations = 100
delta_max = 3
nbK = 3

def test_file_tabusearch():
    def init_function():
        while True:
            sol = enumGraphe.get_random_soluce(graph.get_nbVertices(), nbK)
            if enumGraphe.get_max_delta(sol) <= delta_max:
                break
        return sol
        #return [[0,1,2,3,4,5,6,7],[8,9,10,11,12,13,14,15,16,17,18,19]]

    num_evaluations, best_score, best = ts.tabusearch(init_function, voisinageGraphe.pick_gen, graph.get_weight_inter,
                                                     max_evaluations, delta_max)
    log.info(best)
    return num_evaluations, best_score, best

if __name__ == '__main__':
    import logging
    import sys
    import timeit
    import statistics

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    all_num_evaluations = []
    all_best_score = []
    all_time = []
    for i in range(25):
        start = timeit.default_timer()
        num_evaluations, best_score, best = test_file_tabusearch()
        stop = timeit.default_timer()
        log.info('time : %f' % (stop - start))
        all_num_evaluations.append(num_evaluations)
        all_best_score.append(best_score)
        all_time.append(stop - start)
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

