#!/usr/bin/python
# *-* coding: utf-8 -*-
# $Id: findPartition.py,v 1.3 2012/03/27 18:01:45 mmc Exp $
#

"""
Comment generer une partition aleatoire en deux classes pour n sommets
"""
__author__ = "mmc <marc.corsini@u-bordeaux2.fr>"

#---- import --------
import random
#--------------------

def makeBiPartition(nbSommets):
    """
    cree une partition des sommets en deux classes
    les sommets sont de 1 a N
    @param nbSommets: nombre de sommets
    @return: une partition en deux classes
    """
    l = range(1,nbSommets+1) # la liste des sommets
    k_1 = random.sample(l, nbSommets / 2) # la premiere classe
    k_2 = [ x for x in l if x not in k_1 ] # la seconde classe
    k_1.sort() # on trie
    return k_1,k_2

if __name__ == '__main__' :
    for i in range(7,11):
        print 'Partition en deux classes, %d sommets' % i
        print makeBiPartition(i)

