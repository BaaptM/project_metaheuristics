import sys
from graphDataStructure import *


def usage(prog):
	print ("usage : "+ prog + " <fichier graphe> ")  

###### MAIN ######
if __name__ == '__main__':
	if(len(sys.argv) != 2):
		usage(sys.argv[0])
		exit()

	with open(sys.argv[1], 'r') as f:
		lines = [l for l in f]
		print(lines)

