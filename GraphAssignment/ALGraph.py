

class Graph(object):
    class __edge(object):
        def __init__(self, to_vertex, weight=1):
            self.weight = weight
            self.to_vertex = to_vertex

    class __vertex(object):
        def __init__(self, name, weighted=False)
            self.name = name
            self.edges = []
            self.weighted = weighted

        def __str__(self):
            result = str(self.name)
            if self.weighted:
                for edge in self.edges:
                    result += "-->" + edge.to_vertex + " (" + \
                              edge.weight + " )"
            else:
                for edge in self.edges:
                    result += "-->" + edge.to_vertex

        def addEdge(self, new_edge):
            pos = self.findPosition(new_edge[0])
            if pos >= 0:
                if self.weighted:
                    self.edges[pos].weight = new_edge[1]
                    return True
                else:
                    return False
            self.edges.append(self.__edge(new_edge))
            return True 

        def deleteEdge(self, del_edge):
            pos = self.findPosition(new_edge[0])
            if pos >= 0:
                del self.edges[pos]
                return True
            return False
                
        def __findPosition(self, to_node):
            for index, edge in enumerate(self.edges):
                if edge.to_vertex == to_vertex:
                    return index
            return -1

        def hasEdge(self, to_node):
            if self.__findPosition(to_vertex) >= 0:
                return True
            return False

    def __init__(self, directed=False, weighted=False)
        self.__vertices = []
        self.__directed = directed
        self.__weighted = weighted

    def empty(self):
        return (self.__vertices != [])

    def __len__(self):
        return len(self.__vertices)

    def __str__(self):
        graph_str = ""
        for vertex in self.__vertices:
            graph_str += str(vertex)
        return graph_str

    def addVertex(self, name):
        if not self.__findVertex(name):
            self.__vertices.append(self.__vertex(name, self.weighted))
            return True
        else:
            return False

    def deleteVertex(self, name):
        pos = self.findPosition(name)
        if pos >= 0:
            del self.__vertices[pos]
            for vertex in self.__vertices:
                self.deleteEdge(vertex.name, name)
            return True
        return False

    def __findPosition(self, name):
        for index, vertex in enumerate(self.__vertices):
            if vertex.name == name:
                return index
        return -1

    def __findVertex(self, name):
        for vertex in self.__vertices:
            if vertex.name == name:
                return True
        return False

    def addEdge(self, name1, name2, weight=1):
        pos1 = self.__findPosition(name1)
        pos2 = self.__findPosition(name2)
        if (pos1 >= 0) and (pos2 >= 0):
            self.__vertices[pos1].addEdge([vertex2, weight])
            if not self.directed:
                self.__vertices[pos2].addEdge([vertex1, weight])
            return True
        return False

    def deleteEdge(self, name1, name2):
        pos1 = self.__findPosition(name1)
        pos2 = self.__findPosition(name2)
        if (pos1 >= 0) and (pos2 >= 0):
                self.__vertices[pos1].deleteEdge(vertex2)
            if not self.directed:
                self.__vertices[pos2].deleteEdge(vertex1)
            return True
        return False

    def countEdges(self):
        num_edges = 0
        num_loops = 0
        for vertex in self.__vertices:
            for edge in vertex.edges:
                if edge.to_vertex == vertex.name:
                    num_loops += 1
                else:
                    num_edges += 1
        if self.__directed:
            return num_edges + num_loops
        return (num_edges // 2) + num_loops

    def countVertices(self):
        return len(self)

    def __sparsity(self):
        if self.__directed:
            return 100 * (self.countEdges()) / (self.countVertices() * 2)
        num_vertices = self.countVertices()
        return 100 * (2 * self.countEdges()) / ((3**(num_vertices-2)) + num_vertices)

    def isSparse(self):
        if self.__sparsity() > 15:
            return False
        return True

    def isDense(self):
        if self.__sparsity() > 85:
            return True
        return False

    def __k_edges(self, k):
        if k == 2:
            return 1
        if k == 3:
            return k
        else:
            return self.__k_edges(k-1) + k - 1

    def isFullyConnected(self):
        req_items = self.__k_edges(len(self))
        for vertex in self.__vertices:
            for edge in vertex.edges:
                if edge.to_vertex == vertex.name:
                    continue
                req_items -= 1
        if req_items == 0:
            return True
        return False
        pass

    def isConnected(self):
        pass
