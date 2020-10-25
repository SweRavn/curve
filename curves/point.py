# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 15:23:57 2019

@author: rore
"""

from numpy import sqrt

def plot_points(ax):
    for p in _points:
        if p.name != "":
            p.plot(ax, text=p.name)

_points = list()

class Point:
    def __init__(self, x, y, name=""):
        self._p = (x, y)
        self.name = name
        _points.append(self) #FIXME: add that the point should be removed at some point since this will be a memory leake if not.
    
    @property
    def x(self):
        return self._p[0]

    @property
    def y(self):
        return self._p[1]
    
    @property
    def mag(self):
        return sqrt(self.x**2+self.y**2)
    
    @property
    def p(self):
        return self._p
    
    def dot(self, other):
        """
        The dot product of self with other.
        """
        return self.x*other.x + self.y*other.y
    
    def reflection(self, l, u=None):
        """
        @return: the point reflected in a line drawn by vector l going thorugh point u.
        @param l: vector in the direction of the line
        @param u: point on the line
        """
        if u is None:
            return 2*self.dot(l)*l/l.mag - self
        else:            
            lp = l-u
            return 2*(self-u).dot(lp)*lp/lp.mag - self

    def reflect(self, l, u=None):
        """
        Reflect self in line l,u.
        """
        p = self.reflection(l, u)
        self._p = (p.x, p.y)
    
    def __str__(self):
        if len(self.name) > 0:
            return "{}: ({},{})".format(self.name, self.x, self.y)
        else:
            return "({},{})".format(self.x, self.y)
    
    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Point(x,y)
    
    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        return Point(x,y)
        
    def __lt__(self, other):
        self_mag = (self.x ** 2) + (self.y ** 2)
        other_mag = (other.x ** 2) + (other.y ** 2)
        return self_mag < other_mag
    
    def __gt__(self, other):
        self_mag = (self.x ** 2) + (self.y ** 2)
        other_mag = (other.x ** 2) + (other.y ** 2)
        return self_mag > other_mag
    
#    def __le__:
#    def __ge__:
#    def __eq__:
#    def __ne__:
    def __mul__(self, scalar):
        return Point(self.x*scalar, self.y*scalar)
        
    __rmul__ = __mul__
    
    def __truediv__(self, scalar):
        return self*(1/scalar)
    
    def __getitem__(self, index):
        return self._p[index]
#        if index == 0:
#            return self.x
#        elif index == 1:
#            return self.y
#        else:
#            raise Exception('2D points only have 2 items, x, y, index is {}'.format(index))
    def plot(self, ax, text=None):
        ax.plot([self.x], [self.y], linewidth=0, marker='.', color='black')
        if text is not None:
            ax.text(self.x, self.y, ' '+text)
    