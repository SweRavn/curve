# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 15:23:57 2019

@author: rore
"""

from numpy import sqrt, cos, sin, arctan, pi, arctan2

def plot_points(ax):
    for p in _points:
        if p.name != "":
            p.plot(ax, text=p.name)

_points = list()

class Point:
    count = 0
    def __init__(self, x, y, name=''):
        if name != '':
            _points.append(self) # Do not add name-less points
        self._p = (x, y)
        if name == "":
            self.name = f"P{Point.count}"
        else:
            self.name = name
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
    
    def rotate(self, theta):
        """
        @return self rotated and angle @param theta radians
        """
        return Point(cos(theta)*self.x-sin(theta)*self.y, sin(theta)*self.x+cos(theta)*self.y)
    
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
    