# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 12:16:08 2019

@author: Robert Rehammar

A module for generating parametric curves.
"""

from numpy import array, concatenate, linspace, sqrt, ndarray, sum
from matplotlib.pyplot import gca
from .point import Point

def plot_curves(ax=None,
                xy=None):
    if ax is None:
        ax = gca()
    for c in _curves:
        c.plot(ax)
        c.plot_name(ax, xy)

_curves = list()

class MetaCurve(type):
    def __call__(cls, *args, **kwargs):
        instance = super().__call__(*args, **kwargs)
        instance.finish(*args, **kwargs)
        return instance
        
class Curve(metaclass=MetaCurve):
    """
    Base class for holding a curve. A curve is a parametrized object that renders to a polygon. Curve holds the basic functioanlity to render the curve to an array of points that can be manipulated in other ways.
    @param closed If True, the curve is rendered closed by joining the first and last point.
    
    """
    counter = 0
    def __init__(self, *args,
                 s1=0, s2=1,
                 points=list(),
                 n=100,
                 name='',
                 closed=False,
                 linecolor=None, # Color of curve when plotted
                 linestyle=None, # Lie style of curve when plotted
                 **kwargs):
        if name != '':
            _curves.append(self) # Do not add name-less curves
            self.name = name
        else:
            self.name = f'C{Point.count}'
        self.s1 = s1 # First point in sweep
        self.s2 = s2 # Second point in sweep
        self._n = n
        self._a = linspace(self.s1, self.s2, self.n)
        self.points = points.copy()
        self.closed = closed
        self.linecolor=linecolor
        self.linestyle=linestyle
        
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.name
    
    def finish(self, *args, **kwargs):
        """
        This function is run after the childs __init__ is run and is used for
        initiations functionality that needs to be done after the full child
        functionlaity is in place.
        """
        if 't' in kwargs:
            t = kwargs['t']
            del kwargs['t']
        else:
            t=Point(0,0)
        if 'phi' in kwargs:
            phi = kwargs['phi']
            del kwargs['phi']
        else:
            phi = 0
        if 'C' in kwargs:
            C = kwargs['C']
            del kwargs['C']
        else:
            p1 = Point(self._x(self.s1),self._y(self.s1))
            p2 = Point(self._x(self.s2),self._y(self.s2))
            C = Point((p2.x-p1.x)/2, (p2.y-p1.y)/2) # Default rotation center is geometrical center of endpoints of curve.
        self.rotate(phi, C)
        self.translate(t)
        Curve.counter += 1 # Use this to name unnamed curves.
    
    @property
    def center(self):
        """
        Center of curve, computed from all points.
        """
        return Point(sum(self.x()), sum(self.y()))/self.n
    
    def translate(self, t):
        self.t = t
        
    def rotate(self,
               phi = 0,
               C = None):
        """
        Rotate the curve an angle phi around the point C.
        """
        if C is None:
            C = self.center
        self._phi = phi
        self._C = C
        if len(self.points) == 0:
            raise Exception('Rotation support is not implemented for '+self.__class__.__name__)
        else:
            for point in self.points:
                point.rotate(phi, C)
    
    def reflect(self, l, u=None):
        """
        Reflect self in a line defiend by direction l and going through point u.
        """
        if len(self.points) == 0:
            raise Exception('Reflection support is not implemented for '+self.__class__.__name__)
        else:
            for point in self.points:
                point.reflect(l, u)
    
    @property
    def n(self):
        """
        Number of points in array.
        """
        return self._n
    
    def s(self, s=None):
        """
        @param s Either an array-like object of parameter values, None to let the curve generate the parameters from default or a slice to slice the default list.
        """
        if s is None:
            if self.closed:
                return concatenate((self._a, array([self._a[0]])))
            else:
                return self._a
        elif type(s) is slice:
            return self._a[s]
        else:
            return s
    
    def ds(self, s=None):
        """
        @param: Same as in s(self, s)
        @return The difference between the parameter s datapoints. If
        len(s) = n, the length of the returned array is n-1.
        """
        s = self.s(s)
        return s[1::] - s[:-1:]
    
    def data(self, s=None):
        s = self.s(s)
        return array((self.x(s), self.y(s)))

    def render_points(self, s=None):
        """
        @return A list of Points which corresponds to the rendered curve. This can for example be used to create a Polygon with.
        """
        return [Point(p[0], p[1]) for p in self.data(s).T]
        
    def append_to(self, a, s=None):
        if s is None:
            ae = a[:,-1]
            if sum((ae-self.data(self.s2))**2) < sum((ae-self.data(self.s1))**2):
                s = slice(-1, None, -1)
        s = self.s(s)
        return concatenate((a, self.data(s)), axis=1)
    
    def append_stroke_to(self, a, s=None, w=None):
        s = self.s(s)
        return concatenate((a, self.stroke(s, w)), axis=1)
    
    def x(self, s=None):
        s = self.s(s)
        return self._x(s) + self.t.x

    def y(self, s=None):
        s = self.s(s)
        return self._y(s) + self.t.y

    def _x(self, s):
        raise Exception('Not implemented!')

    def _y(self, s):
        raise Exception('Not implemented!')

    def dx(self, s=None):
        """
        Nummeric x-derivative of the curve. Can be overided by analytical
        implementation of any particular child class.
        Can handle input as ndarray or scalar.
        Returned data has same length or type as s.
        End-points are single-sided extrapolated, internal points are
        interpolated.
        """
        s = self.s(s)
        if isinstance(s, ndarray):
            ds = self.ds(s)
            x = self.x(s)
            dx0 = (x[1::]-x[:-1:])/ds
            return concatenate(([dx0[0]], (dx0[1::]+dx0[:-1:])/2, [dx0[-1]]))
        else:
            ds = 1e-5
            return (self.x(s+ds/2)-self.x(s-ds/2))/ds

    def dy(self, s=None):
        """
        Nummeric y-derivative of the curve. Can be overided by analytical
        implementation of any particular child class.
        Can handle input as ndarray or scalar.
        """
        s = self.s(s)
        if isinstance(s, ndarray):
            ds = self.ds(s)
            y = self.y(s)
            dy0 = (y[1::]-y[:-1:])/ds
            return concatenate(([dy0[0]], (dy0[1::]+dy0[:-1:])/2, [dy0[-1]]))
        else:
            ds = 1e-5
            return (self.y(s+ds/2)-self.y(s-ds/2))/ds
    
    def tx(self, s=None):
        """
        x-component of curve tanget = derivative normalized to length 1.
        """
        s = self.s(s)
        return self.dx(s)/sqrt(self.dx(s)**2 + self.dy(s)**2)
    
    def ty(self, s=None):
        """
        x-component of curve tanget = derivative normalized to length 1.
        """
        s = self.s(s)
        return self.dy(s)/sqrt(self.dx(s)**2 + self.dy(s)**2)
        
    def nx(self, s=None):
        """
        x-component of curve normal. Normalized to 1
        """
        s = self.s(s)
        return self.ty(s)

    def ny(self, s=None):
        """
        x-component of curve normal. Normalized to 1
        """
        s = self.s(s)
        return -self.tx(s)
    
    def i(self, s=None):
        """
        Integral of curve along s.
        """
        s = self.s()
        print(s)
        dl = sqrt(self.dx(s)**2 + self.dy(s)**2)
        print(dl)
        return sum(dl)
    
    def stroke_x1(self, s=None, w=None):
        s = self.s(s)
        if w is None:
            return self.x(s)
        else:
            return self.x(s)+self.nx(s)*w(s)/2
    def stroke_x2(self, s=None, w=None):
        s = self.s(s)
        if w is None:
            return self.x(s)
        else:
            return self.x(s)-self.nx(s)*w(s)/2
        
    def stroke_y1(self, s=None, w=None):
        s = self.s(s)
        if w is None:
            return self.y(s)
        else:
            return self.y(s)+self.ny(s)*w(s)/2

    def stroke_y2(self, s=None, w=None):
        s = self.s(s)
        if w is None:
            return self.y(s)
        else:
            return self.y(s)-self.ny(s)*w(s)/2
        
    def stroke_x(self, s=None, w=None):
        s = self.s(s)
        if w is None:
            return self.x(s)
        else:
#            x1 = self.x(s)+self.nx(s)*w(s)/2
#            x2 = self.x(s)-self.nx(s)*w(s)/2
            return concatenate((self.stroke_x1(s,w), self.stroke_x2(s,w)[::-1]))
    
    def stroke_y(self, s=None, w=None):
        s = self.s(s)
        if w is None:
            return self.y(s)
        else:
#            y1 = self.y(s)+self.ny(s)*w(s)/2
#            y2 = self.y(s)-self.ny(s)*w(s)/2
#            return concatenate((y1, y2[::-1]))
            return concatenate((self.stroke_y1(s,w), self.stroke_y2(s,w)[::-1]))
    
    def stroke(self, s=None, w=None):
        """
        Generate a stroke with width according to the function w.
        """
        s = self.s(s)
        if w is None:
            return self.data(s)
        else:
            return array((self.stroke_x(s, w), self.stroke_y(s, w)))

    def plot_stroke(self, ax, s=None, w=None):
        s = self.s(s)
        data = self.stroke(s, w)
        ax.plot(data[0,:], data[1,:])

    def plot(self, ax=None, s=None, linecolor=None, linestyle=None):
        """
        Plot self on ax.
        """
        if ax is None:
            ax = gca()
        s = self.s(s)
        ax.plot(self.x(s), self.y(s),
                color=self.linecolor or linecolor,
                linestyle=self.linestyle or linestyle)
    
    def plot_support(self, ax):
        """
        Plot any supporting information about self.
        """
        self._plot_support(ax)
    
    def plot_name(self, ax=None, s=0.5, xy=None):
        if ax is None:
            ax = gca()
        if xy is not None:
            x, y = xy
        else:
            x, y = self.x(s), self.y(s)
        ax.text(x, y, self.name)
    
    def _plot_support(self, ax):
        raise Exception("Not implemented!")

class MultiCurve:
    """
    A MultiCurve is a container for several Curves.
    """
    def __init__(self, *args, **kwargs):
        if 'name' in kwargs:
            self.name = kwargs['name']
            del kwargs['name']
        else:
            self.name = ""
        self.curves = list()
    
    def plot(self, ax):
        for curve in self.curves:
            curve.plot(ax)
    
    def data(self):
        data = list()
        for curve in self.curves:
            data.append(curve.data())
        data = tuple(data)
        return concatenate(data, axis=1)
    
    def append(self, curve):
        self.curves.append(curve)
    
    def reflect(self, l, u=None):
        for curve in self.curves:
            curve.reflect(l, u)
