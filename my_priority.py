class Tile(object):

    def __init__(self, m, x, y, p=None):
        self.map = m
        self.id = (x, y)
        self.X = x
        self.Y = y
        self.parent = p

    def __eq__(self, other):
        return self.id[0] == other.element.id[0] and self.id[1] == other.element.id[1]

    def is_same(self, other):
        return self.id[0] == other.id[0] and self.id[1] == other.id[1]

    def __str__(self):
        return str(self.id)

    def neighbours(self):
        n = []
        # LEFT
        if self.X - 1 >= 0 and self.map[self.Y][self.X - 1]:
            n.append(Tile(self.map, self.X - 1, self.Y))
        # RIGHT
        if self.X + 1 < len(self.map[0]) and self.map[self.Y][self.X + 1]:
            n.append(Tile(self.map, self.X + 1, self.Y))
        # UP
        if self.Y + 1 < len(self.map) and self.map[self.Y + 1][self.X]:
            n.append(Tile(self.map, self.X, self.Y + 1))
        # DOWN
        if self.Y - 1 >= 0 and self.map[self.Y - 1][self.X]:
            n.append(Tile(self.map, self.X, self.Y - 1))
        return n

    # Manhattan distance HEURISTIC
    def evaluate(self, target):
        return abs(self.X - target.X) + abs(self.Y - target.Y)

    def set_parent(self, p):
        self.parent = p


class MyPQElement(object):

    def __init__(self, p, el, prev):
        self.priority = p
        self.element = el
        self.history = prev

    def __lt__(self, other):
        return self.priority < other.priority

    def __str__(self):
        return str(self.element) + " [priority = " + str(self.priority) + "]"

    def set_priority(self, new_priority):
        self.priority = new_priority


class MyPQ(object):

    def __init__(self):
        self.queue = []

    def __str__(self):
        return str([str(e) for e in self.queue])

    def __contains__(self, item):
        return item in self.queue

    def push(self, new_item):
        i = 0
        for item in self.queue:
            if item.priority > new_item.priority:
                break
            i += 1
        self.queue = self.queue[:i] + [new_item] + self.queue[i:]

    def pop(self):
        popped = self.queue[0]
        self.queue = self.queue[1:]
        return popped

    def find(self, id):
        i = 0
        for item in self.queue:
            if item.element.id == id:
                break
            i += 1
        return self.queue[i]

    def remove(self, id):
        i = 0
        for item in self.queue:
            if item.element.id == id:
                break
            i += 1
        removed = self.queue[i]
        self.queue = self.queue[:i] + self.queue[i+1:]
        return removed

    def update(self, item, new_priority):
        temp = self.remove(item.element.id)
        temp.set_priority(new_priority)
        self.push(temp)
