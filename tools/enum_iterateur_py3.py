#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "mmc <marc-michel dot corsini at u-bordeaux dot fr>"
__usage__ = "Itérateur how to"
__version__ = "0.2"

#---- import --------
import itertools
#--------------------

nbSommets = 4 # nombre de sommets
nbClasses = 3 # nombre de classes
# l'ensemble des sommets est :
sommets = range(nbSommets) # on a nb sommets
# on cree les ensembles de classes possibles pour chaque sommet
support = ( range(nbClasses) for _ in sommets )
# on cree l'iterateur
monIterateur = itertools.product(*support)
# pour chaque reponse de l'iterateur on cree les partitions
nbSol = 0 # nombre de partitions trouvées
for rep in monIterateur :
    # au début les partitons sont vides
    sol = [ [] for _ in range(nbClasses) ]
    # si on est là c'est que l'itérateur a trouvé une solution
    nbSol += 1
    # on transforme une réponse du type (0,1,0,1) en [ [0,2], [1,3], [] ]
    # puisque pour chaque sommet il donne à quelle partition il appartient
    for s,x in enumerate(rep):
        sol[x].append(s) # le sommet s est dans la partition numero x
    # on a une realisation de l'enumeration
    # on fait un traitement avec (ici juste un print pour exemple)
    print ("Sol = {0!r:23} numero = {1:02}".format(sol,nbSol))

# On verifie que l'on a eu le bon nombre de réponses
_msg = "Found: {found:d} partitions. "
_msg += "Expected: {expected:d} > "
_msg += "diagnostic {status}"
d = {'found':nbSol,'expected':nbClasses ** nbSommets}
d['status'] = d['found']==d['expected']
print (_msg.format(**d))
