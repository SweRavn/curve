# -*- coding: utf-8 -*-
"""
Created on Sat Nov 23 07:39:02 2019

@author: rore
"""

from ..curve import MultiCurve, Curve
from ..fillet import fillet
from numpy import int, array, mod, arange, pi, cos, sin, linspace
from ..point import Point
from .. import CurvesException

def rectange_Polygon_factory(w=1, h=1, ll=None, c=None, name='rectange', **kwargs):
    """
    Build a rectange.
    
    @param w Width
    @param h Heigh
    @param ll Lower left corner
    @param c Center
    @param name Name of resulting Polygon
    If neither ll or c are given, rectange is created with c=Point(0,0).
    """
    if c is not None:
        ll = c - Point(w/2, h/2)
    if ll is None:
        ll = Point(0,0)
    return Polygon([ll, ll+Point(w, 0), ll+Point(w, h), ll+Point(0, h)], name=name, closed=True, **kwargs)

def even_closed_Polygon_factory(n=3, r=1, alpha=0, name='closed polygon', **kwargs):
    """
    Build an even closed Polygone.
    
    @param n Number of sides
    @param r Radius of Polygone
    @param alpha Initial angle
    @param name Name of resulting Polygon
    """
    da = 2*pi/n
    n = range(n)
    return Polygon([Point(r*cos(da*i+alpha), r*sin(da*i+alpha)) for i in n], name=name, closed=True, **kwargs)

def from_Polygons_Polygon_factory(polygons, closed=True, **kwargs):
    """
    Creates a single polygons from a list of polygons. self.points are simply concatinated.
    """
    points = list()
    for polygon in polygons:
        points += polygon.points
    return Polygon(points, closed=True, **kwargs)

def from_Curves_Polygon_factory(curves, closed=True, **kwargs):
    """
    Create a single polygon from a list of curves.
    """
    points = list()
    for curve in curves:
        points += curve.render_points()
    return Polygon(points, closed=closed, **kwargs)

def from_multiCurve_Polygon_factory():
    raise Exception("Not implemented")    

class Polygon(Curve):
    """
    A polygon is parametrized by integers that run from 0 to number of points in the polygon.
    """
    def __init__(self, points, *args, name='Polygon', **kwargs):
        super().__init__(*args,
                         name=name,
                         points=points,
                         s1=0,
                         s2=len(points)-1,
                         n=len(points),
                         **kwargs)
    
    def _x(self, s):
        try:
            s = [int(i) for i in s]
            x = array([self.points[i].x for i in s])
            return x
        except:
            return self.points[int(s)].x

    def _y(self, s):
        try:
            s = [int(i) for i in s]
            y = array([self.points[i].y for i in s])
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
        return self.points[s]

    def fillets(self,
               r=1, # Fillet radius
               N=None, # Indices to perform fillet on
               ):
        """
        Create fillets on corners with index from N. Dafault all.
        @return a list with all created fillets
        """
        fillets = list()
        if N is None:
            ns = arange(self.n-2)+1
        else:
            ns = N
        for n in ns:
            try:
                fillets.append(fillet(self[n], self[n-1], self[n+1], r))
            except CurvesException:
                pass
        if self.closed and N is None:
            try:
                fillets.append(fillet(self[self.n-1], self[self.n-2], self[0], r))
            except CurvesException:
                pass
            try:
                fillets.append(fillet(self[0], self[self.n-1], self[1], r))
            except CurvesException:
                pass
        return fillets
    
    def fillet(self,
               n, # Index to perform fillet on
               r=1, # Fillet radius
               s=None):
        if n == 0:
            f = fillet(self[0], self[self.n-1], self[1], r)
        elif n == len(self.points):
            f = fillet(self[self.n-1], self[self.n-2], self[0], r)
        else:
            f = fillet(self[n], self[n-1], self[n+1], r)
        points = f[0].render_points(s)
        self.points = self.points[:n] + [f[1]] + points + [f[2]] + self.points[n+1:]
        self._n = len(self.points)
        self.s2 = self.n-1
        self._a = linspace(self.s1, self.s2, self.n)
