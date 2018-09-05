from __future__ import print_function
import unittest

class Graph(object):
    def __init__(self, weighted=False, directed=False):
        self.matrix = [[]]
        self.vertices = []
        self.weighted = weighted
        self.directed = directed
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
            return False
        self.vertices.append(vertex)
        self.__expand()
        return True

    def __expand(self):
        if len(self.vertices) == 1:
            self.matrix[0].append(0)
        else:
            self.matrix.append([0 for _ in range(len(self.matrix))])
            for row in self.matrix:
                row.append(0)

    # if unweighted graph, just set weights to 1
    # How can I do this?
    def deleteVertex(self, vertex):
        if vertex not in self.vertices:
            return False
        index = (self.__findIndices(vertex, vertex))[0]
        for row in self.matrix:
            row.pop(index)
        self.matrix.pop(index)
        self.vertices.pop(index)
        return True


    # Need to check if directed
    def hasEdge(self, vertex1, vertex2):
        indices = self.__findIndices(vertex1, vertex2)
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
    def addEdge(self, vertex1, vertex2, weight=1):
        indices = self.__findIndices(vertex1, vertex2)
        if -1 in indices or self.hasEdge(vertex1, vertex2):
            return False
        if not self.weighted:
            weight = 1
        if self.directed:
            self.matrix[indices[0]][indices[1]] = weight
        else:
            self.matrix[indices[0]][indices[1]] = weight
            self.matrix[indices[1]][indices[0]] = weight
        return True

    # directed and undirected
    # Check if there is an item present before deleting
    def deleteEdge(self, vertex1, vertex2):
        indices = self.__findIndices(vertex1, vertex2)
        if (-1 in indices) or (not self.hasEdge(vertex1, vertex2)):
             return False
        self.matrix[indices[0]][indices[1]] = 0
        return True

    def isSparse(self):
        if self.__sparsity() > 15:
            return False
        else:
            return True

    def __sparsity(self):
        if self.directed:
            return 100 * (self.countEdges()) / (self.countVertices() * 2)
        else:
            num_vertices = self.countVertices()
            return 100 * (2 * self.countEdges()) / ((3**(num_vertices-2)) + num_vertices)

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
        numLoops = 0
        for index1, row in enumerate(self.matrix):
            for index2, col in enumerate(row):
                if (col > 0):
                    if index1 == index2:
                        numLoops += 1
                    else:
                        numEdges += 1
        if self.directed:
            return numEdges + numLoops
        else:
            return (numEdges // 2) + numLoops
        

    # Do floyd warshall
    def isConnected(self):
        dist = self.__f_warshall()
        for row in dist:
            for col in row:
                if col == float("inf"):
                    return False
        return True

    def __f_warshall(self):
        num_vert = self.countVertices()
        distance = list(self.matrix)
        for row in distance:
            for col in row:
                if col <= 0:
                    col = float("inf")
        for index, vertex1 in enumerate(self.vertices):
            for vertex2 in self.vertices:
                if vertex1 is vertex2:
                    distance[index][index] = 0
        for k in range(1, num_vert):
            for i in range(1, num_vert):
                for j in range(1, num_vert):
                    if distance[i][j] > (distance[i][k] + distance[k][j]:
                        distance[i][j] = distance[i][k] + distance[k][j]
        return distance

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

    def test_add_three_vert(self):
        graph = Graph()
        graph.addVertex("A")
        graph.addVertex("B")
        graph.addVertex("C")
        self.assertEqual(graph.str_vertices(), "['A', 'B', 'C']")

    def test_matrix_single(self):
        graph = Graph()
        graph.addVertex("A")
        self.assertEqual(str(graph), "[[0]]")

    def test_matrix_two(self):
        graph = Graph()
        graph.addVertex("A")
        graph.addVertex("B")
        self.assertEqual(str(graph), "[[0, 0], "\
                                      "[0, 0]]")

    def test_matrix_three(self):
        graph = Graph()
        graph.addVertex("A")
        graph.addVertex("B")
        graph.addVertex("C")
        self.assertEqual(str(graph), "[[0, 0, 0], "\
                                      "[0, 0, 0], "\
                                      "[0, 0, 0]]")

    def test_delete_first_vertex(self):
        graph = Graph()
        vertices = ['A', 'B', 'C']
        for i in vertices:
            graph.addVertex(i)
        graph.deleteVertex(vertices[0])
        vertices.pop(0)
        self.assertEqual(graph.str_vertices(), str(vertices))
        self.assertEqual(str(graph), "[[0, 0], "\
                                      "[0, 0]]")

    def test_add_same_vertex(self):
        graph = Graph()
        vertex = 'A'
        graph.addVertex(vertex)
        self.assertFalse(graph.addVertex(vertex))

    def test_delete_middle_vertex(self):
        graph = Graph()
        vertices = ['A', 'B', 'C']
        for i in vertices:
            graph.addVertex(i)
        graph.deleteVertex(vertices[1])
        vertices.pop(1)
        self.assertEqual(graph.str_vertices(), str(vertices))
        self.assertEqual(str(graph), "[[0, 0], "\
                                      "[0, 0]]")

    def test_delete_last_vertex(self):
        graph = Graph()
        vertices = ['A', 'B', 'C']
        for i in vertices:
            graph.addVertex(i)
        graph.deleteVertex(vertices[2])
        vertices.pop(2)
        self.assertEqual(graph.str_vertices(), str(vertices))
        self.assertEqual(str(graph), "[[0, 0], "\
                                      "[0, 0]]")

    def test_add_single_edge_loop(self):
        graph = Graph()
        vertices = ['A', 'B', 'C']
        for i in vertices:
            graph.addVertex(i)
        graph.addEdge(vertices[1], vertices[1])
        self.assertTrue(graph.hasEdge(vertices[1], vertices[1]))
        self.assertEqual(str(graph), "[[0, 0, 0], "\
                                      "[0, 1, 0], "\
                                      "[0, 0, 0]]")

    def test_add_all_loop_edges(self):
        graph = Graph()
        vertices = ['A', 'B', 'C']
        for i in vertices:
            graph.addVertex(i)
        for i in vertices:
            graph.addEdge(i, i)
            self.assertTrue(graph.hasEdge(i, i))
        self.assertEqual(str(graph), "[[1, 0, 0], "\
                                      "[0, 1, 0], "\
                                      "[0, 0, 1]]")

    def test_add_all_but_loop_edges(self):
        #default is weighted
        graph = Graph()
        vertices = ['A', 'B', 'C']
        for i in vertices:
            graph.addVertex(i)
        for vertex1 in vertices:
            for vertex2 in vertices:
                if (vertex1 is vertex2) or graph.hasEdge(vertex1, vertex2) or \
                                           graph.hasEdge(vertex2, vertex1):
                    continue
                else:
                    graph.addEdge(vertex1, vertex2)
                    self.assertTrue(graph.hasEdge(vertex1, vertex2))
                    self.assertTrue(graph.hasEdge(vertex2, vertex1))
        self.assertEqual(str(graph), "[[0, 1, 1], "\
                                      "[1, 0, 1], "\
                                      "[1, 1, 0]]")

    def test_add_all_edges(self):
        graph = Graph()
        vertices = ['A', 'B', 'C']
        for i in vertices:
            graph.addVertex(i)
        for vertex1 in vertices:
            for vertex2 in vertices:
                if graph.hasEdge(vertex1, vertex2) or graph.hasEdge(vertex1, vertex2):
                    continue
                else:
                    graph.addEdge(vertex1, vertex2)
                    self.assertTrue(graph.hasEdge(vertex1, vertex2))
                    self.assertTrue(graph.hasEdge(vertex2, vertex1))
        self.assertEqual(str(graph), "[[1, 1, 1], "\
                                     "[1, 1, 1], "\
                                     "[1, 1, 1]]")

    def test_add_edge_twice(self):
        graph = Graph()
        vertices = ['A', 'B', 'C']
        for i in vertices:
            graph.addVertex(i)
        graph.addEdge(vertices[0], vertices[1])
        self.assertFalse(graph.addEdge(vertices[0], vertices[1]))
        self.assertFalse(graph.addEdge(vertices[1], vertices[0]))

    def test_count_vertices(self):
        graph = Graph()
        vertices = ['A', 'B', 'C']
        for i in vertices:
            graph.addVertex(i)
        self.assertEqual(graph.countVertices(), len(vertices))

    def test_count_edges_one(self):
        graph = Graph()
        vertices = ['A', 'B', 'C']
        for i in vertices:
            graph.addVertex(i)
        graph.addEdge(vertices[1], vertices[1])
        self.assertEqual(graph.countEdges(), 1)

    def test_count_edges_undirected_one(self):
        graph = Graph()
        vertices = ['A', 'B', 'C']
        for i in vertices:
            graph.addVertex(i)
        graph.addEdge(vertices[0], vertices[1])
        self.assertEqual(graph.countEdges(), 1)

    def test_count_edges_directed_two(self):
        graph = Graph()
        vertices = ['A', 'B', 'C']
        for i in vertices:
            graph.addVertex(i)
        graph.addEdge(vertices[0], vertices[1])
        graph.addEdge(vertices[1], vertices[2])
        self.assertEqual(graph.countEdges(), 2)

    def test_count_edges_full_graph(self):
        graph = Graph()
        vertices = ['A', 'B', 'C']
        for i in vertices:
            graph.addVertex(i)
        for vertex1 in vertices:
            for vertex2 in vertices:
                if graph.hasEdge(vertex1, vertex2) or graph.hasEdge(vertex1, vertex2):
                    continue
                else:
                    graph.addEdge(vertex1, vertex2)
                    self.assertTrue(graph.hasEdge(vertex1, vertex2))
                    self.assertTrue(graph.hasEdge(vertex2, vertex1))
        #Number of edges possible in simple, undirected graph if nodes > 1
        num_edges = 3**(len(vertices)-2) + len(vertices)
        self.assertEqual(graph.countEdges(), num_edges)

    def test_sparsity_false(self):
        graph = Graph()
        vertices = ['A', 'B', 'C']
        for i in vertices:
            graph.addVertex(i)
        graph.addEdge(vertices[0], vertices[0])
        self.assertFalse(graph.isSparse())

    def test_sparsity_true(self):
        graph = Graph(directed=True)
        vertices = ['A', 'B', 'C', 'D']
        for i in vertices:
            graph.addVertex(i)
        graph.addEdge(vertices[0], vertices[0])
        self.assertTrue(graph.isSparse())

    def test_density_false(self):
        graph = Graph(directed=True)
        vertices = ['A', 'B', 'C']
        for i in vertices:
            graph.addVertex(i)
            graph.addEdge(i, i)
        self.assertFalse(graph.isDense())

    def test_density_true(self):
        graph = Graph()
        vertices = ['A', 'B', 'C']
        for i in vertices:
            graph.addVertex(i)
            graph.addEdge(i, i)
        self.assertTrue(graph.isDense())

    def test_density_one_vert_edge(self):
        graph = Graph()
        graph.addVertex('A')
        graph.addEdge('A', 'A')
        self.assertTrue(graph.isDense())

    def test_sparsity_one_vert(self):
        graph = Graph()
        graph.addVertex('A')
        self.assertTrue(graph.isSparse())

    def test_connected_false(self):
        ####
        pass
