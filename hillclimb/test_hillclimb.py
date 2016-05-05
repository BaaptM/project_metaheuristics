import logging
import sys
import os
import timeit
import statistics

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from graphstructure import lectureFichier
from hillclimb.hc import hillclimb, hillclimb_and_restart
from tools.enumGraphe import get_random_soluce

log = logging.getLogger(__name__)


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

    num_evaluations, best_score, best = hillclimb(init_function, move_operator, objective_function,
                                                  max_evaluations, delta_max)

    assert num_evaluations <= max_evaluations
    assert num_evaluations == 100
    assert best == 100
    assert best_score == 100


def test_file_hillcimb(graph, nbk, delta_max, mu, max_eval, move_operator):
    def init_function():
        return get_random_soluce(graph.get_nbVertices(), nbk, delta_max)

    num_evaluations, best_score, best = hillclimb(init_function, move_operator, graph.get_score,
                                                  max_eval, delta_max, mu)
    log.debug(best)
    return num_evaluations, best_score, best


def test_file_hillcimb_restart(graph, nbk, delta_max, mu, max_eval, move_operator):
    def init_function():
        return get_random_soluce(graph.get_nbVertices(), nbk, delta_max)

    num_evaluations, best_score, best = hillclimb_and_restart(init_function, move_operator, graph.get_score,
                                                              max_eval, delta_max, mu)
    log.debug(best)
    return num_evaluations, best_score, best


def main(graph, nbk, delta_max, mu, max_eval, iter, move_operator, logsPath, restart):
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    if restart:
        fh = logging.FileHandler(logsPath + "/hillclimbing_restart.log")
    else:
        fh = logging.FileHandler(logsPath + "/hillclimbing.log")

    fh.setLevel(logging.INFO)
    frmt = logging.Formatter('%(message)s')
    fh.setFormatter(frmt)
    log.addHandler(fh)

    all_num_evaluations = []
    all_best_score = []
    all_time = []

    if restart:
        log.info("-------RUNNING HILLCLIMB RESTART-------")
    else:
        log.info("-------RUNNING HILLCLIMB-------")
    for i in range(iter):
        start = timeit.default_timer()
        if restart:
            num_evaluations, best_score, best = test_file_hillcimb_restart(graph, nbk, delta_max, mu, max_eval, move_operator)
        else:
            num_evaluations, best_score, best = test_file_hillcimb(graph, nbk, delta_max, mu, max_eval, move_operator)
        stop = timeit.default_timer()
        log.debug('time : %f' % (stop - start))
        all_num_evaluations.append(num_evaluations)
        all_best_score.append(best_score)
        all_time.append(stop - start)
    log.info("nbS = %d; nbK = %d; delta_max = %d; mu = %r" % (graph.get_nbVertices(), nbk, delta_max, mu))
    log.info("for %d iteration with %d max_evaluations each, "
             "\n total time in sec : %r"
             "\n best score found is %d,"
             "\n mean time in sec : %r,"
             "\n mean best_score : %r, EcT : %r"
             "\n mean num_eval : %r"
             % (iter,
                max_eval,
                sum(all_time),
                min(score for score in all_best_score),
                statistics.mean(all_time),
                statistics.mean(all_best_score), statistics.stdev(all_best_score),
                statistics.mean(all_num_evaluations)))


if __name__ == '__main__':
    from tools.voisinageGraphe import pick_gen, sweep_gen, swap_gen
    if (len(sys.argv) != 2):
        lectureFichier.usage(sys.argv[0])
        exit()
    max_evaluations = 100
    delta_max = 3
    nbK = 3
    mu = .5
    iter = 100
    reader = lectureFichier.Reader(sys.argv[1])
    graph = reader.g
    move_operator = pick_gen
    logsPath = "../logs/"
    restart = False

    main(graph, nbK, delta_max, mu, max_evaluations, iter, move_operator, logsPath, restart)
