from simulatedannealing.sa import *
from graphstructure.lectureFichier import *
from tools.enumGraphe import *
from tools.voisinageGraphe import *
log = logging.getLogger(__name__)

reader = Reader('../../fichiersGraphes/dixSommets.txt')
reader.readFile()
graph = reader.g
max_evaluations = 100
nbK = 3
delta_max = 3
start_temp = 100
alpha = .75

def test_file_sa():
    def init_function():
        return random.choice(validate_solution(getSoluces(graph.get_nbVertices(), nbK), delta_max))
        #return [[0,1,2,3,4,5,6,7,8,9],[10,11,12,13,14,15,16,17,18,19]]

    num_evaluations, best_score, best, temp = anneal(init_function, pick_gen, graph.get_weight_inter, max_evaluations, start_temp, alpha, delta_max)
    log.info(best)
    return num_evaluations, best_score, best, temp

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
    global temps
    for i in range(100):
        start = timeit.default_timer()
        num_evaluations, best_score, best, temperature = test_file_sa()
        stop = timeit.default_timer()
        log.info('time : %f' % (stop - start))
        all_temp.append(temperature)
        all_num_evaluations.append(num_evaluations)
        all_best_score.append(best_score)
        all_time.append(stop - start)
    log.info("\n nbS = %d; nbK = %d; delta_max = %d" % (graph.get_nbVertices(), nbK, delta_max))
    log.info("\n for 100 iteration, best score found is %d,"
             "\n mean time : %f,"
             "\n mean best_score : %f, EcT : %f"
             "\n mean num_eval : %f,"
             "\n mean end temperature : %f"%(min(score for score in all_best_score),
                                        statistics.mean(all_time),
                                        statistics.mean(all_best_score),
                                        statistics.stdev(all_best_score),
                                        statistics.mean(all_num_evaluations),
                                        statistics.mean(all_temp)))




