from __future__ import print_function
from sys import argv
import unittest

class Graph(object):
    """
    This class represents a graph as an Adjacency List
    """

    class __edge(object):
        """
        This subclass is an edge object holding the connected vertex
        and the weight
        """

        def __init__(self, to_vertex, weight=1, from_vertex=None):
            """
            The constructor/initializer for the edge object

            :param to_vertex: The adjacent vertex
            :param weight: The weight of the connected edge (default=1)
            """

            self.weight = weight
            self.to_vertex = to_vertex
            self.from_vertex = from_vertex

        def __str__(self):
            return str(self.from_vertex.name + ' --> ' + str(self.weight) + ' --> ' + self.to_vertex.name)


    class __vertex(object):
        """
        This subclass is a vertex object holding the connected
        vertices in a list and associated methods
        """

        def __init__(self, name, weighted=False):
            """
            The constructor/initializer for the edge object

            :param name: The vertex name
            :param weighted: If the graph is weighted or not
            """

            self.name = name
            self.edges = []
            self.weighted = weighted

        def __str__(self):
            """
            Returns a string representation of the matrix in adjacency list format

            :return: The string representation of the list
            """

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
            """
            Adds an edge to the vertex's list of edges (if it is not already present)

            :param new_edge: The new edge object to be added
            :return: True or False
            :rtype: bool
            """

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
            """
            Deletes an edge from the vertex's list of edges (if it is present)

            :param del_edge: The edge object to be deleted
            :return: True or False
            :rtype: bool
            """

            edge = self.findEdge(del_edge)
            if edge != None:
                self.edges.remove(edge)
                return True
            return False
                
        def findEdge(self, to_vertex):
            """
            Finds an edge and returns it if it exists, otherwise, it returns None
            :param to_vertex: The vertex to find
            :return: The found edge or None
            :rtype: edge or None
            """
            for edge in self.edges:
                if edge.to_vertex == to_vertex:
                    return edge
            return None


    def __init__(self, directed=False, weighted=False, filename=""):
        """
        The constructor/initializer for the graph object

        :param directed: If the graph is directed or not (default=False)
        :param weighted: If the graph is weighted or not (default=False)
        :param filename: The input filename (default="")
        """

        self.__vertices = []
        self.__directed = directed
        self.__weighted = weighted
        self.__filename = filename
        self.__visited = dict()

        if filename != "":
            self.readGraph(self.__filename)

    def empty(self):
        """
        This checks if the graph is empty by checking the list of vertices.

        :return: True or False
        :rtype: bool
        """
        return (self.__vertices == [])

    def __len__(self):
        """
        This gets the length of the graph (the length of the vertices)

        :return: The number of vertices
        :rtype: int
        """
        return len(self.__vertices)

    def __str__(self):
        """
        This returns a string representation of the entire graph as
        an Adjacency List, calling the individual functions on each
        vertex

        :return: The string representation of the list
        :rtype: str
        """

        graph_str = ""
        for vertex in self.__vertices:
            graph_str += str(vertex) + "\n"
        return graph_str

    def __iter__(self):
        """
        This creates an iteratable form of the graph

        :return: The iteratable of the primary Adjacency List
        :rtype: iter/list
        """

        return iter(self.__vertices)

    def addVertex(self, name):
        """
        This adds a new vertex to the graph if it does not already exist

        :param name: The name of the vertex to be added
        :return: True or False
        :rtype: bool
        """

        if not self.__findVertex(name):
            self.__vertices.append(self.__vertex(name, self.__weighted))
            return True
        else:
            return False

    def deleteVertex(self, name):
        """
        This deletes a vertex from the graph if it exists

        :param name: The name of the vertex to be deleted
        :return: True or False
        :rtype: bool
        """

        vertex1 = self.__findVertex(name)
        if vertex1 != None:
            for vertex in self.__vertices:
                if vertex == vertex1:
                    continue
                self.deleteEdge(vertex.name, vertex1.name)
            self.__vertices.remove(vertex1)
            return True
        return False


    def __findPosition(self, name):
        """
        This finds the index/position of the vertex in the
        vertices list if it exists

        :param name: The name of the vertex to be found
        :return: The index or -1 if not found
        :rtype: int
        """

        for index, vertex in enumerate(self.__vertices):
            if vertex.name == name:
                return index
        return -1

    def __findVertex(self, name):
        """
        This checks that the vertex exists and
        returns False if it does not

        :param name: The name of the vertex to be found
        :return: True or False
        :rtype:
        """

        for vertex in self.__vertices:
            if vertex.name == name:
                return True
        return False

    def addEdge(self, name1, name2, weight=1):
        """
        This adds an edge if both vertices exist and overwrite
        the weight if the graph is weighted; if the graph is
        not weighted and the edge exists, the method returns
        False

        :param name1: The first vertex
        :param name2: The second vertex
        :param weight: The weight of the edge
        :return: True or False
        :rtype: bool
        """

        vertex1 = self.__findVertex(name1)
        vertex2 = self.__findVertex(name2)
        if (None != vertex1) and (None != vertex2):
            if self.hasEdge(name1, name2) and not self.__weighted:
                return False
            vertex1.addEdge(self.__edge(vertex2, weight, vertex1))
            if (not self.__directed) and (name1 != name2):
                if self.hasEdge(name2, name1) and not self.__weighted:
                    return False
                vertex2.addEdge(self.__edge(vertex1, weight, vertex2))
            return True
        return False

    def __findVertex(self, name):
        """
        This finds and returns a vertex object based
        on it's name value; otherwise, it returns None

        :param name: The name of the vertex to be returned
        :return: The found vertex object or None
        :rtype: vertex or None
        """

        for vertex in self.__vertices:
            if vertex.name == name:
                return vertex
        return None

    def deleteEdge(self, name1, name2):
        """
        This deletes an edge if it exists from the name
        of the two connected vertices

        :param name1: The first vertex
        :param name2: The second vertex
        :return: True or False
        :rtype: bool
        """

        vertex1 = self.__findVertex(name1)
        vertex2 = self.__findVertex(name2)
        if (vertex1 != None) and (vertex2 != None):
            ret_val = vertex1.deleteEdge(vertex2)
            if (not self.__directed) and (vertex1 != vertex2):
                ret_val = vertex2.deleteEdge(vertex1)
            return ret_val
        return False

    def countEdges(self):
        """
        This counts the number of edges and loops in the graph
        and returns the number

        :return: The number of edges in the graph
        :rtype: int
        """

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
        """
        This counts the number of vertices in the graph
        and returns the number

        :return: The number of vertices in the graph
        :rtype: int
        """

        return len(self)

    def __sparsity(self):
        """
        This calculates the sparsity/density value
        and returns the number

        :return: The sparsity/density value
        :rtype: float
        """

        if self.__directed:
            return 100 * (self.countEdges()) / (self.countVertices() * 2)
        num_vertices = self.countVertices()
        return 100 * (2 * self.countEdges()) / ((3**(num_vertices-2)) + num_vertices)

    def isSparse(self):
        """
        This uses the graph's sparsity value to
        determine if the graph is sparse or not

        :return: True or False
        :rtype: bool
        """

        if self.__sparsity() > 15:
            return False
        return True

    def isDense(self):
        """
        This uses the graph's density value to
        determine if the graph is dense or not

        :return: True or False
        :rtype: bool
        """

        if self.__sparsity() > 85:
            return True
        return False

    def __k_edges(self, k):
        """
        This recursively calculates and returns
        the number of edges needed for a graph
        (or subgraph) to be a clique from its
        number of vertices

        :param k: The number of vertices
        :return: The number of required edges
        :rtype: int
        """

        if k == 2:
            return 1
        if k == 3:
            return k
        else:
            return self.__k_edges(k-1) + k - 1

    def hasEdge(self, name1, name2):
        """
        This checks to see if a graph has an edge from
        the vertex with name1 to the vertex with name2
        and returns True if it is found

        :param name1: The starting vertex name
        :param name2: The ending vertex name
        :return: True or False
        :rtype: bool
        """

        vertex1 = self.__findVertex(name1)
        vertex2 = self.__findVertex(name2)
        if (vertex1 != None) and (vertex2 != None):
            if vertex1.findEdge(vertex2) != None:
                return True
        return False

    def isFullyConnected(self):
        """
        This checks if a graph is fully connected
        using the k_cliques equation/method

        :return: True or False
        :rtype: bool
        """

        if len(self.__vertices) == 0:
            return False
        elif len(self.__vertices) == 1:
            return True
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
        """
        This checks if a graph is connected (there is
        a path from one node to every other node) and
        returns True if it is

        :return: True or False
        :rtype: bool
        """

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

    def network_topo(self):
        """
        This checks for one of three network topologies
        ("Fully Connected Mesh", "Ring", "Star") and
        returns None if none are identified

        :return: The type of network topology or None
        :rtype: str or None
        """

        if not self.isConnected():
            return None
        if self.isFullyConnected():
            return "Fully Connected Mesh"
        if self.empty():
            return None
        req_edges = 2
        success = 0
        for vertex in self.__vertices:
            if len(vertex.edges) == req_edges:
                success += 1
            else:
                success = 0
                break
        num_verts = self.countVertices()
        if success == num_verts:
            return "Ring"
        success = 0
        center_found = False
        req_edges = num_verts - 1
        for vertex in self.__vertices:
            if len(vertex.edges) == 1:
                success += 1
                continue
            elif (center_found == False) and (len(vertex.edges) == req_edges):
                success += 1
                center_found = True
                continue
            else:
                success = 0
                break
        if success == num_verts:
            return "Star"
        return None

    def __is_isomorphic(self, other):
        """
        (INCOMPLETE)
        This checks that two graphs are isomorphic and
        returns the mapping if they are

        :param other: The other graph object to be analyzed
        :return: The mapping of the isomorphic graph or None
        :rtype: dict or None
        """

        if not (self.countVertices() == other.countVertices()) or not (self.countEdges() == other.countEdges()):
            return False
        if self.isFullyConnected() and other.isFullyConnected():
            mapping = dict()
            for index, vertex in enumerate(self):
                mapping[index] = tuple((vertex, other[index]))
            return mapping
        my_verts = dict()
        other_verts = dict()
        for vertex in self:
            my_verts[vertex.name] = len(vertex.edges)
        for vertex in other:
            other_verts[vertex.name] = len(vertex.edges)
        my_edges = dict()
        other_edges = dict()

        for vertex in self:
            my_edges[vertex.name] = []
            for edge in vertex.edges:
                my_edges[vertex.name].append(my_verts[edge.to_node.name])
            my_edges[vertex.name] = sorted(my_edges[vertex.name])

        for vertex in other:
            other_edges[vertex.name] = []
            for edge in vertex.edges:
                other_edges[vertex.name].append(my_verts[edge.to_node.name])
            my_edges[vertex.name] = sorted(my_edges[vertex.name])

        matched_indices = list()
        index1 = 0

        ## Do I need to do a dict for this further?

        for edge1 in my_edges:
            matched_indices.append([])
            index2 = 0
            for edge2 in other_edges:
                if edge1 == edge2:
                    matched_indices[index1].append(edge2)
                    
                index2 += 1
            if matched_indices[index1] == []:
                return False
            index += 1
        mapping = dict()
        for edge in matched_indices:
            if len(mapping) == 0:
                pass                

    def __find_path(self, start_vertex, end_vertex, path=None):
        """
        This recursively finds a path from any start vertex
        to an end vertex (if they are connected), while
        avoiding cycles; returns a list of the path if
        one is found

        :param start_vertex: The starting vertex
        :param end_vertex: The ending vertex
        :param path: The vertices already visited in the path (default=None)
        :return: The path or None
        :rtype: list or None
        """

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

    def mst(self):
        return self.__prims()

    def __prims(self):
        if self.__directed or not self.isConnected():
            return None
        vertices = [self.__vertices[0]]
        vert_names = []
        edges = []
        vert_names.append(vertices[0].name)

        for index in range(1, len(self.__vertices)):
            temp_weight = float("inf")
            mins = []
            for vertex in vertices:
                for edge in vertex.edges:
                    if (edge.weight < temp_weight) and (edge.to_vertex not in vertices):
                        temp_weight = edge.weight
                        mins.append([edge.weight, edge])
            min_set = min(mins)
            vertices.append(min_set[1].to_vertex)
            edges.append(min_set[1])
        return edges  

    def __findEdges(self):
        """
        This finds and returns a list of all edges
        (with weights if weighted) for printing in
        it's input format

        :return: The list of edges in the graph
        :rtype: list
        """

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
        """
        This prints a representation of the graph
        similar to the input taken from the
        readGraph method

        :return: True
        :rtype: bool
        """

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
        """
        This reads a graph from a given input
        file and parses through it to run and
        test functionality

        :param filename: The input file name
        :return: None
        """

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
        """
        This receives a line from the input file
        and matches it with an internal
        method to run and test

        :param line: The line from the input file
        :return: The return value of the called method
        :rtype: bool or int
        """

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

    def test_no_network_topo_empty(self):
        graph = Graph()
        self.assertEqual(graph.network_topo(), None)
    
    def test_connected_no_network_topo_some(self):
        graph = Graph()
        vertices = ['A', 'B', 'C', 'D', 'E']
        for vertex in vertices:
            graph.addVertex(vertex)
        graph.addEdge('A', 'B')
        graph.addEdge('A', 'E')
        graph.addEdge('B', 'C')
        graph.addEdge('C', 'D')
        self.assertEqual(graph.network_topo(), None)

    def test_fully_connected_mesh(self):
        graph = Graph()
        vertices = ['A', 'B', 'C', 'D', 'E', 'F']
        for vertex in vertices:
            graph.addVertex(vertex)
        for vertex1 in vertices:
            for vertex2 in vertices:
                if vertex1 != vertex2:
                    graph.addEdge(vertex1, vertex2)
        self.assertTrue(graph.isFullyConnected())
        self.assertEqual(graph.network_topo(), "Fully Connected Mesh")

    def test_ring_topo(self):
        graph = Graph()
        vertices = ['A', 'B', 'C', 'D', 'E', 'F']
        for vertex in vertices:
            graph.addVertex(vertex)
        for index, vertex in enumerate(vertices):
            if (index + 1) == len(vertices):
                graph.addEdge(vertex, vertices[0])
                break
            graph.addEdge(vertex, vertices[index+1])
        self.assertEqual(graph.network_topo(), "Ring")

    def test_star_topo(self):
        graph = Graph()
        vertices = ['A', 'B', 'C', 'D', 'E', 'F']
        for vertex in vertices:
            graph.addVertex(vertex)
        for vertex in vertices:
            if vertex != vertices[0]:
                graph.addEdge(vertices[0], vertex)
        self.assertEqual(graph.network_topo(), "Star")

    def test_prims_directed(self):
        graph = Graph(directed=True)
        self.assertEqual(graph.mst(), None)


    def test_prims_not_connected(self):
        graph = Graph()
        vertices = ['A', 'B', 'C', 'D', 'E']
        for vertex in vertices:
            graph.addVertex(vertex)
        for vertex1 in vertices:
            for vertex2 in vertices:
                graph.addEdge(vertex1, vertex2)
        graph.addVertex('Z')
        self.assertEqual(graph.mst(), None)
        
    def test_prims_simple(self):
        graph = Graph(weighted=True)
        vertices = ['A', 'B', 'C', 'D', 'E']
        for vertex in vertices:
            graph.addVertex(vertex)

        graph.addEdge('A', 'B', 15)
        graph.addEdge('A', 'C', 25)
        graph.addEdge('B', 'E', 10)
        graph.addEdge('C', 'D', 10)
        graph.addEdge('C', 'E', 20)
        mst = graph.mst()
        output = str()

        for edge in mst:
            output += str(edge) + ', '

        expected = 'A --> 15 --> B, ' \
                   'B --> 10 --> E, ' \
                   'E --> 20 --> C, ' \
                   'C --> 10 --> D, '

        self.assertEqual(output, expected)

    def test_prims_more_complex(self):
        graph = Graph(weighted=True)
        vertices = ['A', 'B', 'C', 'D', 'E', 'F']
        for vertex in vertices:
            graph.addVertex(vertex)

        graph.addEdge('A', 'B', 7)
        graph.addEdge('A', 'D', 4)
        graph.addEdge('A', 'F', 2)
        graph.addEdge('A', 'C', 8)
        graph.addEdge('B', 'C', 9)
        graph.addEdge('B', 'D', 14)
        graph.addEdge('C', 'D', 10)
        graph.addEdge('D', 'E', 2)
        graph.addEdge('E', 'F', 6)
        graph.addEdge('F', 'D', 3)

        mst = graph.mst()
        output = str()

        for edge in mst:
            output += str(edge) + ', '

        expected = 'A --> 2 --> F, ' \
                   'F --> 3 --> D, ' \
                   'D --> 2 --> E, ' \
                   'A --> 7 --> B, ' \
                   'A --> 8 --> C, '

        self.assertEqual(output, expected)

if "__main__" == __name__:
    length = len(argv)
    file_num = 1 
    print()
    print("Starting Adjacency List Graph Program")
    print("---------------------------------------")
    print()
    while file_num < length:
        print(f"Trying file '{argv[file_num]}'")
        graph = Graph(filename=str(argv[file_num]))
        file_num += 1
        print("\n---------------------------------\n")
