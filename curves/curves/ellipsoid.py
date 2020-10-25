# -*- coding: utf-8 -*-
"""
Created on Sat Nov 23 07:40:38 2019

@author: rore
"""

from numpy import cos, pi, sin
from ..curve import Curve

# Ellipsoid function
class Ellipsoid(Curve):
    def __init__(self, rx, ry, p, Tx=0, Ty=0):
        super().__init__(Tx, Ty)
        self.rx = rx
        self.ry = ry
        self.p = p
    def x(self, s):
        return self.rx*cos(s*pi/2 + self.p) + self.Tx
    def y(self, s):
        return self.ry*sin(s*pi/2 + self.p) + self.Ty
    def dx(self, s):
        return self.rx*sin(s*pi/2 + self.p)*pi/2
    def dy(self, s):
        return -self.ry*cos(s*pi/2 + self.p)*pi/2
