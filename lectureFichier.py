import sys
from graphDataStructure import *


def usage(prog):
	print ("usage : "+ prog + " <fichier graphe> ")

def isComment(letter):
	return (letter == '#')

###### MAIN ######
if __name__ == '__main__':
	if(len(sys.argv) != 2):
		usage(sys.argv[0])
		exit()

	with open(sys.argv[1], 'r') as f:
		lines = [ls for ls in f]
		cpt = 0
		nbVertices = 0
		nbEdges = 0
		dmin = 0
		dmax = 0
		g = Graph()
		degreeFileList = []
		for i in range(0, len(lines)):
			letter = [l for l in lines[i]]
			if(isComment(letter[0])):
				cpt+=1
			else:
				if(cpt == 1): ##### 1er commentaire : nbSommets nbAretes
					nbVertices = letter[0]
					nbEdges = letter[2]
				if(cpt == 2): ##### 2eme commentaire : dmin dmax
					dmin = letter[0]
					dmax = letter[2]
				if(cpt == 3): ##### 3eme commentaire : from to weight
					g.add_edge(letter[0], letter[2], int(letter[4]))
				if(cpt == 4):
					degreeFileList.append(int(letter[2]))

		######## ASSERT DEG == DEG FILE #########
		for i in range(0,len(degreeFileList)):
			assert(g.get_vertex(str(i+1)).get_degree() == degreeFileList[i])

		print("------- Paramètre du fichier lu -------")
		print("nbVertices = ",nbVertices,", nbEdges = ",nbEdges)
		print("dmin = ",dmin,", dmax = ",dmax)
		print("------- Représentation du graphe à partir du fichier -------")
		##### GET CONNECTIONS ####
		for v in g:
			for w in v.get_connections():
				vid = v.get_id()
				wid = w.get_id()
				print('( %s , %s, %3d)' % (vid, wid, v.get_weight(w)))
		##### GET ADJACENCE LIST ####
		for v in g:
			print('g.vert_dict[%s]= %s' % (v.get_id(), g.vert_dict[v.get_id()]))
			print('degree(%s) = %s' % (v.get_id(), v.get_degree()))







