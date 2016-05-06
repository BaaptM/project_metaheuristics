Projet de Métaheuristique Norbert FERON Baptiste MASSET

### Requirements

- Docopt
```shell
pip3 install docopt
```
### Usage
All command can be done with main.py following the doc:
```shell
Usage:
    main.py enum <path> [--nbk=N --delta_max=N --mu=N]
    main.py hc <path> [--nbk=N --delta_max=N --mu=N] --max_eval=N --iter=N --move=op [-r] [--mproc]
    main.py ts <path> [--nbk=N --delta_max=N --mu=N --tabu=N] --max_eval=N --iter=N --move=op [--mproc]
    main.py sa <path> [--nbk=N --delta_max=N --mu=N] --temp=N --alpha=N --max_eval=N --iter=N --move=op [--mproc]
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
    --tabu=N            Set the tabu queue size [default: 10]
    -r                  Restart hillclimb until max_eval is reached
    --move=op           Set the move operator for elementary move to another solution ( pNd ; swap ; sweep )
    --mproc             Running multi proc version of algorithms
    -h --help           Show this screen.
    --version           Show version.
```