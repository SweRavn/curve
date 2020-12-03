# -*- coding: utf-8 -*-
"""
Created on Sat Nov 23 07:40:38 2019

@author: rore
"""

from numpy import cos, sin
from ..curve import Curve

# Ellipse function
class Ellipse(Curve):
    def __init__(self, r=1, rx=None, ry=None, name='Ellipse', **kwargs):
        super().__init__(name=name, **kwargs)
        if rx is None:
            rx = r
        if ry is None:
            ry = r
        self.rx = rx
        self.ry = ry
    def _x(self, s):
        return self.rx*cos(s)
    def _y(self, s):
        return self.ry*sin(s)
    def dx(self, s):
        return -self.rx*sin(s)
    def dy(self, s):
        return self.ry*cos(s)
