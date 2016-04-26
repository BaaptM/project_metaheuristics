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
        return self.num_vertices

    def get_nb_Edges(self):
        nb_edges = 0
        for v in g:
            nb_edges += len(v.get_connections())
        return nb_edges//2

    def sol_to_classes(self, sol):
        #convert sol like [[0,1,2][3,4]] to classes like [[a,b,c][d,e]]

        classes = []
        for classe in sol:
            build_classe = []
            for vertex_num in classe:
                build_classe.append(self.get_vertex(list(sorted(self.vert_dict.keys()))[vertex_num]))
            classes.append(build_classe)
        return classes

    def get_weight_inter(self, solutions):
        # function to sum the weight of interclass edges
        # @return the weight

        # todo check if all vertices are in the same graph
        # todo check if all vertex have a classe

        classes = self.sol_to_classes(solutions)
        edgeDone = [()]
        sum = 0
        for classe in classes[:-1]:
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
    #for vertex1 in graph:
    #    for vertex2 in vertex1.get_connections():
    #        vertex1Id = vertex1.get_id()
    #        vertex2Id = vertex2.get_id()
    #        print ('( %s , %s, %3d)'  % ( vertex1Id, vertex2Id, vertex1.get_weight(vertex2)))
    ##### GET ADJACENCE LIST ####
    #for vertex1 in graph:
    #    print ('graph.vert_dict[%s]= %s' %(vertex1.get_id(), graph.vert_dict[vertex1.get_id()]))
    #    print('degree(%s) = %s' %(vertex1.get_id(), vertex1.get_degree()))

    #### GET WEIGHT INTERCLASSES ####
    classes = [[0, 1, 2, 3], [4, 5]]

    weight_inter_classes = graph.get_weight_inter(classes)
    print('weight interclasses intended 17 have got : %s' %weight_inter_classes)






