class Vertex:
    __slots__ = 'element'

    def __init__(self, x):
        self.element = x

    def __hash__(self):
        return hash(id(self))

    def __str__(self):
        return 'element: {0}'.format(self.element)

    def __repr__(self):
        return 'element: {0}'.format(self.element)


class Edge:
    __slots__ = 'origin', 'destination', 'element'

    def __init__(self, u, v, x):
        self.origin = u
        self.destination = v
        self.element = x

    def endpoints(self):
        return self.origin, self.destination

    def opposite(self, v):
        return self.destination if v is self.origin else self.origin

    def __hash__(self):
        return hash((self.origin, self.destination))


class Graph:
    def __init__(self, directed=False):
        self.outgoing = {}
        self.incoming = {} if directed else self.outgoing

    def is_directed(self):
        return self.incoming is not self.outgoing

    def vertex_count(self):
        return len(self.outgoing)

    def vertices(self):
        return self.outgoing.keys()

    def edge_count(self):
        total = sum(len(self.outgoing[v]) for v in self.outgoing)
        return total if self.is_directed() else total // 2

    def edges(self):
        result = set()
        for secondary_map in self.outgoing.values():
            result.update(secondary_map.values())
        return result

    def get_edge(self, u, v):
        return self.outgoing[u].get(v)

    def degree(self, v, outgoing=True):
        adj = self.outgoing if outgoing else self.incoming
        return len(adj[v])

    def incident_edges(self, v, outgoing=True):
        adj = self.outgoing if outgoing else self.incoming
        for edge in adj[v].values():
            yield edge

    def insert_vertex(self, x=None):
        v = Vertex(x)
        self.outgoing[v] = {}
        if self.is_directed():
            self.incoming[v] = {}
        return v

    def insert_edge(self, u, v, x=None):
        e = Edge(u, v, x)
        self.outgoing[u][v] = e
        self.incoming[v][u] = e
