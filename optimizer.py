#!/usr/bin/env python2
"""
Usage:
    optimizer.py <problem>

"""

import re
from  shelter import Shelter
from     node import Node, Assignment
from  village import Village
from   svgout import Plot
from   docopt import docopt
import random
import   math

#---------------------------------------------------------------------------
# Simulated Annealing
#

# TODO Refactor
def sa(node):
    cooling_factor = 0.9999   # This needs to be properly tuned
    # TODO this needs to be determined automatically.
    temperature    = 8800.0   # This needs to be properly tuned

    best_score = None

    with open("runlog.csv", "w") as run_log_file:
        run_log_file.write("temperature objective\n")
        n = len(node.shelters)
        while temperature > 0.01: # This needs to be tuned.
            objective = node.objective()
            if best_score is not None and objective < best_score:
                best_score = objective
                print("{:6.2f} - {:12.1f}".format(temperature, objective))
            elif best_score is None:
                best_score = objective
                print("{:6.2f} - {:12.1f}".format(temperature, objective))
            else:
                pass

            run_log_file.write("{:.6f} {:.3f}\n".format(temperature, objective))
            temperature = cooling_factor*temperature

            if random.random() > 0.5:
                # Swap villages between two shelters
                shelter1_id = node.pick_used_shelter()
                shelter2_id = node.pick_used_shelter(exclude=shelter1_id)
                assignment1_id = node.pick_assignment(shelter1_id)
                assignment2_id = node.pick_assignment(shelter2_id)

                assignment1     = node.assignments[assignment1_id]
                assignment2     = node.assignments[assignment2_id]
                new_assignment1 = Assignment(assignment2.village,
                                             assignment1.shelter,
                                             assignment1.count)
                new_assignment2 = Assignment(assignment1.village,
                                             assignment2.shelter,
                                             assignment2.count)
                old_cost = assignment1.cost() + assignment2.cost()
                new_cost = new_assignment1.cost() + new_assignment2.cost()
                gain = old_cost - new_cost

                if gain < 0:
                    u = math.exp(gain/temperature)
                else:
                    u = 1
                if random.random() < u:
                    # Do the move
                    node.assignments[assignment1_id] = new_assignment1
                    node.assignments[assignment2_id] = new_assignment2
                else:
                    # Don't do the move
                    #print("No {}".format(gain))
                    pass
            else:
                # Pick two distinct random shelters
                shelter1_id = node.pick_used_shelter()
                shelter2_id = node.pick_any_shelter(exclude=shelter1_id)

                assignment_id = node.pick_assignment(shelter1_id)
                assignment    = node.assignments[assignment_id]

                shelter1 = node.shelters[shelter1_id]
                shelter2 = node.shelters[shelter2_id]
                #print("{} {} {}".format(temperature, shelter1_id, shelter2_id))
                #print("{} {}  -> {}".format(shelter1_id, assignment_id, shelter2_id))

                cost_old   = assignment.cost()

                count_old  = assignment.count
                cap_target = shelter2.capacity_left()

                delta = min(count_old, cap_target)
                # print("Count {} -> Cap left {}".format(count_old, cap_target))
                if delta > 0:
                    # Compute the gain from moving villagers
                    # from shelter1 to shelter2
                    new_assignment1 = None
                    new_assignment2 = None
                    if count_old <= cap_target:
                        # Shelter2 has enough capacity
                        new_assignment1 = Assignment(
                                assignment.village, shelter2, count_old)
                        cost_new = new_assignment1.cost()
                    elif count_old > cap_target:
                        # Shelter2 has too little capacity
                        # only part of the villagers can be moved
                        new_assignment1 = Assignment(
                                assignment.village, shelter2, delta)
                        new_assignment2 = Assignment(
                                assignment.village, shelter1, count_old - cap_target)
                        cost_new  = new_assignment1.cost()
                        cost_new += new_assignment2.cost()
                        # TODO should take in account new_assignment2

                    # Compute what we would gain by doing this move.
                    # We want to drive the cost down. This computes
                    # by how much we drive it down (gain > 0 is good)
                    gain = cost_old - cost_new
                    # Should we do this move?
                    if gain < 0:
                        u = math.exp(gain/temperature)
                    else:
                        u = 1
                    if random.random() < u:
                        # Do the move
                        #print("Yes {}".format(gain))
                        # TODO This should be in a method
                        assignment.shelter.used      -= new_assignment1.count
                        new_assignment1.shelter.used += new_assignment1.count
                        node.assignments[assignment_id] = new_assignment1
                        if new_assignment2 is not None:
                            node.add_assignment(new_assignment2)
                    else:
                        # Don't do the move
                        #print("No {}".format(gain))
                        pass
                else:
                    pass

    print("done")


if __name__ == '__main__':
    arguments = docopt(__doc__)

    problem_file = arguments['<problem>']

    #================================================================
    # Set the seed for the random generator. This will make
    # the results reproducible and therefore easier to debug.
    #
    random.seed(19671111)

    node = Node()
    # Read the problem from file
    node.read_problem(problem_file)

    print(str(node))
    # Create a initial solution we can optimize from
    node.initial_solution()
    # Plot the problem
    node.plot(id=1, assignment=False)
    # Plot the initial solution
    node.plot(id=2)

    # Use simulated annealing to optimize the initial solution
    sa(node)

    # Report the solution
    with open("report.txt", "w") as report_file:
        node.print_solution(report_file)

    # Create a visualization in svg
    node.plot(id=3)

    #print(node)

# vi: spell spl=en
