# -*- coding: utf-8 -*-
"""
Created on Sat Nov 23 07:41:22 2019

@author: rore
"""

from numpy import array, pi, cos, sin
from ..curve import Curve
from ..point import Point

# Bezier functions
class Spiral(Curve):
    def __init__(self, a0, *args, f=lambda x: x/(2*pi), df=None, **kwargs):
        if 'name' in kwargs:
            name = kwargs['name']
            del kwargs['name']
        else:
            name = 'Spiral'
        super().__init__(*args, name=name, **kwargs)
        self.a0 = a0 # Inital angle
        self.f = f # Growth rate function
        if df is None:
            ds = (self.s2 - self.s1)/1e5
            self.df = lambda s: (self.f(s+ds/2)-self.f(s-ds/2))/ds
        else:
            self.df = df
    def _x(self, s):
        return self.f(s)*cos(2*pi*s + self.a0)
    def _y(self, s):
        return self.f(s)*sin(2*pi*s + self.a0)
#    def dx(self, s):
#        return -self.f(s)*sin(2*pi*s + self.a0)*2*pi+self.df(s)*cos(2*pi*s + self.a0)
#    def dy(self, s):
#        return self.f(s)*cos(2*pi*s + self.a0)*2*pi-self.df(s)*sin(2*pi*s + self.a0)
    	
    def _plot_support(self, ax):
        ax.plot([-1], [-1], marker='.', color='black', linewidth=0.5)

