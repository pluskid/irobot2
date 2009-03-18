from .basic   import Action
from .compose import SequenceAction
from .move    import AcMoveTo
from ..util   import vec2d

class AcPathTo(Action):
    def __init__(self, robot, dest):
        Action.__init__(self, robot)
        path = find_path(robot['k.god']._engine.map, 
                         robot['k.position'],
                         dest)
        actions = []
        node_start = path[0]
        xinc = path[1][0]-path[0][0]
        yinc = path[1][1]-path[0][1]
        for i in range(2, len(path)):
            node = path[i]
            node_prev = path[i-1]
            if node[0]-node_prev[0] == xinc and \
               node[1]-node_prev[1] == yinc:
                continue
            actions.append(AcMoveTo(robot, vec2d(node_prev)))
            node_start = node_prev
            xinc = node[0]-node_prev[0]
            yinc = node[1]-node_prev[1]
        actions.append(AcMoveTo(robot, vec2d(path[-1])))
        self._action = SequenceAction(robot, actions)

    def update(self, god, intv):
        return self._action.update(god, intv)

class Node(object):
    def __init__(self, pos, parent, G, end):
        self.pos = pos
        self.parent = parent
        self.G = G
        self.H = abs(pos[0]-end[0])+abs(pos[1]-end[1])

    @property
    def F(self):
        return self.G+10*self.H

def find_path(map, src, dest):
    def get_moves(pos):
        moves = []
        for xinc, yinc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_pos = (pos[0]+xinc,pos[1]+yinc)
            if not map.is_obstacle(new_pos):
                moves.append((new_pos, 10))
        for xinc in (-1, 1):
            for yinc in (-1, 1):
                if map.is_obstacle((pos[0]+xinc,pos[1]+yinc)) or \
                   map.is_obstacle((pos[0], pos[1]+yinc)) or \
                   map.is_obstacle((pos[0]+xinc, pos[1])):
                    continue
                moves.append(((pos[0]+xinc,pos[1]+yinc), 14))
        return moves

    start = map.pixel2tile(src)
    end   = map.pixel2tile(dest)

    close_nodes = set()
    open_nodes = {start: Node(start, None, 0, end)}

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
        if node.pos == end:
            break

        for new_pos, cost in get_moves(node.pos):
            if new_pos in close_nodes:
                continue
            new_G = node.G + cost
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

