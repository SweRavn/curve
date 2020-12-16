# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 15:23:57 2019

@author: rore
"""

from numpy import sqrt, cos, sin, arctan, pi, arctan2
from matplotlib.pyplot import gca

def plot_vectors(ax=None):
    plot_points(ax, vector=True)

def plot_points(ax=None, vector=False):
    for p in _points:
        if p.name != "":
            p.plot(ax, text=p.name, vector=vector)

_points = list()

class Point:
    count = 0
    def __init__(self, x, y, name=''):
        if name != '':
            _points.append(self) # Do not add name-less points
            self.name = name
        else:
            self.name = f'P{Point.count}'
        self._p = (x, y)
        Point.count += 1
    
    def __str__(self):
        return self.name+f'({self.x}, {self.y})'

    def __repr__(self):
        return self.name+f'({self.x}, {self.y})'

    @property
    def x(self):
        return self._p[0]

    @property
    def y(self):
        return self._p[1]
    
    @property
    def mag(self):
        return sqrt(self.x**2+self.y**2)
    
    def __abs__(self):
        return self.mag
    
    @property
    def p(self):
        return self._p
    
    @property
    def n(self):
        """
        Self normalized
        """
        return self/self.mag
    
    @property
    def theta(self):
        """
        @return Angle of point in cartesian coordinate system.
        """
        print("Warning: property theta is deprecated. Use arg instead.")
        if self.x != 0:
            return arctan(self.y/self.x)
        else:
            return pi/2
        
    @property
    def arg(self):
        return arctan2(self.y, self.x)
    
    def rotation(self, theta, point):
        """
        @return self rotated and angle @param theta radians around @param point
        """
        return Point(cos(theta)*(self.x-point.x)-sin(theta)*(self.y-point.y), sin(theta)*(self.x-point.x)+cos(theta)*(self.y-point.y))+point
    
    def rotate(self, theta, point):
        """
        Rotate self an angle @these around a point @point
        """
        p = self.rotation(theta, point)
        self._p = (p.x, p.y)

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
        l = l.n
        if u is None:
            u = Point(0,0)
        b = u - (u.dot(l))*l
        p = self-b
        return 2*p.dot(l)*l - p+b

    def reflect(self, l, u=None):
        """
        Reflect self in line l,u.
        """
        p = self.reflection(l, u)
        self._p = (p.x, p.y)
    
    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Point(x,y)
    
    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        return Point(x,y)
    
    def __div__(self, n):
        return Point(self.x/n, self.y/n)
        
    def __lt__(self, other):
        self_mag = (self.x ** 2) + (self.y ** 2)
        other_mag = (other.x ** 2) + (other.y ** 2)
        return self_mag < other_mag
    
    def __gt__(self, other):
        self_mag = (self.x ** 2) + (self.y ** 2)
        other_mag = (other.x ** 2) + (other.y ** 2)
        return self_mag > other_mag

    def __neg__(self):
        return Point(-self.x, -self.y)
    
#    def __le__:
#    def __ge__:
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not self==other
    
    def __mul__(self, scalar):
        return Point(self.x*scalar, self.y*scalar)
        
    __rmul__ = __mul__
    
    def __truediv__(self, scalar):
        return self*(1/scalar)
    
    def __getitem__(self, index):
        return self._p[index]

    def plot(self,
             ax=None,
             text=None,
             vector=False,
             linecolor=None,
             marker='.',
             markercolor=None,
             ):
        if ax is None:
            ax = gca()
        if vector is False:
            vector=Point(0,0)
            ax.plot([self.x], [self.y], linewidth=0, marker=marker, color=markercolor)
        else:
            ax.plot([vector.x, vector.x+self.x], [vector.y, vector.y+self.y], linewidth=1, color=linecolor)
            ax.plot([vector.x+self.x], [vector.y+self.y], linewidth=1, marker=marker, color=markercolor)
        if text is not None:
            ax.text(vector.x+self.x, vector.y+self.y, ' '+text)
    