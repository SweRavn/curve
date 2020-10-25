# -*- coding: utf-8 -*-
"""
Created on Sat Nov 23 07:39:54 2019

@author: rore
"""

from ..curve import Curve

# Line segment:
class Line(Curve):
    def __init__(self, p1, p2, *args, **kwargs):
        if 'n' in kwargs:
            n = kwargs['n']
            del kwargs['n']
        else:
            n = 2
        if 'name' in kwargs:
            name = kwargs['name']
            del kwargs['name']
        else:
            name = 'Line'
        self.p1 = p1
        self.p2 = p2
        super().__init__(*args, n = n, points=[self.p1, self.p2], name=name, **kwargs)
    
    def _y(self, s):
        return self.p1.y + (self.p2.y-self.p1.y)*s

    def _x(self, s):
        return self.p1.x + (self.p2.x-self.p1.x)*s

    def dy(self, s):
        return (self.p2.y-self.p1.y)

    def dx(self, s):
        return (self.p2.x-self.p1.x)
