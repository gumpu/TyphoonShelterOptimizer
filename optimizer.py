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

# This code assumes we move a whole village at a time.
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
                    # This can be optimized with a swap() function.
                    node.remove_assignment(assignment1)
                    node.remove_assignment(assignment2)
                    node.add_assignment(new_assignment1)
                    node.add_assignment(new_assignment2)
                else:
                    # Don't do the move
                    pass

            else:
                # Move village to another shelter
                shelter1_id = node.pick_used_shelter()
                shelter2_id = node.pick_any_shelter(exclude=shelter1_id)
                assignment1_id = node.pick_assignment(shelter1_id)
                assignment1    = node.assignments[assignment1_id]
                # Check if there is room in shelter2
                shelter2 = node.shelters[shelter2_id]
                if shelter2.capacity_left() > 0:
                    new_assignment1 = Assignment(
                            assignment1.village,
                            node.shelters[shelter2_id],
                            assignment1.count)
                    old_cost = assignment1.cost()
                    new_cost = new_assignment1.cost()
                    # What do we gain with this?
                    gain = old_cost - new_cost
                    if gain < 0:
                        u = math.exp(gain/temperature)
                    else:
                        u = 1
                    if random.random() < u:
                        node.remove_assignment(assignment1)
                        node.add_assignment(new_assignment1)
                    else:
                        # Don't do the move
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
