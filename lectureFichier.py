import sys
from graphDataStructure import *


def usage(prog):
    print("usage : " + prog + " <fichier graphe> ")


def isComment(letter):
    return (letter == '#')

class Reader():
    def __init__(self, file):
        self.file = file
        self.nbVertices = 0
        self.nbEdges = 0
        self.dmin = 0
        self.dmax = 0
        self.g = Graph()
        self.degreeFileList = []

    def readFile(self):
        with open(self.file, 'r') as f:
            lines = [ls for ls in f]
            cpt = 0
            for i in range(0, len(lines)):
                letter = [l for l in lines[i]]
                if (isComment(letter[0])):
                    cpt += 1
                else:
                    if (cpt == 1):  ##### 1er commentaire : nbSommets nbAretes
                        self.nbVertices, self.nbEdges = lines[i].split()
                    if (cpt == 2):  ##### 2eme commentaire : dmin dmax
                        self.dmin, self.dmax = lines[i].split()
                    if (cpt == 3):  ##### 3eme commentaire : from to weight
                        self.g.add_edge(lines[i].split()[0], lines[i].split()[1], int(lines[i].split()[2]))
                    if (cpt == 4):
                        self.degreeFileList.append(int(lines[i].split()[1]))


###### MAIN ######
if __name__ == '__main__':
    if (len(sys.argv) != 2):
        usage(sys.argv[0])
        exit()

    reader = Reader(sys.argv[1])
    reader.readFile()

    ######## ASSERT DEG == DEG FILE #########
    for i in range(0, len(reader.degreeFileList)):
        assert (reader.g.get_vertex(str(i + 1)).get_degree() == reader.degreeFileList[i])

    print("------- Paramètre du fichier lu -------")
    print("nbVertices = ", reader.nbVertices, ", nbEdges = ", reader.nbEdges)
    print("dmin = ", reader.dmin, ", dmax = ", reader.dmax)
    print("------- Représentation du graphe à partir du fichier -------")
    ##### GET CONNECTIONS ####
    for v in reader.g:
        for w in v.get_connections():
            vid = v.get_id()
            wid = w.get_id()
            print('( %s , %s, %3d)' % (vid, wid, v.get_weight(w)))
    ##### GET ADJACENCE LIST ####
    for v in reader.g:
        print('g.vert_dict[%s]= %s' % (v.get_id(), reader.g.vert_dict[v.get_id()]))
        print('degree(%s) = %s' % (v.get_id(), v.get_degree()))
