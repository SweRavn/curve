# Curves

*Disclaimer* This package is in an early development phase, and several features are avaialbe and functioning, but the package is not yet production-ready.

A package to generate parametric curves. Curves was designed to create paramertic curves and export them to suitable format for processing in other applications. The idea with the package is to treat curves at analytic objects and be able to do manipulation on those analytic objects and then export the result as an arbitrty resolution polygon. Exporting to a polygon is done by choice. This is a very simple format that any program that deals with geomertical/graphical elements can handle.

A Curve in `Curves` is a parametric object defined by a number or parameters which varies between the different types of curves. All `Curve`-classes inherit the `Curve` base class which is responsible for rendering a curve and performing operations on the curve. Furhter, a the curve can be plotted or exported and when that is done, the curve is run through a range using a parameter which is defined during object creation. A part of a curve can also be expoerted, e.g. by providing a slice or a subset of the parameter.

## Features
Several different curves are suported and more are added. Currenlty curves can generat and handle
- Polygons
- Exponetial curves
- Bezier curves of third order
- Ellipses
- Spirals
- Lines

All curves can be
- moved
- mirrored in an arbitrary line
- rotated around an arbitrary point
- stroked to create a closed poligone of arbitrary thickness along the curve

Derived curves that consists of segments of different parametric curves can be treated as a single object in a transparent way by placing them in the `MultiCurve` class. This is also used internally in `Curves` when performing certain operations on a curve, for example when doing a fillet operation.

### Per-curve specific features
Special features are implemented per-curve as described below:

#### Polygon
- Fillet

#### Bezier curve
- Connect: connecting a bezier curve with another curve so that the resulting curve is $C^1$.

## Export
When data is exported, it is always exported as a polygon but with arbitrary resolution.

Currenty data can be exported to
- CSV
- KiCAD footprint
- SVG

## Usage
There are several examples in the `examples` folder of the respoitory. The basic flow of creating a curve is:
- Create suitable points that define the curve
- Create the curve using which-ever class it is
- Do any modification
- Export the cureve to whereve it is to be used

### Example 1 - A parametrized rectangle


## Repository structure
`curves` - the curves package
`examples` - examples
`doc` - documentation
`tests` - tests

## Development
Create a virtual environment

  `python -m venv venv`

and activate it

  `source ./venv/bin/activate (Linux, macOS)`

or

  `.\venv\Scripts\activate (Win)`

and then install the package in an editable state

  `pip install -e .`

# Toto
- Add capability to render arbitrary Curve to Polygon
