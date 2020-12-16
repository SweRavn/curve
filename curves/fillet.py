# -*- coding: utf-8 -*-
"""
Created on Sat Oct 31 06:14:23 2020

@author: rore
"""

from numpy import arccos, sin, pi, sqrt
from .curves.ellipse import Ellipse
#from .curves.polygon import Polygon
from . import CurvesSettings, CurvesException
import traceback

def fillet(p, # Fillet point
           p1, # First point of V
           p2, # Second point of V
           r, # Fillet radius
           n=10, # Number of points in the fillet Ellipse arc rendering
           ):
    """
    Create a fillet at point p defined by points p1 and p2 and r.
    @return tripplet (e, a1, a2) where e is the arc of the ellipse defining the fillet arc, ai is the touching point towards pi.
    """
    p1 = p1 - p
    p2 = p2 - p
    
    t1 = p1.n # Direction of first point
    t2 = p2.n # Direction of seconed point
    c = (t1 + t2) # Directoin in the middle of them, not normalized
    if c.mag == 0:
        # Trying to fillet along a straight line, raise an exception
        raise CurvesException(f"Cannot create fillet in point {p}, it is on a straight line.")
    
    theta = arccos(t1.dot(t2)) # Angle at point
    z = r/sin(theta/2) # Distance to center of fillet ellipse
    a = sqrt(z**2 - r**2) # Distance to fillet start
    c = z*c.n # Fillet center
    a1 = a*t1 # Fillet touching point towards p1
    a2 = a*t2 # Fillet touching point towards p2
    if (a1.mag > p1.mag or a2.mag > p2.mag) and CurvesSettings['verbosity']>0:
        traceback.print_stack()
        print("Warning: Fillet will break polygon since fillet radius is larger then distance to corner points.")
    b1 = a1 - c # Vector from fillet center to touching point 1
    b2 = a2 - c # Vector from fillet center to touching point 2
    
    s1 = b1.arg%(2*pi)
    s2 = b2.arg%(2*pi)
    if abs(s2-s1) > pi:
        if s1 > s2:
            s1 -= 2*pi
        else:
            s2 -= 2*pi

    return (Ellipse(r=r, s1=s1, s2=s2, t=c+p, n=n), a1+p, a2+p)

def chamfer(p, # Chamfer point
            p1, # First point of V
            p2, # Second point of V
            a1=1, # Distance to chamber point towards p1
            a2=1, # Distance to chamber point towards p2
            ):
    return [a1*(p1-p).n+p, a2*(p2-p).n+p, ]
