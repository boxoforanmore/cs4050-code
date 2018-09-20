from __future__ import print_function
import unittest
from sys import argv
from copy import deepcopy

class Graph(object):
    def __init__(self, weighted=False, directed=False, filename=""):
        self.matrix = [[]]
        self.vertices = []
        self.weighted = weighted
        self.directed = directed
        if filename != "":
            self.readGraph(filename)

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
        if len(self.vertices) == 0:
            self.matrix = list([[]])
            self.vertices = []
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
        return indices


    # Check if edge already exists before adding (specs seem to not allow for multiple edges)
    # Check if directed or undirected (undirected should have mirrored matrix)
    def addEdge(self, vertex1, vertex2, weight=1):
        indices = self.__findIndices(vertex1, vertex2)
        if (-1 in indices):
            return False
        if ((self.hasEdge(vertex1, vertex2)) and not self.weighted):
            return False
        if not self.weighted:
            weight = 1
        if self.directed:
            self.matrix[indices[0]][indices[1]] = float(weight)
        else:
            self.matrix[indices[0]][indices[1]] = float(weight)
            self.matrix[indices[1]][indices[0]] = float(weight)
        return True

    # directed and undirected
    # Check if there is an item present before deleting
    def deleteEdge(self, vertex1, vertex2):
        indices = self.__findIndices(vertex1, vertex2)
        if (-1 in indices) or (not self.hasEdge(vertex1, vertex2)):
             return False
        self.matrix[indices[0]][indices[1]] = 0
        if not self.directed:
            self.matrix[indices[1]][indices[0]] = 0
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
        distance = self.__f_warshall()
        for row in distance:
            for col in row:
                if col == float("inf"):
                    del distance
                    return False
        return True

    def __f_warshall(self):
        num_vert = self.countVertices()
        distance = deepcopy(self.matrix)
        for index1, row in enumerate(distance):
            for index2, col in enumerate(row):
                if col <= 0:
                    distance[index1][index2] = float("inf")
        for index, vertex1 in enumerate(self.vertices):
            for vertex2 in self.vertices:
                if vertex1 is vertex2:
                    distance[index][index] = 0
        for k in range(0, num_vert):
            for i in range(0, num_vert):
                for j in range(0, num_vert):
                    if distance[i][j] > (distance[i][k] + distance[k][j]):
                        distance[i][j] = distance[i][k] + distance[k][j]
        return distance

    def __flatten(self, matrix):
        temp = []
        for row in self.matrix:
            for col in row:
                temp.append(col)
        return temp

    def isFullyConnected(self):
        req_edges = 2 * self.__k_edges(len(self.vertices))
        for index1, row in enumerate(self.matrix):
            for index2, col in enumerate(row):
                if (index2 == index1) or (col <= 0):
                    continue
                else:
                    req_edges -= 1
        if req_edges == 0:
            return True
        return False

    def __k_edges(self, k):
        if k == 2:
            return 1
        elif k == 3:
            return k
        else:
            return self.__k_edges(k-1) + k - 1

    def network_topo(self):
        if self.empty():
            return None
        if not self.isConnected():
            return None
        if self.isFullyConnected():
            return "Fully Connected Mesh"
        req_edges = 2 
        success = 0 
        for row in self.matrix:
            edge_count = 0 
            for col in row:
                if col==1:
                    edge_count += 1
            if req_edges == edge_count:
                success += 1
                continue
            else:
                success = 0 
                break
        num_verts = self.countVertices()
        if success == num_verts:
            return "Ring"
        success = 0 
        center_found = False
        req_edges = num_verts - 1 
        for row in self.matrix:
            edge_count = 0 
            for col in row:
                if col==True:
                    edge_count += 1
            if edge_count == 1:
                success += 1
                continue
            elif (center_found == False) and (edge_count == req_edges):
                success += 1
                center_found = True
            else:
                success = 0 
                break
        if success == num_verts:
            return "Star"
        return None

    def __findVertices(self, index1, index2):
        return [self.vertices[index1], self.vertices[index2]]

    def __findEdges(self):
        edges = []
        visited = [[False for _ in range(len(self.vertices))] for _ in range(len(self.vertices))]
        for index1, row in enumerate(self.matrix):
            for index2, col in enumerate(row):
                if col > 0:
                    vertices = self.__findVertices(index1, index2)
                    if self.weighted and self.directed:
                        edges.append(str(vertices[0] + " " + vertices[1] + " " + str(col)))
                    elif (not self.weighted) and self.directed:
                        edges.append(str(vertices[0] + " " + vertices[1]))
                    elif self.weighted and (not self.directed):
                        if (visited[index2][index1] and visited[index1][index2]):
                            continue
                        else:
                            edges.append(str(vertices[0] + " " + vertices[1] + " " + str(col)))
                            visited[index1][index2], visited[index2][index1] = True, True
                    elif (not self.weighted) and (not self.directed):
                        if (visited[index2][index1] and visited[index1][index2]):
                            continue
                        else:
                            edges.append(str(vertices[0] + " " + vertices[1]))
                            visited[index1][index2], visited[index2][index1] = True, True
        return edges

    # Print out similar output to input
    def printGraph(self):
        vertices = ""
        edges = self.__findEdges()
        weighted = "unweighted"
        directed = "undirected"
        for vertex in self.vertices:
            vertices += vertex + " "
        if self.weighted:
            weighted = "weighted"
        if self.directed:
            directed = "directed"
        final_print = weighted + "\n" + directed + "\n" + \
                      "begin\n" + vertices + "\n"
        for edge in edges:
            final_print += edge + "\n"
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
                        self.weighted = False
                    elif "weighted" in line:
                        self.weighted = True
                    elif "undirected" in line:
                        self.directed = False
                    elif "directed" in line:
                        self.directed = True
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
                            if not self.weighted:
                                print(f"Adding edge '{edges[0]}  {edges[1]}' to graph")
                                actual_result = self.addEdge(edges[0], edges[1])
                            else:
                                print(f"Adding edge '{edges[0]} {edges[1]} {edges[2]}' to graph")
                                actual_result = self.addEdge(edges[0], edges[1], edges[2])
                            if actual_result:
                                if self.weighted:
                                    print(f"{actual_result} : edge '{edges[0]} {edges[1]} {edges[2]}' added to graph\n")
                                else:
                                    print(f"{actual_result} : edge '{edges[0]} {edges[1]}' added to graph\n")
                            else:
                                print(f"{actual_result} : edge '{edges[0]} {edges[1]} {edges[2]}' not added to graph\n")
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
                if self.weighted:
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
                                      "[0, 1.0, 0], "\
                                      "[0, 0, 0]]")

    def test_add_all_loop_edges(self):
        graph = Graph()
        vertices = ['A', 'B', 'C']
        for i in vertices:
            graph.addVertex(i)
        for i in vertices:
            graph.addEdge(i, i)
            self.assertTrue(graph.hasEdge(i, i))
        self.assertEqual(str(graph), "[[1.0, 0, 0], "\
                                      "[0, 1.0, 0], "\
                                      "[0, 0, 1.0]]")

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
        self.assertEqual(str(graph), "[[0, 1.0, 1.0], "\
                                      "[1.0, 0, 1.0], "\
                                      "[1.0, 1.0, 0]]")

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
        self.assertEqual(str(graph), "[[1.0, 1.0, 1.0], "\
                                     "[1.0, 1.0, 1.0], "\
                                     "[1.0, 1.0, 1.0]]")

    def test_add_edge_twice(self):
        graph = Graph()
        vertices = ['A', 'B', 'C']
        for i in vertices:
            graph.addVertex(i)
        graph.addEdge(vertices[0], vertices[1])
        self.assertFalse(graph.addEdge(vertices[0], vertices[1]))
        self.assertFalse(graph.addEdge(vertices[1], vertices[0]))

    def test_add_edge_twice(self):
        graph = Graph(weighted=True)
        vertices = ['A', 'B', 'C']
        for i in vertices:
            graph.addVertex(i)
        graph.addEdge(vertices[0], vertices[1], 1)
        self.assertTrue(graph.hasEdge(vertices[0], vertices[1]))
        self.assertTrue(graph.addEdge(vertices[0], vertices[1], 11))

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
