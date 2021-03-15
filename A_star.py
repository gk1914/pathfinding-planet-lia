from my_priority import MyPQ
from my_priority import MyPQElement


class AStar(object):

    def __init__(self, m, start, end, s=None):
        self.map = m
        self.goal = end
        self.opened = MyPQ()
        self.opened.push(MyPQElement(0, start, []))
        self.closed = []
        self.state = s

    def __call__(self):
        # Repeat until goal/target is found
        while True:
            curr = self.opened.pop()
            self.closed.append(curr)

            if curr.element.X == self.goal.X and curr.element.Y == self.goal.Y:
                return curr.element

            neighbours = curr.element.neighbours()
            for n in neighbours:
                if n in self.closed:
                    continue
                # f = g + h
                f = len(curr.history) + 1 + n.evaluate(self.goal)
                if n not in self.opened:
                    n.set_parent(curr.element)
                    self.opened.push(MyPQElement(f, n, curr.history + [curr.element]))
                else:
                    # find coresponding PQElement
                    pq_el = self.opened.find(n.id)
                    # check if f (new priority) is smaller than PQElement's existing priority
                    if f < pq_el.priority:
                        # update PQElement
                        self.opened.update(pq_el, f)
