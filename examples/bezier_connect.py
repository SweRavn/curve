# -*- coding: utf-8 -*-
"""
Create two lines and a Bezier curve that connects to the lines.
"""

from curves.point import Point
from curves.curves.line import Line
from curves.curves.bezier import Bezier3
from curves.curve import plot_curves
from curves.point import plot_points
from matplotlib.pyplot import gca, show, axis, grid

w = 1 # Line length
h = 0.7 # Lines distance

# Create all points:
p1 = Point(0, 0, name='p1')
p2 = Point(w, 0, name='p2')
p3 = Point(w, h, name='p3')
p4 = Point(0, h, name='p4')

# Create the curve:
line1 = Line(p1, p2, name='line 1')
line2 = Line(p4, p3, name='line 2')
bezier = Bezier3(p2, (p2+p3)/2, (p2+p3)/2, p3, name='bezier')
bezier.connect(line1, line2)

ax = gca()
plot_curves(ax)
plot_points(ax)
axis('equal')
grid(True)
show()
