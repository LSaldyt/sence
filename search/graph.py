def to_obstacles(mazeString):
    lists = [[c != '.' for c in row] for row in mazeString.split('\n') if len(row) > 0]

    obstacles = []
    for x, row in enumerate(lists):
        for y, b in enumerate(row):
            if b:
                obstacles.append((x, y))
    return obstacles

class Graph(object):
    def __init__(self, height=0, width=0, obstructions=[]):
        self.height = height
        self.width  = width
        self.obstructions = obstructions
        self.points = {(x, y) : self.get_adjacent((x, y), None) for x in range(width) for y in range(height)}

    def get_adjacent(self, point, end):
        (x, y) = point
        return [p for p in [(x+1, y), (x-1, y), (x, y+1), (x, y-1)] if self.within(p) and p not in self.obstructions]

    def within(self, p):
        return p[0] < self.height and p[0] >= 0 and p[1] < self.width and p[1] >= 0

    def show(self, path=None):
        if path is None:
            path = []
        for y in range(self.height):
            print()
            for x in range(self.width):
                if (x, y) in self.points and (x, y) not in self.obstructions:
                    if (x, y) in path:
                        print("*", end="")
                    else:
                        print(".", end="")
                else:
                    print ("O", end="")


