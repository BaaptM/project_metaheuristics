# -*- coding: utf-8 -*-
# Implementation of simulated annealing algorithm
# anneal(init_function,move_operator,objective_function,max_evaluations,start_temp,alpha)
# where init_function() – the function used to create our initial solution (random? ; hillcimb output?)
#       move_operator() – the function we use to iterate over all possible “moves” for a given solution
#       objective_function() - used to assign a numerical score to a solution – how “good” the solution is (weight inter k)
#       max_evaluations - max number of iteration
#       start_temp - initial temperature
#       alpha - cooling factor [0,1] (prof: try with: [.85, .95] or .5)
