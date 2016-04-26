# -*- coding: utf-8 -*-
# Implementation of hillclimbing algorithm with restart variant
# hillclimb(init_function,move_operator,objective_function,max_evaluations)
# where init_function() – the function used to create our initial solution (random ?)
#       move_operator() – the function we use to iterate over all possible “moves” for a given solution
#       objective_function() - used to assign a numerical score to a solution – how “good” the solution is (weight inter k)
#       max_evaluations - max number of iteration