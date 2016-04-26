import random
import math
import logging
log = logging.getLogger(__name__)
#### struct to store best solution & score known
#### so ObjectiveFunction is a callable function and also store best sol
class ObjectiveFunction:
    def __init__(self,objective_function):
        self.objective_function=objective_function
        self.best=None
        self.best_score=None

    def __call__(self,solution):
        score=self.objective_function(solution)
        if self.best is None or score > self.best_score:
            self.best_score=score
            self.best=solution
            log.info('new best score: %f' % self.best_score)
        return score

#### probabilistically choosing a neighbour
#### return acceptation probability
def P(prev_score,next_score,temperature):
    if next_score < prev_score:
        return 1.0
    else:
        return math.exp( -abs(prev_score-next_score)/temperature )

#### cooling schedule
#### get start_temp cooling by alpha=[0,1]
def kirkpatrick_cooling(start_temp,alpha):
    T=start_temp
    while True:
        yield T
        T=alpha*T

def anneal(init_function,move_operator,objective_function,max_evaluations,start_temp,alpha):

    objective_function=ObjectiveFunction(objective_function)
    
    current=init_function()
    current_score=objective_function(current)
    num_evaluations=1
    
    cooling_schedule=kirkpatrick_cooling(start_temp,alpha)
    
    log.info('anneal started: score=%f' % current_score)
    
    for temperature in cooling_schedule:
        done = False
        # examine moves around current position
        for next in move_operator(current):
            if num_evaluations >= max_evaluations:
                done=True
                break
            
            next_score=objective_function(next)
            num_evaluations+=1
            
            # probablistically accept this solution
            # always accepting better solutions
            p=P(current_score,next_score,temperature)
            if random.random() < p:
                current=next
                current_score=next_score
                break
        if done: break # no better solution
    
    best_score=objective_function.best_score
    best=objective_function.best
    log.info('final temperature: %f' % temperature)
    log.info('anneal finished: num_evaluations=%d, best_score=%f' % (num_evaluations,best_score))
    return (num_evaluations,best_score,best)