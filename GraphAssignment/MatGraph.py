from __future__ import print_function
import unittest

class Graph(object):
    def __init__(self):
        self.matrix = [[]]
        self.vertices = []
        self.weighted = False
        self.directed = False
        self.edgeAdd = False
        self.matrixFilled = False

    def empty(self):
        return (len(self.vertices) == 0)

    def __str__(self):
        return str(self.matrix)

    def str_vertices(self):
        return str(self.vertices)

    def addVertex(self, vertex):
        if vertex in self.vertices:
            raise RuntimeError("Vertex already exists in graph")
        self.vertices.append(vertex)
        if len(self.vertices) == 0:
            self.matrix[0].append([])
        else:
            self.__expand()

    def __expand(self):
        if len(self.vertices) == 0:
            self.matrix[0].append(0)
        else:
            self.matrix.append([0 for _ in range(len(self.matrix) - 1)])
            for row in self.matrix:
                row.append(0)

    # if unweighted graph, just set weights to 1
    # How can I do this?
    def deleteVertex(self, vertex):
        pass

    # Need to check if directed
    def hasEdge(self, vertex1, vertex2):
        indices = self.__findIndices(vertex1, vertex2)
        if weighted:
            if len(self.matrix[indices[0]][indices[1]]) > 0:
                return True
            else:
                return False
        else:
            if self.matrix[indices[0]][indices[1]] == 0:
                return False
            else:
                return True


    def __findIndices(self, vertex1, vertex2):
        index = 0
        indices = [-1, -1]
        for vertex in self.vertices:
            if vertex1 in vertex:
                indices[0] = index
            if vertex2 in vertex:
                indices[1] = index
            index += 1
        if -1 in indices:
            raise RuntimeError("Given vertex pair is invalid/does not exist")
        return indices


    # Check if edge already exists before adding (specs seem to not allow for multiple edges)
    # Check if directed or undirected (undirected should have mirrored matrix)
    def addEdge(self, vertex1, vertex2, weight=None):
        indices = self.__findIndices(vertex1, vertex2)
        if self.weighted:
            self.matrix[indices[0]][indices[1]].append(weight)
        else:
            self.matrix[indices[0]][indices[1]] += 1
        return True

    # Check if there is an item present before deleting
    def deleteEdge(self, vertex1, vertex2):
        indices = self.__findIndices(vertex1, vertex2)
        if self.weighted:
            self.matrix[indices[0]][indices[1]].clear()
        else:
            self.matrix[indices[0]][indices[1]] = 0
        return True

    def isSparse(self):
        numEdges = 0
        if weighted:
            for row in self.matrices:
                for col in row:
                    if len(col) > 0:
                        numEdges += 1
        else:
            for row in self.matrices:
                for col in row:
                    if col > 0:
                        numEdges += 1

        if self.__sparsity() > 15:
            return False
        else:
            return True

    def __sparsity(self):
        if self.directed:
            return 100 * (self.countEdges()) / (self.countVertices() * (self.countVertices() - 1))
        else:
            return 100 * (2 * self.countEdges()) / (self.countVertices() * (self.countVertices() - 1))

    def isDense(self):
        if self.__sparsity() > 85:
            return True
        else:
            return False

    def countVertices(self):
        return len(self.vertices)
        pass

    def countEdges(self):
        numEdges = 0 
        if self.weighted:
            for row in self.matrices:
                for col in row:
                    if len(col) > 0:
                        numEdges += 1
        else:
            for row in self.matrices:
                for col in row:
                    if col > 0:
                        numEdges += 1
        if self.directed:
            return numEdges
        else:
            return (numEdges / 2)
        

    # Do floyd warshall
    def isConnected(self):
        dist = []
        pass

    # Also floyd warshall?
    def isFullyConnected(self):
        pass

    def __kEdges(self, k):
        if k == 2:
            return k
        elif k == 3:
            return k
        else:
            return self.__edges(k-1) + k - 1

    # Read the file--maybe take command line args?
    def readGraph(self):
        pass

    # Print out similar output to input
    def printGraph(self):
        pass


class TestBasicFunction(unittest.TestCase):
    def test_empty_graph(self):
        self.assertTrue(Graph().empty())

    def test_add_one_vert(self):
        graph = Graph()
        graph.addVertex("A")
        self.assertFalse(graph.empty())
        self.assertEqual(graph.str_vertices(), "['A']")

    def test_add_two_vert(self):
        graph = Graph()
        graph.addVertex("A")
        graph.addVertex("B")
        self.assertEqual(graph.str_vertices(), "['A', 'B']")

    def test_matrix_single(self):
        graph = Graph()
        graph.addVertex("A")
        self.assertEqual(str(graph), "[[0]]")

