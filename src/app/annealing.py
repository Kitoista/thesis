import math
import random

def annealing(random_start,
              cost_function,
              random_neighbour,
              acceptance_probability,
              temperature,
              probability_start,
              probability_end,
              maxsteps=1000,
              debug_bundles=1,
              show=None,
              show_budles=1000,
              debug=True):
    """ Optimize the black-box function 'cost_function' with the simulated annealing algorithm."""
    state = random_start()
    cost = cost_function(state)

    # states, costs = [state], [cost]
    for step in range(maxsteps):
        # fraction = step / float(maxsteps)
        T = temperature(step, maxsteps, probability_start, probability_end)
        new_state, debug_message = random_neighbour(state, step, maxsteps)
        new_cost = cost_function(new_state)
        if debug and (step % debug_bundles == 0 or step == maxsteps-1):
            print(f"Step #{(step + 1):>4g} /{maxsteps:>4g} : T = {T:>4.3g}, cost = {cost:>4.3g}, new_cost = {new_cost:>4.3g} ... random chance = {acceptance_probability(cost, new_cost, T)} {debug_message}")
        if debug and show is not None and step != 0 and (step % show_budles == 0 or step == maxsteps-1):
            show(state, cost, step, maxsteps)
        if acceptance_probability(cost, new_cost, T) > random.uniform(0, 1):
            state, cost = new_state, new_cost
            # states.append(state)
            # costs.append(cost)
        #     print("  ==> Accept it!")
        # else:
        #    print(f"  ==> Reject it...")
    return state, cost_function(state)
