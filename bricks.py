# -*- coding: utf-8 -*-

import itertools 
import math
import numpy as np
import random

# Choose the bricks to be enumerated

pieces = [(2,2)]*1  +[(1,1)]*4  #+ [(3,1)]*1
#pieces = [(2,1)]*5 # +[(1,1)]*1 
#pieces = [(1,1) , (1,2) , (1,3) , (2,4) ] 

# create all the sets from 1 to the total of bricks
powerset = itertools.chain.from_iterable(itertools.combinations(pieces, r) for r in range(len(pieces)+1))
powerset = set(powerset)
powerset = list(powerset)
powerset.sort(key =lambda a: len(a))

# enumerate all the permutations for each susbset
perm = [ itertools.permutations(s) for  s in powerset]
perm = perm[-1:]

hashes = set()


q = np.zeros(10)
q[0] = 1

# some random-ish numbers to compute unique fingerprint of configurations

def sqrt(c): return math.sqrt(c)
S2, S3, S5, S7, S11 = sqrt(2), sqrt(3), sqrt(5), sqrt(7),sqrt(11)



"""This function calculates a unique hash that is invariant under rotations and mirrors (if wanted).
It achieve this by getting the x,y,z-distance of each brick to the center of mass and 
multuplying the coordinates the irrational factors before. Then it sums all in a big integer. 
The sum, by being order-invariant, erases ordering of the original list"""

def calc_hash(aa):

    if len(aa) ==0:
        return None
    a = np.array(list(aa))
    N = a.shape[0]

    # center of mass -translation
    am = np.mean(a, axis=0)
    a = a - am 
    sign = lambda x: 1 if x>=0 else -1


        #reflection
    x,y,z = a[:,1], a[:,2], a[:,0]
    fx= np.sum( np.sign(x)*(S2 + abs(x))*(S3+abs(y))*(S5+z))
    fy= np.sum( np.sign(y)*(S2 + abs(y))*(S3+abs(x))*(S5+z))
    x *= sign(fx)
    y *= sign(fy)
    if abs(fy) > abs(fx):
         x,y = y,x

        # break 45 degree symmetry
    if abs(fx)<0.01 and abs(fy)<0.01:   
        fxy = np.sum( np.sign(x*y)*(S2 + abs(x))*(S3+abs(y))*(S5+z))
        if fxy<0:         
            x = -x

    def r(i): return np.floor(i + np.sign(i)*0.001)
    ret = np.sum( (S2 + r(x))*(S3+r(y))*(S5+r(z)))
    return int(1000*ret)
   

# recursively adds bricks from 'lst' to the 'added', 
# where 'free_points are possible attachment positions and 'occupied' are filled coordinates

def add(lst, added, free_points, occupied):

    if len(lst)==0:   # already added all
        h = calc_hash(occupied)  
        if h is not None:
            hashes.add(h)  
    else:    
       piece = lst[0]
       
       for pos in free_points:           
           h, posx, posy = pos
          
           if h < 0:
               continue
               
               # add a brick of size dx-dy at the position px, py and height h
           def addPiece(px, py, h, dx,dy):  
               
               # checks if it can fit
               for p,q in itertools.product(range(px, px+dx),range( py, py+dy)):
                   if (h,p,q) in occupied:
                       return
                       
               free_points1 = free_points.copy()  
               occupied1 = occupied.copy()    
               added1 = added.copy()   
               
               # the new brick creates new free points
               for p,q in itertools.product(range(px, px+dx),range( py, py+dy)):                   
                   free_points1.add( (h+1, p,q) )
                   free_points1.add( (h-1, p,q) )
                   occupied1.add((h, p,q))  
                  
               added1.append((px+dx/2,py+dy/2, dx,dy,h))                    
               add(lst[1:], added1, free_points1, occupied1)
           
           for p,q in itertools.product(range(posx-(piece[0]-1), posx+1), range(posy-(piece[1]-1), posy+1)):             
               addPiece(p, q, h,piece[0], piece[1])
           for p,q in itertools.product(range(posx-(piece[1]-1), posx+1), range(posy-(piece[0]-1), posy+1)):
               addPiece(p, q, h,piece[1], piece[0])

                 

# function to add to hash list all configurations obtainable from a given list of bricks
# You put brick B0 at origin, then attach B1 on it, then B2 on these, and so on
# => there are lots of speed-ups possible here

def calc(perm1):               
    for i in set(perm1):
        lst = [ (0,0,0)]
        add(list(i), [], set(lst), set())

#finally, we start at a empty set of hashes and iterate over all possible permutations

for perm1 in perm:
    z = set(perm1)
    n = len(hashes) 
    calc(z)
    print (len(hashes)-n, list(z)[0])
    

# uncomment to list all hashes
#for i in hashes:
#    print (i)
print (len(hashes))   # how many configurations there are in total?
