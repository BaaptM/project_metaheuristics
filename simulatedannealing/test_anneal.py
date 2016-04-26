import logging
from simulatedannealing.sa import *
from graphstructure.lectureFichier import *
from tools.enumGraphe import *
from tools.voisinageGraphe import *
log = logging.getLogger(__name__)

def test_file_sa(graph, nbK, max_evaluations, start_temp, alpha):
    def init_function():
        #return random.choice(getSoluces(graph.get_nbVertices(), nbK))
        return [[0,1,2,3,4,5,6,7,8,9],[10,11,12,13,14,15,16,17,18,19]]

    num_evaluations, best_score, best = anneal(init_function, pick_gen, graph.get_weight_inter, max_evaluations, start_temp, alpha)
    log.info(best)
    log.info(graph.get_weight_inter(best))

if __name__ == '__main__':
    import logging
    import sys

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    reader = Reader('../../fichiersGraphes/vingtSommets.txt')
    reader.readFile()
    test_file_sa(reader.g, 2, 1000, 100, 0.85)

