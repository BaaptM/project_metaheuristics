import hillclimb as hc
import logging

log = logging.getLogger(__name__)

def objective_function(i):
    return i


max_evaluations = 500


def test_simple_hillclimb():
    """
    test whether given simple move_operator that just increments the number given
        best == the max number of evaluations
    """

    def move_operator(i):
        yield i + 1

    def init_function():
        return 1

    log.info("-------test_simple_hillclimb()-------")

    num_evaluations, best_score, best = hc.hillclimb(init_function, move_operator, objective_function,
                                                            max_evaluations)

    assert num_evaluations == max_evaluations
    assert best == max_evaluations
    assert best_score == max_evaluations


def test_peak_hillclimb():
    '''
    check we hit the peak value and stop
    '''

    def move_operator(i):
        if i < 100:
            yield i + 1

    def init_function():
        return 1

    log.info("-------test_peak_hillclimb()-------")

    num_evaluations, best_score, best = hc.hillclimb(init_function, move_operator, objective_function,
                                                            max_evaluations)

    assert num_evaluations <= max_evaluations
    assert num_evaluations == 100
    assert best == 100
    assert best_score == 100


if __name__ == '__main__':
    import logging
    import sys

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    test_simple_hillclimb()
    test_peak_hillclimb()
