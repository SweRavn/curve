# -*- coding: utf-8 -*-
"""
Created on Sat Nov 23 07:41:22 2019

@author: rore
"""

from numpy import array
#from matplotlib.pyplot import plot
from ..curve import Curve
from ..point import Point

# Bezier functions
class Bezier3(Curve):
    def __init__(self, p0, p1, p2, p3, *args, **kwargs):
        self.p0 = p0
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        if 'name' in kwargs:
            name = kwargs['name']
            del kwargs['name']
        else:
            name = 'Bezier'
        super().__init__(*args, points=[self.p0, self.p1, self.p2, self.p3], name=name, **kwargs)
        
    def _x(self, s):
        return (1-s)**3*self.p0[0]+3*(1-s)**2*s*self.p1[0]+3*(1-s)*s**2*self.p2[0]+s**3*self.p3[0]
    def _y(self, s):
        return (1-s)**3*self.p0[1]+3*(1-s)**2*s*self.p1[1]+3*(1-s)*s**2*self.p2[1]+s**3*self.p3[1]
    def dx(self, s):
        return 3*(1-s)**2*(self.p1[0]-self.p0[0])+6*(1-s)*s*(self.p2[0]-self.p1[0])+3*s**2*(self.p3[0]-self.p2[0])
    def dy(self, s):
        return 3*(1-s)**2*(self.p1[1]-self.p0[1])+6*(1-s)*s*(self.p2[1]-self.p1[1])+3*s**2*(self.p3[1]-self.p2[1])
    
    def connect(self, c1, c2, s1=1, s2=1, m1=1, m2=1):
        """
        Connects the Bezier-curve to p1 of curve 1 and p2 of curve 2 so that
		 the derivative become continous.
        """
#        self.points[0] = self.p0 = Point(c1.x(s1), c1.y(s1))
#        self.points[1] = self.p1 = Point(c1.dx(s1)/3+c1.x(s1), c1.dy(s1)/3+c1.y(s1))
#        self.points[2] = self.p2 = Point(c2.dx(s2)/3+c2.x(s2), c2.dy(s2)/3+c2.y(s2))
#        self.points[3] = self.p3 = Point(c2.x(s2), c2.y(s2))
        self.connect_start(c1, s=s1, m=m1)
        self.connect_end(c2, s=s2, m=m2)

    def connect_start(self, c, s=0, m=1):
        """
        Connect the start of the Bezier curve to the point s on the curve c
        so that the derivative becomes continous.
        FIXME: can add so that one can state the level of continuity from 0-3
        and the function couls move the corresponding number of points.
        """
        self.points[0] = self.p0 = Point(c.x(s), c.y(s))
        self.points[1] = self.p1 = Point(m*c.dx(s)/3+c.x(s), m*c.dy(s)/3+c.y(s))

    def connect_end(self, c, s=0, m=1):
        """
        Connect the start of the Bezier curve to the point s on the curve c
        so that the derivative becomes continous.
        FIXME: can add so that one can state the level of continuity from 0-3
        and the function couls move the corresponding number of points.
        """
        self.points[2] = self.p2 = Point(m*c.dx(s)/3+c.x(s), m*c.dy(s)/3+c.y(s))
        self.points[3] = self.p3 = Point(c.x(s), c.y(s))
		
#    @property
#    def points(self):
#        return array([self.p0.p, self.p1.p, self.p2.p, self.p3.p, ])
	
    def _plot_support(self, ax):
        points = array([self.p0.p, self.p1.p, self.p2.p, self.p3.p, ])
        ax.plot(points[:,0], points[:,1], marker='.', color='black', linewidth=0.5)

