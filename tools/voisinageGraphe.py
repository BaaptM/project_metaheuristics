#!/usr/bin/python
# *-* coding: utf-8 -*-
# $Id: voisinageGraphe.py,v 1.8 2012/03/27 18:01:55 mmc Exp $
#


# Notion de voisinages :
#     - On dispose d'une situation de depart
#     - On peut prendre un element et le mettre ailleurs (Pick'n'Drop)
#     - On peut soit prendre deux elements et les echanger (Swap)
#     - On peut faire une permutation circulaire (Sweep)
#
# Convention de nommage :
#     - XXX_one : renvoie un exemplaire
#     - delta_XXX : renvoie le mouvement elementaire
#     - XXX_name_YYY : name est le nom du voisinage
#     - XXX_gen : renvoie un iterateur


__author__ = "mmc <marc.corsini@u-bordeaux2.fr>"

#---- import ---------
import random
import copy
import itertools
#---------------------

def delta_swap_one(partition):

    # renvoie un mouvement elementaire dans le cas du Swap
    # @param partition: une liste de listes
    # @return: ( (K_i,K_j),(x_from_K_i,y_from_K_j) )

    _sz = len(partition)
    _select = tuple(random.sample(range(_sz),2))
    _un = partition[_select[0]]
    _deux = partition[_select[1]]
    _x = random.choice(_un)
    _y = random.choice(_deux)
    return _select,(_x,_y)

def swap_one(partition):

    # renvoie une nouvelle partition apres swap
    # @param partition: une liste de listes
    # @return: une nouvelle partition

    _next = copy.deepcopy(partition)
    (i,j),(x,y) = delta_swap_one(partition)
    _un = _next[i]
    _deux = _next[j]
    _un.remove(x)
    _un.append(y)
    _deux.remove(y)
    _deux.append(x)
    return _next

def delta_swap_gen(partition):

    # iterateur sur les mouvements elementaires d'un swap
    # @param partition: partition initiale
    # @return: le mouvement suivant

    _sz = len(partition)
    for i in xrange(_sz-1):
        for j in xrange(i+1,_sz):
            for x in partition[i]:
                for y in partition[j] :
                    yield ( (i,j),(x,y) )
    raise StopIteration

def swap_gen(partition):

    # iterateur sur les partitions obtenues par swap
    # @param partition: partition initiale
    # @return: partition suivante

    _start = copy.deepcopy(partition)
    _gen = delta_swap_gen(partition)
    for (i,j),(x,y) in _gen :
        _current = copy.deepcopy(_start)
        _current[i].remove(x)
        _current[i].append(y)
        _current[j].remove(y)
        _current[j].append(x)
        yield _current


def delta_pick_one(partition):

    # renvoie un mouvement elementaire dans le cas du Pick'n'Drop
    # @param partition: une liste de listes
    # @return: ( (K_i,K_j), x in K_i)

    _sz = len(partition)
    _select = tuple(random.sample(range(_sz),2))
    _un = partition[_select[0]]
    _x = random.choice(_un)
    return _select,_x

def pick_one(partition):

    # renvoie une nouvelle partition apres pick'n'drop
    # @param partition: une liste de listes
    # @return: une nouvelle partition

    _next = copy.deepcopy(partition)
    (i,j),x = delta_pick_one(partition)
    _un = _next[i]
    _deux = _next[j]
    _un.remove(x)
    _deux.append(x)
    return _next

def delta_pick_gen(partition):

    # iterateur sur les mouvements elementaires d'un pick'n'drop
    # @param partition: partition initiale
    # @return: le mouvement suivant

    _sz = len(partition)
    for i in xrange(_sz):
        for j in xrange(_sz):
            if i == j : continue
            for x in partition[i]:
                yield ( (i,j), x )
    raise StopIteration

def pick_gen(partition):

    # iterateur sur les partitions obtenues par pick'n'drop
    # @param partition: partition initiale
    # @return: partition suivante

    _start = copy.deepcopy(partition)
    _gen = delta_pick_gen(partition)
    for (i,j),x in _gen :
        _current = copy.deepcopy(_start)
        _current[i].remove(x)
        _current[j].append(x)
        yield _current

def delta_sweep_one(partition):

    # renvoie un mouvement elementaire dans le cas du Sweep
    # @param partition: une liste de listes
    # @return: (x1_from_K1, x2_from_K2, ..., xn_from_Kn)

    _chooser = lambda x: random.choice(x)
    _rep = tuple(map(_chooser,partition))
    return _rep

def sweep_one(partition):

    # renvoie une nouvelle partition apres sweep
    # @param partition: une liste de listes
    # @return: une nouvelle partition

    _current = copy.deepcopy(partition)
    _rep = delta_sweep_one(partition)
    _sz = len(_rep)
    for i,x in enumerate(_rep):
        _current[i].remove(x)
        _current[ (i+1) % _sz ].append(x)
    return _current
    
def delta_sweep_gen(partition):

    # iterateur sur les mouvements elementaires d'un sweep
    # @param partition: partition initiale
    # @return: le mouvement suivant

    _current = tuple(partition)
    return itertools.product(*_current)

def sweep_gen(partition):

    # iterateur sur les partitions obtenues par sweep
    # @param partition: partition initiale
    # @return: partition suivante

    _start = copy.deepcopy(partition)
    _gen = delta_sweep_gen(partition)
    _sz = len(partition)
    for x in _gen :
        _current = copy.deepcopy(_start)
        for i,y in enumerate(x):
            _current[i].remove(y)
            _current[ (i+1) % _sz ].append(y)
        yield _current

def build_gen(name,sizeVoisinage,partition,nBloc=1):

    # Fonction generatrice
    # @param name: le nom du voisinage
    # @param sizeVoisinage: sa taille
    # @param partition: la partition initiale
    # @param nBloc: [defaut B{1}] le nombre de blocs
    # @return: une liste d'iterateurs

    _slice = sizeVoisinage / nBloc
    _genLst = []
    _meth = name + '_gen'
    for i in range(nBloc - 1) :
        _start = i * _slice
        _genLst.append( itertools.islice(eval(_meth)(partition),
                                         _start, _start + _slice) )
    _genLst.append( itertools.islice(eval(_meth)(partition),
                                     _slice*(nBloc-1),
                                     sizeVoisinage) )
    return _genLst

def nth_gen(name,szVoisinage,partition,numBloc,nBloc):

    # accesseur sur le generateur du nieme bloc
    # @param name: swap, pick, sweep
    # @param szVoisinage: taille du voisinage
    # @param partition: la partition courante
    # @param numBloc: le numero du bloc a generer B{Attention} a partir de 0
    # @param nBloc: le nombre de blocs
    # @return: le generateur associe

    assert(numBloc in xrange(nBloc))
    _slice = szVoisinage / nBloc
    _meth = name+'_gen'
    _start = _slice * numBloc
    if numBloc == nBloc - 1 : # c'est le dernier
        _stop = szVoisinage
    else:
        _stop = _start + _slice
    return itertools.islice(eval(_meth)(partition),_start,_stop)

def make_dico_size(partition):

    # A partir d'une partition on calcule la taille du voisinage
    # @param partition: partition initiale

    # dimensions des partitions
    _dim = [ len(x) for x in partition ]
    # tailles des voisinages
    _vsize = { 'swap': 0,
               'pick': 0,
               'sweep': 1}
    for key in _vsize :
        _meth = '__'+key+'_size' # on cree le nom de la fonction
        _vsize[key] = eval(_meth)(_dim,_vsize[key])
    return _vsize

def __swap_size(dim,score):

    # methode privee: appelee par make_dico_size
    # renvoie la taille du voisinage de type swap

    _cpt = score
    for i in range(len(dim)-1):
        for j in range(i+1,len(dim)):
            _cpt += dim[i]*dim[j]
    return _cpt


def __pick_size(dim,score):

    # methode privee: appelee par make_dico_size
    # renvoie la taille du voisinage de type pick

    _cpt = score
    _cpt = sum(dim)*(len(dim) - 1)
    return _cpt


def __sweep_size(dim,score):

    # methode privee: appelee par make_dico_size
    # renvoie la taille du voisinage de type sweep

    _cpt = score
    for i in range(len(dim)): _cpt *= dim[i]

    return _cpt

if __name__ == '__main__' :
    # une partition
    p = [ range(3),['a','b'],range(5,9) ]
    vsize = make_dico_size(p)
    
    print('p> %r' % p)
    print('swap> %r' %swap_one(p))
    swap_v = swap_gen(p)
    print('il y a %d possibilités, attendu %d ' % (len(list(swap_v))),
                                                   vsize['swap'])
    print('pick> %r' % pick_one(p))
    pickNdrop_v = pick_gen(p)
    print('il y a %d possibilités, attendu %d ' % (len(list(pickNdrop_v))),
                                                   vsize['pick'])
    print('sweep> %r' % sweep_one(p))
    sweep_v = sweep_gen(p)
    print('il y a %d possibilités, attendu %d ' % (len(list(sweep_v))),
                                                   vsize['sweep'])

    # on cree les générateurs par blocs
    nBloc = 5
    gen_v = {}
    for key in vsize :
        gen_v[key] = build_gen(key,vsize[key],p,nBloc)

    # on crée le dernier générateur
    last_generator = {}
    for key in vsize :
        last_generator[key] = nth_gen(key,vsize[key],p,nBloc-1,nBloc)
        
    for key in gen_v :
        v = [len(list(x)) for x in gen_v[key]]
        print('%s : %r got %d expected %d' % (key,v,sum(v),vsize[key]))
        # on verifie que le dernier de gen_v[key] est last_generator[key]
        # verification sur la taille seulement
        assert (len(list(last_generator[key])) == v[-1])
        print('.')
