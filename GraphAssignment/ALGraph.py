import unittest

class Graph(object):
    class __edge(object):
        def __init__(self, to_vertex, weight=1):
            self.weight = weight
            self.to_vertex = to_vertex


    class __vertex(object):
        def __init__(self, name, weighted=False):
            self.name = name
            self.edges = []
            self.weighted = weighted

        def __str__(self):
            result = str(self.name)
            if self.weighted:
                for edge in self.edges:
                    result += "-->" + str(edge.to_vertex.name) + " (" + \
                              str(edge.weight) + " )"
            else:
                for edge in self.edges:
                    result += "-->" + str(edge.to_vertex.name)
            return result

        def addEdge(self, new_edge):
            edge = self.__findEdge(new_edge.to_vertex)
            if edge != None:
                if self.weighted:
                    edge = new_edge
                    return True
                else:
                    return False
            self.edges.append(new_edge)
            return True 

        def deleteEdge(self, del_edge):
            edge = self.__findEdge(del_edge)
            if edge != None:
                self.edges.remove(edge)
                return True
            return False
                
        def __findEdge(self, to_vertex):
            for edge in self.edges:
                if edge.to_vertex == to_vertex:
                    return edge
            return None


    def __init__(self, directed=False, weighted=False, filename=""):
        self.__vertices = []
        self.__directed = directed
        self.__weighted = weighted
        self.__filename = filename

    def empty(self):
        return (self.__vertices == [])

    def __len__(self):
        return len(self.__vertices)

    def __str__(self):
        graph_str = ""
        for vertex in self.__vertices:
            graph_str += str(vertex) + "\n"
        return graph_str

    def __iter__(self):
        return iter(self.__vertices)

    def addVertex(self, name):
        if not self.__findVertex(name):
            self.__vertices.append(self.__vertex(name, self.__weighted))
            return True
        else:
            return False

    def deleteVertex(self, name):
        vertex1 = self.__findVertex(name)
        if vertex1 != None:
            for vertex in self.__vertices:
                if vertex == vertex1:
                    continue
                self.deleteEdge(vertex.name, vertex1.name)
            self.__vertices.remove(vertex1)
            return True
        return False

        pos = self.__findPosition(name)
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
        vertex1 = self.__findVertex(name1)
        vertex2 = self.__findVertex(name2)
        if (None != vertex1) and (None != vertex2):
            vertex1.addEdge(self.__edge(vertex2, weight))
            if (not self.__directed) and (name1 != name2):
                vertex2.addEdge(self.__edge(vertex1, weight))
            return True
        return False

    def __findVertex(self, name):
        for vertex in self.__vertices:
            if vertex.name == name:
                return vertex
        return None

    def deleteEdge(self, name1, name2):
        vertex1 = self.__findVertex(name1)
        vertex2 = self.__findVertex(name2)
        if (vertex1 != None) and (vertex2 != None):
            ret_val = vertex1.deleteEdge(vertex2)
            if (not self.__directed) and (vertex1 != vertex2):
                ret_val = vertex2.deleteEdge(vertex1)
            return ret_val
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

    def printGraph(self):
        pass

    def readGraph(self):
        pass



##############################################
################ Unit Testing ################
##############################################

class TestBasicFunction(unittest.TestCase):
    def test_empty_graph(self):
        self.assertTrue(Graph().empty())

    def test_add_one_vertex(self):
        graph = Graph()
        graph.addVertex('A')
        self.assertFalse(graph.empty())
        self.assertEqual(len(graph), 1)
        self.assertEqual(str(graph), 'A\n')

    def test_add_two_vertices(self):
        graph = Graph()
        graph.addVertex('A')
        graph.addVertex('B')
        self.assertEqual(len(graph), 2)
        self.assertEqual(str(graph), 'A\nB\n')

    def test_add_vertex_twice(self):
        graph = Graph()
        self.assertTrue(graph.addVertex('A'))
        self.assertFalse(graph.addVertex('A'))
        self.assertEqual(len(graph), 1)

    def test_add_seven_vertices(self):
        vertices = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
        str_graph = ""
        graph = Graph()
        for vertex in vertices:
            graph.addVertex(vertex)
            str_graph += vertex + "\n"
        self.assertEqual(len(graph), len(vertices))
        self.assertEqual(str(graph), str_graph)

    def test_delete_solo_vertex(self):
        graph = Graph()
        graph.addVertex('A')
        self.assertFalse(graph.empty())
        self.assertTrue(graph.deleteVertex('A'))
        self.assertEqual(len(graph), 0)
        self.assertEqual(str(graph), "")

    def test_delete_vertex_of_two(self):
        graph = Graph()
        graph.addVertex('A')
        graph.addVertex('B')
        self.assertTrue(graph.deleteVertex('A'))
        self.assertEqual(len(graph), 1)
        self.assertEqual(str(graph), "B\n")

    def test_add_edge_to_single_vertex(self):
        graph = Graph()
        graph.addVertex('A')
        self.assertTrue(graph.addEdge('A', 'A'))
        self.assertEqual(str(graph), 'A-->A\n')

    def test_delete_edge_from_single_vertex_true(self):
        graph = Graph()
        graph.addVertex('A')
        self.assertTrue(graph.addEdge('A', 'A'))
        self.assertTrue(graph.deleteEdge('A', 'A'))
        self.assertEqual(str(graph), 'A\n')

    def test_delete_edge_from_single_vertex_false(self):
        graph = Graph()
        graph.addVertex('A')
        self.assertFalse(graph.deleteEdge('A', 'A'))

    def test_add_edge_two_vertices(self):
        graph = Graph()
        vertices = ['A', 'B']
        for vertex in vertices:
            graph.addVertex(vertex)
        self.assertTrue(graph.addEdge('A', 'B'))
        self.assertEqual(str(graph), 'A-->B\nB-->A\n')

    def test_delete_edge_two_vertices(self):
        graph = Graph()
        vertices = ['A', 'B']
        for vertex in vertices:
            graph.addVertex(vertex)
        graph.addEdge(vertices[0], vertices[1])
        self.assertTrue(graph.deleteEdge(vertices[0], vertices[1]))
        self.assertEqual(str(graph), 'A\nB\n')

    def test_add_all_possible_edges_three_vertices(self):
        graph = Graph()
        vertices = ['A', 'B', 'C']
        for vertex in vertices:
            graph.addVertex(vertex)
        for vertex1 in vertices:
            for vertex2 in vertices:
                graph.addEdge(vertex1, vertex2)
        self.assertEqual(str(graph), 'A-->A-->B-->C\nB-->A-->B-->C\nC-->A-->B-->C\n')
