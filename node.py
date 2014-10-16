# vi: spell spl=en
#

import re
from shelter import Shelter
from village import Village
from svgout  import Plot
import math
import random


def dist(x1, y1, x2, y2):
    dx = x1 - x2
    dy = y1 - y2
    return math.sqrt(dx*dx + dy*dy)


class Assignment(object):
    def __init__(self, village, shelter, count):
        self.village    = village
        self.shelter = shelter
        self.count   = count

    def cost(self):
        """Cost of this assignemnt
        This determines what is optimized.
        Possible factors to put in are:
           distance from village to shelter
           How full the shelter is
           Cost to build the shelter
           Cost to open the shelter if it is not there yet

            This need to be balanced too.
        """

        return self.count*dist(self.shelter.position[0],
                    self.shelter.position[1],
                    self.village.cx,
                    self.village.cy)
        # Simply use only the cost to test first debug SA.
#        return self.shelter.cost


    def __str__(self):
        return "{} -> ({:5d}) -> {}".format(
                self.village.id, self.count, self.shelter.id)

class Node(object):
    def __init__(self):
        self.shelters     = [] # Ordered list of shelters
        self.villages        = [] # Ordered list of villages
        # The current solution
        self.assignments  = [] # how many students are assigned to which shelter
        #self.shelters_used = [] # Which of the shelters are used

    def __str__(self):
        return "# Shelters {}  # Villages {}".format(
                len(self.shelters), len(self.villages))

    def objective(self):
        """The objective function, gives a measure of
        how good the current solution is"""
        cost = 0
        for a in self.assignments:
            cost += a.cost()
        return cost

    def pick_assignment(self, shelter_id):
        """Randomly pick one of the assignments for the given
        shelter."""
        ids = []
        for i in range(0, len(self.assignments)):
            if self.assignments[i].shelter.id == shelter_id:
                ids.append(i)

        if len(ids) == 0:
            print("not found {}".format(shelter_id))
            return None   # Returns assignment index
        else:
            #print(ids)
            return random.choice(ids)


    def pick_used_shelter(self, exclude=None):
        """Pick one of the shelters that are already used in one or
        more assignments."""

        n = len(self.shelters)
        id = random.randint(0, n-1)
        while self.shelters[id].used == 0 or (
                (exclude is not None) and (id == exclude)) :
            id = random.randint(0, n-1)

        assert(self.shelters[id].used >0)
        return id

    def pick_any_shelter(self, exclude=None):
        n = len(self.shelters)
        id = random.randint(0, n-1)
        if exclude is not None:
            while id == exclude:
                id = random.randint(0, n-1)
        return id

    def add_assignment(self, assignment):
        found = False
        # print(assignment)
        for a in self.assignments:
            if (a.shelter.id == assignment.shelter.id and
                a.village.id   == assignment.village.id):
                #print(a)
                a.count       += assignment.count
                #a.shelter.used += assignment.count
                found = True
                #print(a)
                break

        #print(found)
        if not found:
            self.assignments.append(assignment)


    def initial_solution(self):
        """Create a greedy initial solution"""
        for a in self.villages:
            demand = a.demand
            for s in self.shelters:
                delta = s.capacity - s.used
                if delta > 0 and demand > 0:
                    if demand < delta:
                        delta = demand
                    s.used += delta
                    demand -= delta
                    self.assignments.append(Assignment(a, s, delta))

            if demand > 0:
                print("Not enough shelter capacity!")
                exit(1)


    def print_solution(self, f):
        f.write("village -> Number of students -> shelter\n")
        for a in self.assignments:
            f.write(str(a))
            f.write("\n")


    def plot(self, id=1, assignment=True):
        tempx = []
        tempy = []
        for s in self.shelters:
            tempx.append(s.position[0])
            tempy.append(s.position[1])
        for a in self.villages:
            tempx.append(a.cx)
            tempy.append(a.cy)
        xmax = max(tempx)
        xmin = min(tempx)
        ymax = max(tempy)
        ymin = min(tempy)

        with open("p{:05}.svg".format(id), "w") as outf:
            p = Plot(outf)
            p.set_domain((xmin, xmax, ymin, ymax))
            for s in self.shelters:
                p.box(s.position[0], s.position[1],
                        r=8+8*s.capacity*s.capacity/49)

            for village in self.villages:
                p.dot(village.cx, village.cy, r=8)

            if assignment:
                for a in self.assignments:
                    village = a.village
                    shelter = a.shelter
                    p.line(village.cx, village.cy, 
                           shelter.position[0], shelter.position[1], 
                           color="red" )

            id = 0
            for s in self.shelters:
                p.label(s.position[0], s.position[1], str(id))
                id += 1

            id = 0
            for a in self.villages:
                p.label(a.cx, a.cy, str(id))
                id += 1
            p.close()


    def read_problem(self, filename):
        """Read the problem from file"""
        village_id   = 0
        shelter_id = 0
        with open(filename, "r") as problem_file:
            for line in problem_file:
                if re.match("^#", line):
                    pass # comment
                elif re.match("V\s.*", line):
                    village = Village()
                    village.parse(line)
                    village.id = village_id
                    village_id += 1
                    self.villages.append(village)
                elif re.match("^\s*$", line):
                    pass  # Empty line
                else: # Must be a shelter
                    shelter = Shelter()
                    shelter.parse(line)
                    shelter.id = shelter_id
                    shelter_id += 1
                    self.shelters.append(shelter)


