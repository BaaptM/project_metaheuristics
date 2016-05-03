#!/usr/bin/python
# *-* coding: utf-8 -*-
# $Id: enumGraphe.py,v 1.4 2012/03/27 18:01:27 mmc Exp $
#


# On s'occupe de l'enumeration
# explicite : ne pas rater de classes
# implicite : ne pas explorer de classes sans avenir
import random

__author__ = "mmc <marc.corsini@u-bordeaux2.fr>"

#---- import -----------------------------------
import itertools
#-----------------------------------------------

def enum_gen(nbS,nbK):

    # construction d'un enumerateur
    # @param nbS: le nombre de sommets
    # @param nbK: le nombre de classes
    # @return: un iterateur

    _support = ( range(nbK) for _ in range(nbS) )
    return itertools.product(* _support)

def __fromGen2Partition(rep,nbS,nbK):

    # methode privee:
    # Transforme une reponse du generateur en partition
    # @param rep: reponse a traiter
    # @param nbS: nombre de sommets
    # @param nbK: nombre de classes
    # @return: une partition

    _sol = [ [] for _ in range(nbK) ]
    for s,x in enumerate(rep):
        _sol[x].append(s)
    return _sol

def getSoluces(nbS,nbK):

    # la liste de toutes les solutions
    # @param nbS: le nombre de sommet
    # @param nbK: le nombre de classes
    # @return: une liste des solutions

    _generator = enum_gen(nbS,nbK)
    return [ __fromGen2Partition(_,nbS,nbK) for _ in _generator ]


def get_random_soluce(nbS,nbK):

    # get a random soluce
    # @param nbS: le nombre de sommet
    # @param nbK: le nombre de classes
    # @return one random soluce

    sol = []
    for k in range(nbK):
        sol.append([])
    for i in range(nbS):
        sol[random.randint(0, nbK-1)].append(i)
    return sol
def get_max_delta(sol):
    max_delta = 0
    for classe1 in sol:
        for classe2 in sol:
            delta = abs(len(classe1) - len(classe2))
            if max_delta < delta:
                max_delta = delta
    return max_delta


def validate_solution(solutions, delta):
    valid_sol = []
    for sol in solutions:
        if get_max_delta(sol) <= delta:
            valid_sol.append(sol)
    return valid_sol

def rec(nbK,nbS):

    # Implementation recursive de l'enumeration de solutions
    # pour le partitionnement d'un graphe
    # @param nbK: nombre de classes
    # @param nbS: nombre de sommets
    # @return: ensemble des solutions acceptables
    
        # >>> rec(2,4)
        # [[0, 0, 1, 1], [0, 1, 0, 1], [0, 1, 1, 0], [1, 0, 0, 1], [1, 0, 1, 0], [1, 1, 0, 0]]

    def local(x,idx,sol,done):

        # fonction locale recursive terminale
        #
        # @param x: sommet a traiter
        # @param idx: index de classe a affecter pour x
        # @pram sol: solution en cours de traitement
        # @pram done: ensemble des solutions deja connus

        if x >= nbS :
            done.append(sol)
            newidx = sol[-1] + 1
            return local(x-1,newidx,sol[:-1],done)
        if idx >= nbK :
            if x == 0 : return done
            else:
                newidx = sol[-1] + 1
                return local(x-1,newidx,sol[:-1],done)
        else:
            sol.append(idx)
            if valide(nbK,nbS,sol):
                return local(x+1,0,sol,done)
            else:
                return local(x,idx+1,sol[:-1],done)
    return local(0,0,[],[])

def valide(nbK,nbS,sol):

    # teste si une solution partielle a des chances d'etre correcte
    #
    # @param nbK: nombre de classe
    # @param nbS: nombre de sommets
    # @param sol: solution partielle
    # @return: True si ca peut marcher

    import math
    n = int(math.ceil(nbS * 1. / nbK))
    l = [ sol.count(_) for _ in range(nbK) ]
    _rep = True
    i = 0
    while i < nbK and _rep :
        _rep = l[i] <= n
        i += 1
    return _rep

def rec2(nbK,nbS):

    # Calcule l'ensemble des solutions pour le partionnement de nSommets
    # en nClasses. Methode avec gestion de pile integree
    #
    # @param nbK: nombre de classes
    # @param nbS: nombre de sommets
    # @return: listes des solutions acceptables

    toDo = [ (0,0,[]) ]
    done = [ ]
    sol = [ ]
    while toDo != [ ] :
        x,i,sol = toDo.pop(0)
        if x >= nbS :
            done.append(sol)
            i = sol[-1] + 1
            toDo.insert(0,(x-1,i,sol[:-1]))
        elif i >= nbK :
            if x != 0 :
                i = sol[-1] + 1
                toDo.insert(0,(x-1,i,sol[:-1]))
            else:
                assert toDo == [ ], "%s should be empty" % toDo
        else:
            sol.append(i)
            if valide(nbK,nbS,sol):
                toDo.insert(0,(x+1,0,sol))
            else:
                toDo.insert(0,(x,i+1,sol[:-1]))
    return done

if __name__ == '__main__' :
    for nSommets in (3,4,7):
        for nClasses in (3,2,5):
            assert len(getSoluces(nSommets,nClasses)) == nClasses ** nSommets
            print('.'),
            try:
                _ll = rec2(nClasses,nSommets)

                _l = rec(nClasses,nSommets)
                print(_l)
                assert _l  == _ll
                print('$'),
            except Exception as _e:
                print("%d %d" % (nSommets,nClasses)),
            finally:
                print("size : %d < %d " % (len(_ll),nClasses ** nSommets))
    print(get_random_soluce(20,3))