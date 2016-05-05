import logging
from tools.enumGraphe import validate_solution

log = logging.getLogger(__name__)


def hillclimb(init_function,move_operator,objective_function,max_evaluations, delta_max, mu):

    best=init_function()
    best_score=objective_function(best, mu)
    
    num_evaluations=1

    log.debug('hillclimb started: score=%f' % best_score)
    
    while num_evaluations < max_evaluations:
        # examine moves around current position
        move_made=False
        for next in validate_solution(move_operator(best), delta_max):
            if num_evaluations >= max_evaluations:
                break
            
            # see if this move is better than the current
            next_score=objective_function(next, mu)
            num_evaluations+=1
            if next_score < best_score:
                best=next
                best_score=next_score
                move_made=True
                break # depth first search
            
        if not move_made:
            break # couldn't find a better move
    
    log.debug('hillclimb finished: num_evaluations=%d , best_score=%d' % (num_evaluations, best_score))
    return num_evaluations,best_score,best


def hillclimb_and_restart(init_function,move_operator,objective_function,max_evaluations, delta_max, mu):
    # hillclimbing with restart implementation: repeat hillclimb until max_evaluations is reached

    best=None
    best_score=0
    
    num_evaluations=0
    while num_evaluations < max_evaluations:
        remaining_evaluations=max_evaluations-num_evaluations

        log.debug('(re)starting hillclimb %d/%d remaining' % (remaining_evaluations,max_evaluations))
        evaluated,score,found=hillclimb(init_function,move_operator,objective_function,remaining_evaluations, delta_max,
                                        mu)
        
        num_evaluations+=evaluated
        if score > best_score or best is None:
            best_score=score
            best=found
        
    return num_evaluations,best_score,best


