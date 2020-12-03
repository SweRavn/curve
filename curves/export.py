# -*- coding: utf-8 -*-
"""
Created on Sat Nov 23 07:42:59 2019

@author: rore
"""

from numpy import arange, sqrt, array, pi, cos
__inf = float('inf')

class Export:
    """
    Class to do export to different file formats.
    """
    def __init__(self, **kwargs):
        pass
    
    def to_csv(self, data):
        pass
    
    def to_svg(self, data):
        pass
    
    def to_kicad(self, data):
        pass

export_options_kicad = {
        'layer': 'F.Cu', # B.Cu, F.SilkS, B.SilkS, F.Fab, B.Fab
        'draw_type': 'fp_poly', # fp_line, np_thru_hole
        }
export_options_csv = {
        'sep': ','}
export_options_svg = {
        }

def export(data, filename='noname', path='./', filetype='csv', name='noname', options={}, **kwargs):
    """
    Export the contents of data to a number of different formats.
    @param data list or nympy.array. If it is a list is it expected to be a list of numpy.array's. Then export is run on each numpy.array in the list to the same file.
    """
    filename = path.strip('/\\')+'/'+filename.split('.')[0]
    
    if type(data) != list:
        d = [data]
    else:
        d = data

    if 'names' in kwargs:
        names = kwargs['names']
        del kwargs['names']
    else:
        names = list()
        for k in range(len(data)):
            names.append(f'noname{k}')
    if len(names) != len(data):
        raise Exception('Object names needs to be same length as objects or omitted.')

    # Export:
    if filetype=='csv':
        for k in range(len(d)):
            data = d[k]
            n = names[k]
            with open(filename+'_'+n+'.csv', 'w') as file:
                I,J = data.shape
                for j in range(J):
                    file.write(f'{data[0,j]}, {data[1,j]}\n')
    elif filetype=='svg':
        # FIXME: dimension in svg-file is wrong - it is px, not mm...
        with open(filename+'.svg', 'w') as file:
            file.write("""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!-- Created with Inkscape (http://www.inkscape.org/) -->
<svg
   xmlns:dc="http://purl.org/dc/elements/1.1/"
   xmlns:cc="http://creativecommons.org/ns#"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
   xmlns:svg="http://www.w3.org/2000/svg"
   xmlns="http://www.w3.org/2000/svg"
   xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
   version="1.1"
   width="210mm"
   height="297mm"
   id="svg2">
  <g
     id="layer1">
    <path
       d="M """)
            file.write(f'{data[0,0]}, {data[1,0]} L  \n')
            for k in range(len(d)):
                data = d[k]
                n = names[k]
                I,J = data.shape
                for j in range(J-1):
                    file.write(f'{data[0,j+1]}, {data[1,j+1]}\n')
                file.write(f""""
           id="{n}"
           style="fill:none;stroke:#000000;stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1" />
      </g>
    </svg>""")
    elif filetype=='kicad_mod':
        if 'layers' in kwargs:
            layers = kwargs['layers']
        else:
            layers = ['F.Cu' for k in range(len(d))]
        if 'types' in kwargs:
            types = kwargs['types']
        else:
            types = ['fp_poly' for k in range(len(d))]
        with open(filename+'.kicad_mod', 'w') as file:
            file.write('(module {name} (layer {layer}) (tedit 123456678)\n'.format(name=name, layer='F.Cu'))
            file.write('  (fp_text reference REF** (at 0 0) (layer F.SilkS)\n')
            file.write('    (effects (font (size 1 1) (thickness 0.15)))\n')
            file.write('  )\n') # fp_text
            file.write('  (fp_text value {name} (at 0 0) (layer F.Fab)\n'.format(name=name))
            file.write('    (effects (font (size 1 1) (thickness 0.15)))\n')
            file.write('  )\n') # fp_text
            if 'texts' in options:
                for text in options['texts']:
                    if 'angle' in text:
                        angle = text['angle']
                    else:
                        angle = 0
                    file.write(f'(fp_text user "{text["text"]}" (at {text["point"].x} {text["point"].y} {angle}) (layer {text["layer"]}) (effects (font (size 1 1)(thickness 0.15) )))\n')
            for k in range(len(d)):
                data = d[k]
                layer = layers[k]
                tp = types[k]
                if tp == 'fp_poly':
                    file.write(f'  ({tp} (pts ')
                    I,J = data.shape
                    for j in range(J):
                        file.write(f' (xy {data[0,j]:0.4g} {data[1,j]:0.4g})')
                    file.write(f') (layer {layer}) (width 0.001))\n')
                elif tp=='fp_line':
                    I,J = data.shape
                    for j in range(J-1):
                        file.write(f'  ({tp} (start {data[0,j]:0.4g} {data[1,j]:0.4g}) (end {data[0,j+1]:0.4g} {data[1,j+1]:0.4g}) (layer {layer}) (width 0.001))\n')
                elif tp == 'np_thru_hole':
                    for j in range(J-1):
                        file.write(f'  (pad "" {tp} oval (at {(data[0,j]+data[0,j+1])/2:0.3g} {(data[1,j]+data[1,j+1])/2:0.3g}) (size {(data[0,j]+data[0,j+1])/2:0.3g} {(data[1,j+1]-data[1,j+1]):0.3g})')
                elif 'pad' in tp:
                    x = (max(data[0,:])+min(data[0,:]))/2
                    y = (max(data[1,:])+min(data[1,:]))/2
                    w = (max(data[0,:])-min(data[0,:]))
                    h = (max(data[1,:])-min(data[1,:]))
                    s = min(w, h)
                    file.write(f'({tp} smd custom (at {x:0.4g} {y:0.4g}) (size {s:0.4g} {s:0.4g}) (layers {layer})\n')
                    file.write('  (options (clearance outline) (anchor circle))\n')
                    file.write('  (primitives\n')
                    file.write('    (gr_poly (pts\n')
                    I,J = data.shape
                    for j in range(J):
                        file.write(f' (xy {data[0,j]-x:0.4g} {data[1,j]-y:0.4g})')
                    file.write(') (width 0.001)) ))\n')
                else:
                    raise Exception(f'Unknown object type {tp}')
                file.write('\n')
            file.write(')\n') # module
    else:
        raise Exception(f'Unknown file type {filetype}')

def dist(p1, p2):
    """
    Distance between two points.
    """
    return sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)

def cleanup(data, mind=__inf, mina=pi):
    """
    Remove points that are closer than mind.
    """
    M,N = data.shape
    newx, newy = [data[0,0],], [data[1,0],]
    for n in arange(1, N-2):
        a = dist([newx[-1], newy[-1]], data[:,n])
        b = dist(data[:,n], data[:,n+1])
        c = dist([newx[-1], newy[-1]], data[:,n+1])
        C = cos(mina)
        if (a > mind) or ((a**2+b**2-c**2)/(2*a*b) > C):
            newx.append(data[0,n])
            newy.append(data[1,n])
    newx.append(data[0,-1])
    newy.append(data[1,-1])
    return array((newx, newy))

