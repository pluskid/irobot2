from .basic   import Action
from .compose import SequenceAction
from ..util   import vec2d

class AcPathTo(Action):
    def __init__(self, robot, dest):
        Action.__init__(self, robot)
        

class Node(object):
    def __init__(self, pos, parent, G, end):
        self.pos = pos
        self.parent = parent
        self.G = G
        self.H = abs(pos[0]-end[0])+abs(pos[1]-end[1])

        print 'Node (%s): G=%d, H=%d' % (self.pos, G, self.H)

    @property
    def F(self):
        return self.G+10*self.H

def find_path(map, src, dest):
    start = map.pixel2tile(src)
    end   = map.pixel2tile(dest)

    close_nodes = set()
    open_nodes = {start: Node(start, None, 0, end)}

    incs = [((1, -1), 14), ((1, 0), 10), ((1, 1), 14),
            ((0, -1), 10), ((0, 1), 10), ((-1, -1), 14),
            ((-1, 0), 10), ((-1, 1), 14)]
    node = None

    while True:
        if len(open_nodes) == 0:
            break
        bestk = None; bestF = float('inf')
        for k in open_nodes.iterkeys():
            F = open_nodes[k].F
            if F < bestF:
                bestF = F
                bestk = k
        node = open_nodes[bestk]
        del open_nodes[bestk]
        close_nodes.add(node.pos)
        if node == end:
            break

        for inc in incs:
            new_pos = (node.pos[0] + inc[0][0], node.pos[1]+inc[0][1])
            if new_pos in close_nodes:
                continue
            if map.is_obstacle(new_pos):
                print 'obstacle: %s (%s)' % (inc, new_pos)
                continue
            new_G = node.G + inc[1]
            new_node = open_nodes.get(new_pos)
            if new_node is not None:
                if new_node.G > new_G:
                    new_node.G = new_G
                    new_node.parent = node
            else:
                new_node = Node(new_pos, node, new_G, end)
                open_nodes[new_pos] = new_node
    path = []
    while node is not None:
        path.append(map.tile2pixel(node.pos, center=True))
        node = node.parent
    path.reverse()
    if map.tile2pixel(start, center=True) != (src[0], src[1]):
        path.insert(0, (src[0], src[1]))
    if map.tile2pixel(end, center=True) != (dest[0], dest[1]):
        path.append((dest[0], dest[1]))
    return path

