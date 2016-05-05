import os 
import sys
import logging
import timeit
import statistics

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from graphstructure import lectureFichier
from hillclimb.hc import hillclimb, hillclimb_and_restart
from itertools import repeat
from tools.enumGraphe import get_random_soluce
from multiprocessing import Pool, cpu_count

log = logging.getLogger(__name__)


def doWork(iter, graph, move_operator, max_evaluations, delta_max, mu, nbk):

    def init_function():
        return get_random_soluce(graph.get_nbVertices(), nbk, delta_max)

    log.debug('Start process number : %d' %iter)
    start = timeit.default_timer()
    num_evaluations, best_score, best = hillclimb(init_function, move_operator, graph.get_score,
                                                  max_evaluations, delta_max, mu)
    stop = timeit.default_timer()
    log.debug('time : %f' % (stop - start))
    return num_evaluations, best_score, best, (stop - start)


def doWorkRestart(iter, graph, move_operator, max_evaluations, delta_max, mu, nbk):

    def init_function():
        return get_random_soluce(graph.get_nbVertices(), nbk, delta_max)

    log.debug('Start process number : %d' %iter)
    start = timeit.default_timer()
    num_evaluations, best_score, best = hillclimb_and_restart(init_function, move_operator, graph.get_score,
                                                  max_evaluations, delta_max, mu)
    stop = timeit.default_timer()
    log.debug('time : %f' % (stop - start))
    return num_evaluations, best_score, best, (stop - start)


def main(graph, nbk, delta_max, mu, max_eval, iter, move_operator, logsPath, restart):

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    if restart:
        fh = logging.FileHandler(logsPath + "/mproc_hillclimbing_restart.log")
    else:
        fh = logging.FileHandler(logsPath + "/mproc_hillclimbing.log")
    fh.setLevel(logging.INFO)
    frmt = logging.Formatter('%(message)s')
    fh.setFormatter(frmt)
    log.addHandler(fh)

    all_num_evaluations = []
    all_best_score = []
    all_time = []

    nb_proc = cpu_count()
    pool = Pool(processes=nb_proc)
    startWork = timeit.default_timer()
    if restart:
        results = pool.starmap(doWorkRestart, zip(range(iter), repeat(graph), repeat(move_operator), repeat(max_eval),
                                                  repeat(delta_max), repeat(mu), repeat(nbk)))
    else :
        results = pool.starmap(doWork, zip(range(iter), repeat(graph), repeat(move_operator), repeat(max_eval),
                                           repeat(delta_max), repeat(mu), repeat(nbk)))
    pool.close()
    pool.join()
    stopWork = timeit.default_timer()
    timeWork = (stopWork - startWork)

    actual_best_score = sys.maxsize

    if restart:
        log.info("-------MULTI_PROC HILLCLIMB RESTART-------")
    else:
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
    log.info("nbS = %d; nbK = %d; delta_max = %d; mu = %r" % (graph.get_nbVertices(), nbk, delta_max, mu))
    log.info("for %d iteration with %d max_evaluations each, "
             "\n total time in sec : %r"
             "\n best score found is %d,"
             "\n mean time in sec : %r,"
             "\n mean best_score : %r, EcT : %r"
             "\n mean num_eval : %r"
             % (iter,
                max_eval,
                timeWork,
                min(score for score in all_best_score),
                statistics.mean(all_time),
                statistics.mean(all_best_score), statistics.stdev(all_best_score),
                statistics.mean(all_num_evaluations)))


if __name__ == '__main__':
    from tools.voisinageGraphe import pick_gen, swap_gen, sweep_gen

    if len(sys.argv) != 2:
        lectureFichier.usage(sys.argv[0])
        exit()

    reader = lectureFichier.Reader(sys.argv[1])
    graph = reader.g
    max_evaluations = 100
    delta_max = 3
    nbk = 3
    iter = 100
    mu = .5
    move_operator = pick_gen
    logsPath = "../logs/"
    restart = False

    main(graph, nbk, delta_max, mu, max_evaluations, iter, move_operator, logsPath, restart)


