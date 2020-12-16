# -*- coding: utf-8 -*-
"""
Created on Sat Nov 23 07:40:38 2019

@author: rore
"""

from numpy import cos, sin, pi
from .. import CurvesSettings
from ..curve import Curve
import traceback

# Ellipse curve
class Ellipse(Curve):
    def __init__(self,
                 r=1, # Radius if set to circle or a or b missing
                 a=None, # Major axis
                 b=None, # Minor axis
                 phi = 0, # Rotation angle
                 s1 = 0,
                 s2 = 2*pi,
                 name='Ellipse',
                 **kwargs):
        super().__init__(name=name, s1=s1, s2=s2, **kwargs)
        if a is None:
            a = r
        if b is None:
            b = r
        self.a = a
        self.b = b
        self.phi = phi
    def _x(self, s):
        return self.a*cos(self.phi)*cos(s) - self.b*sin(self.phi)*sin(s)
    def _y(self, s):
        return self.a*sin(self.phi)*cos(s) + self.b*cos(self.phi)*sin(s)
    def dx(self, s):
        return -self.a*cos(self.phi)*sin(s) - self.b*sin(self.phi)*cos(s)
    def dy(self, s):
        return -self.a*sin(self.ph)*sin(s) + self.b*cos(self.phi)*cos(s)
    @property
    def center(self):
        return self.t
    
    def rotate(self,
               phi = 0,
               C = None):
        if C is not None and CurvesSettings['verbosity']>0:
            traceback.print_stack()
            print("Warning: Rotating around a point different from the ellipse center is not implemented.")
            print("Rotatin center set to", C)
        self.phi = phi
        