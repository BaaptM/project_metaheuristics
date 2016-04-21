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
        return g.num_vertices

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



if __name__ == '__main__':
###### TEST ######
    g = Graph()

    g.add_vertex('a')
    g.add_vertex('b')
    g.add_vertex('c')
    g.add_vertex('d')
    g.add_vertex('e')
    g.add_vertex('f')

    g.add_edge('a', 'b', 1)
    g.add_edge('a', 'c', 2)
    g.add_edge('a', 'e', 3)
    g.add_edge('b', 'f', 4)
    g.add_edge('b', 'd', 5)
    g.add_edge('c', 'd', 4)
    g.add_edge('c', 'b', 3)
    g.add_edge('d', 'e', 2)
    g.add_edge('e', 'f', 1)

    #print("path :",g.find_all_paths('a','c'))
    #graph = g.vert_dict
    #for v in graph['a'].adjacent:
    #    print(v.get_id())


    #### GET CONNECTIONS ####
    for v in g:
        for w in v.get_connections():
            vid = v.get_id()
            wid = w.get_id()
            print ('( %s , %s, %3d)'  % ( vid, wid, v.get_weight(w)))
    #### GET ADJACENCE LIST ####
    for v in g:
        print ('g.vert_dict[%s]= %s' %(v.get_id(), g.vert_dict[v.get_id()]))
        print('degree(%s) = %s' %(v.get_id(), v.get_degree()))