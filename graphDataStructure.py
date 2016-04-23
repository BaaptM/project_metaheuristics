#!/usr/local/bin/pyhon3
import sys

class Vertex:
    def __init__(self, node):
        self.id = node
        self.adjacent = {}

    def __str__(self):
        return str(self.id) + ' adjacent: ' + str([x.id for x in self.adjacent])

    def add_neighbor(self, neighbor, weight=0):
        self.adjacent[neighbor] = weight

    def get_connections(self):
        return self.adjacent.keys()  

    def get_id(self):
        return self.id

    def get_weight(self, neighbor):
        return self.adjacent[neighbor]

    def get_degree(self):
        return len(self.get_connections())

class Graph:
    def __init__(self):
        self.vert_dict = {}
        self.num_vertices = 0

    def __iter__(self):
        return iter(self.vert_dict.values())

    def add_vertex(self, node):
        self.num_vertices = self.num_vertices + 1
        new_vertex = Vertex(node)
        self.vert_dict[node] = new_vertex
        return new_vertex

    def get_vertex(self, n):
        if n in self.vert_dict:
            return self.vert_dict[n]
        else:
            return None

    def add_edge(self, frm, to, cost = 0):
        if frm not in self.vert_dict:
            self.add_vertex(frm)
        if to not in self.vert_dict:
            self.add_vertex(to)

        self.vert_dict[frm].add_neighbor(self.vert_dict[to], cost)
        self.vert_dict[to].add_neighbor(self.vert_dict[frm], cost)

    def get_vertices(self):
        return self.vert_dict.keys()

    def get_dMin(self):
        min = sys.maxsize
        for v in self.vert_dict.values():
            v_degree = v.get_degree()
            if (v_degree < min):
                min = v_degree
        return min

    def get_dMax(self):
        max = 0
        for v in self.vert_dict.values():
            v_degree = v.get_degree()
            if (v_degree > max):
                max = v_degree
        return max

    def get_nbVertices(self):
        return graph.num_vertices

    def get_nb_Edges(self):
        nb_edges = 0
        for v in g:
            nb_edges += len(v.get_connections())
        return nb_edges//2

    def find_path(self, start_vertex, end_vertex, path=[]):
        graph = self.vert_dict
        path += [start_vertex]
        if (start_vertex == end_vertex):
            return path
        if (start_vertex not in graph):
            return None
        for vertex in graph[start_vertex].adjacent:
            if vertex.get_id() not in path:
                extended_path = self.find_path(vertex.get_id(),
                                               end_vertex,
                                               path)
                if extended_path:
                    return extended_path
        return None

    #def find_all_paths(self, start_vertex, end_vertex, path=[]):
    #    graph = self.vert_dict
    #    path += [start_vertex]
    #    if (start_vertex == end_vertex):
    #        return path
    #    if (start_vertex not in graph):
    #        return []
    #    paths = []
    #    for vertex in graph[start_vertex].adjacent:
    #        if vertex.get_id() not in path:
    #            extended_paths = self.find_all_paths(vertex.get_id(),
    #                                                 end_vertex,
    #                                                 path)
    #            for p in extended_paths:
    #                paths.append(p)
    #    return paths


#todo check if vertex is in graph
#todo do not do check vertex of the last classe
def get_weight_inter(classes):
    edgeDone = [()];
    sum = 0;
    for classe in classes:
        for vertex in classe:
            for neighboor in vertex.get_connections():
                if edgeDone.count((vertex,neighboor)) == 0 and edgeDone.count((neighboor,vertex)) == 0 and classe.count(neighboor) == 0:
                    edgeDone.append((vertex,neighboor))
                    sum += vertex.get_weight(neighboor)
    return sum





if __name__ == '__main__':
###### TEST ######
    graph = Graph()

    graph.add_vertex('a')
    graph.add_vertex('b')
    graph.add_vertex('c')
    graph.add_vertex('d')
    graph.add_vertex('e')
    graph.add_vertex('f')

    graph.add_edge('a', 'b', 1)
    graph.add_edge('a', 'c', 2)
    graph.add_edge('a', 'e', 3)
    graph.add_edge('b', 'f', 4)
    graph.add_edge('b', 'd', 5)
    graph.add_edge('c', 'd', 4)
    graph.add_edge('c', 'b', 3)
    graph.add_edge('d', 'e', 2)
    graph.add_edge('e', 'f', 1)

    #print("path :",graph.find_all_paths('a','c'))
    #graph = graph.vert_dict
    #for v in graph['a'].adjacent:
    #    print(v.get_id())


    #### GET CONNECTIONS ####
    for vertex1 in graph:
        for vertex2 in vertex1.get_connections():
            vertex1Id = vertex1.get_id()
            vertex2Id = vertex2.get_id()
            print ('( %s , %s, %3d)'  % ( vertex1Id, vertex2Id, vertex1.get_weight(vertex2)))
    #### GET ADJACENCE LIST ####
    for vertex1 in graph:
        print ('graph.vert_dict[%s]= %s' %(vertex1.get_id(), graph.vert_dict[vertex1.get_id()]))
        print('degree(%s) = %s' %(vertex1.get_id(), vertex1.get_degree()))

    #### GET  WEIGHT INTER
    classe1 = [graph.get_vertex('a'), graph.get_vertex('e')]
    classe2 = [graph.get_vertex('b'), graph.get_vertex('d')]
    classe3 = [graph.get_vertex('c'), graph.get_vertex('f')]
    classes = [classe1,classe2, classe3]

    weight_inter_classes = get_weight_inter(classes)
    print(weight_inter_classes)