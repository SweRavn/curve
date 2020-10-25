# -*- coding: utf-8 -*-
"""
Created on Sat Nov 23 07:39:02 2019

@author: rore
"""

from numpy import log, exp
from scipy.optimize import fsolve
from ..curve import Curve

class ExpX(Curve):
    def __init__(self, p1, p0y5x, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.p1 = p1
        self.p0y5x = p0y5x
        c = p1.x/p0y5x
        def f(x):
            return (x-1)/(x**(0.5) -1) - c
        x = fsolve(f, 0.25*p1.x)[0]
        self.k = 1/log(x)
        self.ds = -self.k*log(p1.x/(exp(1/self.k)-1))
    def _y(self, s):
        return self.p1.y*s
    def _x(self, s):
        return exp(-self.ds/self.k)*(exp(s/self.k)-1)
    def dy(self, s):
        return self.p1.y
    def dx(self, s):
        return exp(-self.ds/self.k)*exp(s/self.k)/self.k
    @property
    def pivot(self):
        return self.p0y5x+self.t.x, 0.5*self.p1.y+self.t.y # FIXME: show not operate with self.t
    
    def _plot_support(self, ax):
        px, py = self.pivot
        ax.plot([px], [py], marker='.', color='black', linewidth=0.5)

class ExpY(Curve):
    def __init__(self, p1, p0x5y, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expx = ExpX(p1, p0x5y)

    def _x(self, s):
        return self.expx.y(self, s)
    def _y(self, s):
        return self.expx.x(self, s)
    def dy(self, s):
        return self.expx.dx(self, s)
    def dx(self, s):
        return self.expx.dy(self, s)
    @property
    def pivot(self):
        return self.expx.pivot
    
    def _plot_support(self, ax):
        py, px = self.expx.pivot
        ax.plot([px], [py], marker='.', color='black', linewidth=0.5)
    