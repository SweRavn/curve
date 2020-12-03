# Curves
A package to generate parametric curves. Curves was designed to create paramertic curves and export them to suitable format for processing in other applications. The idea with the package is to treat curves at analytic objects and be able to do manipulation on those analytic objects and then export the result as an arbitrty resolution polygon. Exporting to a polygon is done by choice. This is a very simple format that any program that deals with geomertical/graphical elements can handle.

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

### Special features
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
There are several examples in the `examples` folder of the respoitory. Below follows a quick start example.


## Repository structure
curves - the curves package
examples - examples
doc - documentation
tests - tests

## Development
Create a virtual environment

  python -m venv venv

and activate it

  source ./venv/bin/activate (Linux, macOS)

or

  .\venv\Scripts\activate (Win)

and then install the package in an editable state

  pip install -e .

# Toto
- Add capability to render arbitrary Curve to Polygon