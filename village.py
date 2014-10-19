#
class Village(object):
    def __init__(self):
        self.demand = 0
        self.id     = 0
        self.cx     = 0.0
        self.cy     = 0.0

    def __str__(self):
        return str(self.demand) + " : " + str(self.cx) + "," + str(self.cy)

    def parse(self, line):
        parts = line.split()
        # parts[0] == 'V'
        self.demand = int(parts[-1])
        self.cx     = float(parts[1])
        self.cy     = float(parts[2])
        # For now we do not split village population over
        # different shelters.
        assert(self.demand == 1)

