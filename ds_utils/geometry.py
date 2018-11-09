import math, sys, os
import numpy as np

def grid_simplify(plst, resolution=10):
    d = {}
    if len(plst)<10:
        return plst
    plst = [[plst[i][0],plst[i][1],i] for i in range(len(plst))]
    for p in plst:
        pxy = "%i-%i"%(p[0]/resolution, p[1]/resolution)
        if not(pxy in d): d[pxy]=[]
        d[pxy].append(p)
    olst=[]
    for k in list(d.keys()):
        #d[k].sort(key=lambda x:x[2])
        olst.append(d[k][int(len(d[k])/2.0)])
    olst.sort(key=lambda x:x[2])
    olst.append(olst[0])
    return [p[:2] for p in olst]

def getxy(plst):
    x = np.array([plst[i][0] for i in range(len(plst))])
    y = np.array([plst[i][1] for i in range(len(plst))])
    return x,y

