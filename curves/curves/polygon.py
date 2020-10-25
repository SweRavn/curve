# -*- coding: utf-8 -*-
"""
Created on Sat Nov 23 07:39:02 2019

@author: rore
"""

from ..curve import MultiCurve
from ..curves.line import Line

class Polygon(MultiCurve):
    def __init__(self, points, *args, closed=False, **kwargs):
        if 'name' in kwargs:
            name = kwargs['name']
            del kwargs['name']
        else:
            name = 'Polygon'
        super().__init__(*args, name=name, **kwargs)
        n = len(points)
        for k in range(n-1):
            self.curves.append(Line(points[k], points[k+1]))
        if closed:
            self.curves.append(Line(points[-1], points[0]))

    def _plot_support(self, ax):
        pass
#        px, py = self.pivot
#        ax.plot([px], [py], marker='.', color='black', linewidth=0.5)

    