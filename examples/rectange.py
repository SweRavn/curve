# -*- coding: utf-8 -*-
"""
Create a rectange using a polygone and add fillets to the inner corners.
"""

from curves.point import Point
from curves.curves.polygon import Polygon
from curves.curve import plot_curves
from curves.point import plot_points
from curves.export import export
from matplotlib.pyplot import gca, show, axis, grid

w = 1 # Rectange width
h = 0.7 # Rectange height

# Create all points:
p1 = Point(0, 0, name='p1')
p2 = Point(w, 0, name='p2')
p3 = Point(w, h, name='p3')
p4 = Point(0, h, name='p4')

# Create the curve:
rectange = Polygon([p1, p2, p3, p4], name='rectange', closed=False)
r2 = rectange.fillet(r=0.2*w)

# Buid the data set:
data = rectange.data()

ax = gca()
plot_curves(ax)
plot_points(ax)
#ax.plot(data[0,:], data[1,:])
axis('equal')
grid(True)
show()

export(data, 'rectange')
