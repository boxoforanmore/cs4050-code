from __future__ import print_function
from sys import argv
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
            edge = self.findEdge(new_edge.to_vertex)
            if edge != None:
                if self.weighted:
                    edge = new_edge
                    return True
                else:
                    return False
            self.edges.append(new_edge)
            return True 

        def deleteEdge(self, del_edge):
            edge = self.findEdge(del_edge)
            if edge != None:
                self.edges.remove(edge)
                return True
            return False
                
        def findEdge(self, to_vertex):
            for edge in self.edges:
                if edge.to_vertex == to_vertex:
                    return edge
            return None


    def __init__(self, directed=False, weighted=False, filename=""):
        self.__vertices = []
        self.__directed = directed
        self.__weighted = weighted
        self.__filename = filename
        self.__visited = dict()

        if filename != "":
            self.readGraph(self.__filename)

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
            if self.hasEdge(name1, name2) and not self.__weighted:
                return False
            vertex1.addEdge(self.__edge(vertex2, weight))
            if (not self.__directed) and (name1 != name2):
                if self.hasEdge(name2, name1) and not self.__weighted:
                    return False
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
                if edge.to_vertex == vertex:
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

    def hasEdge(self, name1, name2):
        vertex1 = self.__findVertex(name1)
        vertex2 = self.__findVertex(name2)
        if (vertex1 != None) and (vertex2 != None):
            if vertex1.findEdge(vertex2) != None:
                return True
        return False

    def isFullyConnected(self):
        req_items = 2 * self.__k_edges(len(self))
        for vertex in self.__vertices:
            for edge in vertex.edges:
                if edge.to_vertex == vertex:
                    continue
                else: 
                    req_items -= 1
        if req_items == 0:
            return True
        return False

    def isConnected(self):
        self.__visited = dict()
        for vertex in self.__vertices:
            self.__visited[vertex] = 0
        for vertex1 in self.__vertices:
            for vertex2 in self.__vertices:
                if self.__find_path(vertex1, vertex2) != None:
                    self.__visited[vertex1] += 1
        num_paths = 0
        for vertex1 in self.__vertices:
            if self.__visited[vertex1] >= (len(self.__vertices) - 1):
                num_paths += 1
        return num_paths == len(self.__vertices)

    def __find_path(self, start_vertex, end_vertex, path=None):
        if path == None:
            path = []
        path.append(start_vertex)
        if start_vertex == end_vertex:
            return path
        for edge in start_vertex.edges:
            if edge.to_vertex not in path:
                extended_path = self.__find_path(edge.to_vertex, end_vertex, path)
                if extended_path:
                    return extended_path
        return None

    def __findEdges(self):
        edges = []
        weights = []
        for index, vertex in enumerate(self.__vertices):
            for edge in vertex.edges:
                temp = set()
                temp.add(vertex.name)
                temp.add(edge.to_vertex.name)
                if temp not in edges:
                    edges.append(temp)
                    if self.__weighted:
                        weights.append(edge.weight)
        final = []
        if len(edges) == len(weights):
            for index, edge in enumerate(edges):
                temp = ""
                for item in edge:
                    temp += item + " "
                temp += weights[index] + "\n"
                final.append(temp)
        else:
            for index, edge in enumerate(edges):
                temp = ""
                for item in edge:
                    temp += item + " "
                temp += "\n"
                final.append(temp)
        return final

    def printGraph(self):
        vertices = ""
        edges = self.__findEdges()
        weighted = "unweighted"
        directed = "undirected"
        for vertex in self.__vertices:
            vertices += vertex.name + " "
        if self.__weighted:
            weighted = "weighted"
        if self.__directed:
            directed = "directed"
        final_print = weighted + "\n" + directed + "\n" + \
                      "begin\n" + vertices + "\n"
        for edge in edges:
            final_print += edge
        final_print += "end\n"
        print(final_print)
        return True

    def readGraph(self, filename):
        begin_token = False
        end_token = False
        vertices_token = False
        actual_result = False
        error_token = False
        with open(filename) as inputFile:
            for line in inputFile:
                if not begin_token:
                    if "unweighted" in line:
                        self.__weighted = False
                    elif "weighted" in line:
                        self.__weighted = True
                    elif "undirected" in line:
                        self.__directed = False
                    elif "directed" in line:
                        self.__directed = True
                    elif "begin" in line:
                        begin_token = True
                    else:
                        print(line.rstrip())
                        continue
                    print()
                    print(line.rstrip())
                else:
                    if not vertices_token:
                        vertices_token = True
                        print()
                        print(f"Adding vertices {[line.rstrip()]}from file '{filename}'")
                        for item in line.rstrip().split():
                            print(f"Adding vertex '{item}' to graph...")
                            actual_result = self.addVertex(str(item))
                            if actual_result:
                                print(f"{actual_result} : vertex '{item}' added to graph\n")
                            else:
                                print(f"{actual_result} : vertex '{item}' not added to graph\n")
                        print(f"Finished adding vertices from file '{filename}'\n")
                    elif not end_token:
                        if "end" in line.rstrip():
                            print(f"Finished adding edges from file '{filename}'\n")
                            print(line.rstrip(),"\n\n")
                            end_token = True
                        else:
                            edges = line.rstrip().split()
                            if not self.__weighted:
                                print(f"Adding edge '{edges[0]}  {edges[1]}' to graph")
                                actual_result = self.addEdge(edges[0], edges[1])
                            else:
                                print(f"Adding edge '{edges[0]} {edges[1]} {edges[2]}' to graph")
                                actual_result = self.addEdge(edges[0], edges[1], edges[2])
                            if actual_result:
                                if self.__weighted:
                                    print(f"{actual_result} : edge '{edges[0]} {edges[1]} {edges[2]}' added to graph\n")
                                else:
                                    print(f"{actual_result} : edge '{edges[0]} {edges[1]}' added to graph\n")
                            else:
                                if self.__weighted:
                                    print(f"{actual_result} : edge '{edges[0]} {edges[1]} {edges[2]}' not added to graph\n")
                                else:
                                    print(f"{actual_result} : edge '{edges[0]} {edges[1]}' not added to graph\n")
                    else:
                        if str(actual_result) == line.capitalize().rstrip():
                            print("PASSED:")
                            print(f"Expected Result: {line.capitalize().rstrip()}")
                            print(f"Actual Result:   {actual_result}\n\n")
                        elif str(not actual_result) == line.capitalize().rstrip():
                            print("FAILED:")
                            print(f"Expected Result: {line.capitalize().rstrip()}")
                            print(f"Actual Result:   {actual_result}\n\n")
                            error_token = True
                        else:
                            actual_result = self.__functions(str(line.rstrip()))
        print("Final Graph:")
        self.printGraph()
        print()
        if not error_token:
            print("OVERALL RESULTS:      SUCCESS")
        else:
            print("OVERALL RESULTS:      FAIL")

    def __functions(self, line):
        print(f"TESTING: {line}")
        if "isSparse" in line:
            return self.isSparse()
        elif "isDense" in line:
            return self.isDense()
        elif "countVertices" in line:
            return self.countVertices()
        elif "countEdges" in line:
            return self.countEdges()
        elif "isConnected" in line:
            return self.isConnected()
        elif "isFullyConnected" in line:
            return self.isFullyConnected()
        elif "printGraph" in line:
            return self.printGraph()
        else:
            line_split = line.split()
            if "hasEdge" in line:
                return self.hasEdge(line_split[1], line_split[2])
            elif "addEdge" in line:
                if self.__weighted:
                    return self.addEdge(line_split[1], line_split[2], line_split[3])
                return self.addEdge(line_split[1], line_split[2])
            elif "deleteEdge" in line:
                return self.deleteEdge(line_split[1], line_split[2])
            elif "addVertex" in line:
                return self.addVertex(line_split[1])
            elif "deleteVertex" in line:
                return self.deleteVertex(line_split[1])    
 



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

    def test_add_edge_twice(self):
        graph = Graph()
        graph.addVertex('A')
        graph.addVertex('B')
        self.assertTrue(graph.addEdge('A', 'B'))
        self.assertFalse(graph.addEdge('A', 'B'))

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

    def test_add_all_edges_delete_one(self):
        graph = Graph()
        vertices = ['A', 'B', 'C']
        for vertex in vertices:
            graph.addVertex(vertex)
        for vertex1 in vertices:
            for vertex2 in vertices:
                graph.addEdge(vertex1, vertex2)
        self.assertTrue(graph.deleteEdge(vertices[0], vertices[2]))
        self.assertEqual(str(graph), 'A-->A-->B\nB-->A-->B-->C\nC-->B-->C\n')

    def test_add_all_edges_delete_vertex(self):
        graph = Graph()
        vertices = ['A', 'B', 'C']
        for vertex in vertices:
            graph.addVertex(vertex)
        for vertex1 in vertices:
            for vertex2 in vertices:
                graph.addEdge(vertex1, vertex2)
        self.assertTrue(graph.deleteVertex(vertices[1]))
        self.assertEqual(str(graph), 'A-->A-->C\nC-->A-->C\n')

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

    def test_connected_undirected_false(self):
        graph = Graph()
        vertices = ['A', 'B', 'C', 'D']
        for i in vertices:
            graph.addVertex(i)
        graph.addEdge(vertices[0], vertices[1])
        graph.addEdge(vertices[2], vertices[3])
        self.assertFalse(graph.isConnected())

    def test_connected_directed_false(self):
        graph = Graph(directed=True)
        vertices = ['A', 'B', 'C', 'D']
        for i in vertices:
            graph.addVertex(i)
        for i in range(len(vertices) - 1):
            graph.addEdge(vertices[i], vertices[i+1])
        self.assertFalse(graph.isConnected())

    def test_connected_undirected_true(self):
        graph = Graph()
        vertices = ['A', 'B', 'C', 'D']
        for i in vertices:
            graph.addVertex(i)
        for i in range(len(vertices) - 1):
            graph.addEdge(vertices[i], vertices[i+1])
        self.assertTrue(graph.isConnected())

    def test_connected_directed_true(self):
        graph = Graph(directed=True)
        vertices = ['A', 'B', 'C', 'D']
        for i in vertices:
            graph.addVertex(i)
        graph.addEdge(vertices[len(vertices) - 1], vertices[0])
        for i in range(len(vertices) - 1):
            graph.addEdge(vertices[i], vertices[i+1])
        self.assertTrue(graph.isConnected())

    def test_connected__all_but_one_undirected(self):
        graph = Graph()
        vertices = ['A', 'B', 'C', 'D', 'E']
        for i in vertices:
            graph.addVertex(i)
        for vertex1 in vertices:
            for vertex2 in vertices:
                if ('E' in (vertex1, vertex2)) or graph.hasEdge(vertex1, vertex2) or graph.hasEdge(vertex1, vertex2):
                    continue
                else:
                    graph.addEdge(vertex1, vertex2)
        self.assertFalse(graph.isConnected())

    def test_connected_all_undirected(self):
        graph = Graph()
        vertices = ['A', 'B', 'C', 'D', 'E']
        for i in vertices:
            graph.addVertex(i)
        for vertex1 in vertices:
            for vertex2 in vertices:
                if graph.hasEdge(vertex1, vertex2) or graph.hasEdge(vertex1, vertex2):
                    continue
                else:
                    graph.addEdge(vertex1, vertex2)
        self.assertTrue(graph.isConnected())

    def test_connected_all_directed(self):
        graph = Graph(directed=True)
        vertices = ['A', 'B', 'C']
        for i in vertices:
            graph.addVertex(i)
        for vertex1 in vertices:
            for vertex2 in vertices:
                graph.addEdge(vertex1, vertex2)
        self.assertTrue(graph.isConnected())

    def test_fully_connected_undirected_false(self):
        graph = Graph()
        vertices = ['A', 'B', 'C', 'D']
        for i in vertices:
            graph.addVertex(i)
        for i in range(len(vertices) - 1):
            graph.addEdge(vertices[i], vertices[i+1])
        self.assertFalse(graph.isFullyConnected())

    def test_fully_connected_directed_false(self):
        graph = Graph(directed=True)
        vertices = ['A', 'B', 'C', 'D']
        for i in vertices:
            graph.addVertex(i)
        graph.addEdge(vertices[len(vertices) - 1], vertices[0])
        for i in range(len(vertices) - 1):
            graph.addEdge(vertices[i], vertices[i+1])
        self.assertFalse(graph.isFullyConnected())

    def test_fully_connected_undireced_true(self):
        graph = Graph()
        vertices = ['A', 'B', 'C', 'D']
        for i in vertices:
            graph.addVertex(i)
        for vertex1 in vertices:
            for vertex2 in vertices:
                if graph.hasEdge(vertex1, vertex2) or graph.hasEdge(vertex1, vertex2):
                    continue
                else:
                    graph.addEdge(vertex1, vertex2)
        self.assertTrue(graph.isFullyConnected())

    def test_fully_connected_directed_true(self):
        graph = Graph(directed=True)
        vertices = ['A', 'B', 'C']
        for i in vertices:
            graph.addVertex(i)
        for vertex1 in vertices:
            for vertex2 in vertices:
                graph.addEdge(vertex1, vertex2)
        self.assertTrue(graph.isFullyConnected())

    def test_connected_directed_funky_false(self):
        graph = Graph(directed=True, weighted=True)
        vertices = ['A', 'B', 'C', 'D', 'E']
        for vertex in vertices:
            graph.addVertex(vertex)
        graph.addEdge('A', 'B', 1.0)
        graph.addEdge('B', 'C', 3.6)
        graph.addEdge('C', 'D', 4.2)
        graph.addEdge('C', 'E', 6.9)
        self.assertFalse(graph.isConnected())


if "__main__" == __name__:
    length = len(argv)
    file_num = 1 
    print()
    print("Starting Adjacency Matrix Graph Program")
    print("---------------------------------------")
    print()
    while file_num < length:
        print(f"Trying file '{argv[file_num]}'")
        graph = Graph(filename=str(argv[file_num]))
        file_num += 1
        print("\n---------------------------------\n")
