"""Project META.
by Baptiste MASSET & Norbert Feron


Usage:
    main.py enum <path> --nbk=N --delta_max=N --mu=N
    main.py hc <path> --nbk=N --delta_max=N --mu=N --max_eval=N --iter=N --move=op [-r] [--mproc]
    main.py (-h | --help)
    main.py --version
Arguments:
    <path>  The path of the graph file
Options:
    --nbk=N             Set number of classes for graph partitionning [default: 3]
    --delta_max=N       Set the max differences of elements between classes [default: 3]
    --mu=N              Set MU value [default: 0.5]
    --temp=N            Set the start temperature for simulated annealing [default: 100]
    --alpha=N           Set the cooling coefficient for simulated annealing [default: 0.95]
    --max_eval=N        Set the max number of evaluating a solution
    --iter=N            Set the number of repeated execution (for loop)
    -r                  Restart hillclimb until max_eval is reached
    --move=op           Set the move operator for elementary move to another solution ( pNd ; swap ; sweep )
    --mproc              Running multi proc version of algorithms
    -h --help           Show this screen.
    --version           Show version.
"""
import docopt
import sys
import logging
from enumerate.test_enumerate import test_enum
from hillclimb import test_hillclimb
from multi_proc import mproc_hillclimb
from graphstructure.lectureFichier import Reader
from tools.voisinageGraphe import pick_gen, swap_gen, sweep_gen

log = logging.getLogger(__name__)

if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    arguments = docopt.docopt(__doc__, version='Project META v1.0')
    reader = Reader(arguments['<path>'])
    graph = reader.g
    nbk = int(arguments['--nbk'])
    delta_max = int(arguments['--delta_max'])
    mu = int(arguments['--mu'])

    if arguments['enum']:
        test_enum(graph, nbk, delta_max, mu)
    else:
        max_eval = int(arguments['--max_eval'])
        iter = int(arguments['--iter'])
        global move_operator
        if 'pNd' in arguments['--move']:
            move_operator = pick_gen
        elif 'swap' in arguments['--move']:
            move_operator = swap_gen
        elif 'sweep' in arguments['--move']:
            move_operator = sweep_gen

        if arguments['hc']:
            if arguments['--mproc']:
                mproc_hillclimb.main(graph, nbk, delta_max, mu, max_eval, iter, move_operator)
            else:
                if arguments['-r']:
                    test_hillclimb.mainRestart(graph, nbk, delta_max, mu, max_eval, iter, move_operator)
                else:
                    test_hillclimb.main(graph, nbk, delta_max, mu, max_eval, iter, move_operator)
        # todo implements the others
        # if arguments['sa']:
        # if arguments['-mproc']:
        # else:
        # if arguments['ts']:
        # if arguments['-mproc']:
        # else:
