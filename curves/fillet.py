# -*- coding: utf-8 -*-
"""
Created on Sat Oct 31 06:14:23 2020

@author: rore
"""

from numpy import arccos, sin, pi, sqrt
from .curves.ellipse import Ellipse

def fillet(p, p1, p2, r):
    """
    Create a fillet at point p defined by points p1 and p2 and r.
    @return tripplet (e, a1, a2) where e is the arc of the ellipse defining the fillet arc, ai is the touching point towards pi.
    """
    p1 = p1 - p
    p2 = p2 - p
    
    t1 = p1.n # Direction of first point
    t2 = p2.n # Direction of seconed point
    c = (t1 + t2).n # Directoin in the middle of them
    
    theta = arccos(t1.dot(t2)) # Angle at point
    alpha = pi/2 - theta/2 # Complementary angle to theta
    z = r/sin(theta/2) # Distance to center of fillet ellipse
    a = sqrt(z**2 - r**2) # Distance to fillet start
    c = z*c # Fillet center
    a1 = a*t1 # Fillet touching point towards p1
    a2 = a*t2 # Fillet touching point towards p2
    
    s = (-c).arg# + 2*pi # add 2 pi to be certain not to wrap over negative angles
    s1 = s - alpha
    s2 = s + alpha
    
    d1, d2 = t1.arg, t2.arg # Used to sort the arguments
    
    return (Ellipse(r=r, s1=s2*(d1<=d2)+s1*(d2<d1), s2=s1*(d1<=d2)+s2*(d2<d1), t=c+p), a1+p, a2+p)
