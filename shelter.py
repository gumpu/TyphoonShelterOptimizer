class Shelter(object):
    def __init__(self):
        self.position = (0.0, 0.0)
        self.capacity = 0
        self.used     = 0
        self.cost     = 0.0
        self.id       = 0

    def __str__(self):
        return "{}  {} cap: {} cost: {} {}".format(
                self.id,
                self.position, self.capacity, self.cost,
                self.used)

    def parse(self, line):
        parts = line.split()
        # parts[0] == 'S'
        self.position = (float(parts[1]), float(parts[2]))
        self.capacity = int(parts[3])
        self.cost     = float(parts[4])

    def capacity_left(self):
        """How many villages can this shelter still accomodate"""
        return self.capacity - self.used

