# -*- coding: utf-8 -*-
"""
Created on Sat Nov 23 07:39:02 2019

@author: rore
"""

from ..curve import MultiCurve, Curve
from ..fillet import fillet
from numpy import int, array, mod, arange
from ..point import Point

class Polygon(Curve):
    """
    A polygon is parametrized by integers that run from 0 to number of points in the polygon.
    @param closed If True, adds a final point equal to the first point if there is no such point to close the polygon.
    """
    def __init__(self, points, *args, name='Polygon', **kwargs):
        super().__init__(*args, name=name, points=points, s1=0, s2=len(points)-1, n=len(points), **kwargs)
    
    def _x(self, s):
        try:
            s = [int(i) for i in s]
            x = array([self.points[i].x for i in s])
#            x = array([p.x for p in self.points[s]])
            return x
        except:
            return self.points[int(s)].x

    def _y(self, s):
        try:
            s = [int(i) for i in s]
            y = array([self.points[i].y for i in s])
#            y = array([p.y for p in self.points[s]])
            return y
        except:
            return self.points[int(s)].y            
    
    def _plot_support(self, ax):
        pass
    
    def __getitem__(self, s):
        """
        Fetches points in self
        @param s slice.
        """
#        if i >= len(self.points):
#        try:
#            i = mod(i,len(self.points))
#            s = [int(s) for s in i]
#        except:
#            s = int(i)
        return self.points[s]

    def fillet(self, r=1, N=None):
        """
        Create fillets on corners with index from N. Dafault all
        """
        fillets = list()
        if N is None:
            N = arange(self.n-2)+1
            for n in N:
                fillets.append(fillet(self[n], self[n-1], self[n+1], r))
            if self.closed:
                fillets.append(fillet(self[0], self[self.n-1], self[1], r))
                fillets.append(fillet(self[self.n-1], self[self.n-2], self[0], r))
        return fillets
        