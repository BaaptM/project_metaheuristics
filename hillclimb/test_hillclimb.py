import logging
import random
import sys
import os
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
from graphstructure import lectureFichier
from hillclimb.hc import hillclimb, hillclimb_and_restart
from tools.enumGraphe import get_random_soluce, getSoluces, get_max_delta, validate_solutiongit
from tools.voisinageGraphe import pick_gen

log = logging.getLogger(__name__)
#reader = lectureFichier.Reader('../fichiersGraphes/cinquanteSommets.txt')
reader = lectureFichier.Reader('/net/stockage/nferon/data/cinquanteSommets.txt')
reader.readFile()
graph = reader.g
max_evaluations = 100
delta_max = 3
nbK = 3

def test_simple_hillclimb():
    """
    test whether given simple move_operator that just increments the number given
        best == the max number of evaluations
    """

    def objective_function(i):
        return i

    def move_operator(i):
        yield i + 1

    def init_function():
        return 1

    log.info("-------test_simple_hillclimb()-------")

    num_evaluations, best_score, best = hillclimb(init_function, move_operator, objective_function,
                                           max_evaluations, delta_max)

    assert num_evaluations == max_evaluations
    assert best == max_evaluations
    assert best_score == max_evaluations


def test_peak_hillclimb():
    '''
    check we hit the peak value and stop
    '''

    def objective_function(i):
        return i

    def move_operator(i):
        if i < 100:
            yield i + 1

    def init_function():
        return 1

    log.info("-------test_peak_hillclimb()-------")

    num_evaluations, best_score, best = hillclimb(init_function, move_operator, objective_function,
                                           max_evaluations, delta_max)

    assert num_evaluations <= max_evaluations
    assert num_evaluations == 100
    assert best == 100
    assert best_score == 100


def test_file_hillcimb():
    def init_function():
        while True:
            sol = get_random_soluce(graph.get_nbVertices(), nbK)
            if get_max_delta(sol) <= delta_max:
                break
        return sol
        #return [[0,1,2,3,4,5,6,7],[8,9,10,11,12,13,14,15,16,17,18,19]]

    num_evaluations, best_score, best = hillclimb(init_function, pick_gen, graph.get_weight_inter,
                                           max_evaluations, delta_max)
    log.info(best)
    return num_evaluations, best_score, best


def test_file_hillcimb_restart():
    def init_function():
        return random.choice(validate_solution(getSoluces(graph.get_nbVertices(), nbK), delta_max))

    num_evaluations, best_score, best = hillclimb_and_restart(init_function, pick_gen, graph.get_weight_inter,
                                                     max_evaluations, delta_max)
    log.info(best)

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
        num_evaluations, best_score, best = test_file_hillcimb()
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

