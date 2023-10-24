from celluloid import Camera
from testfunctions import Function2D, ShafferF62D
from dataclasses import dataclass

import matplotlib as mat
import matplotlib.pyplot as plt
import numpy as np
from numpy.typing import NDArray 

import typing as t


class BadData(Exception):
    def __init__(self):
        super().__init__('Bad Data.')


@dataclass
class Datapoints:
    xcoords: t.List[NDArray[np.float32]] 
    ycoords: t.List[NDArray[np.float32]]
    axis: mat.axis.Axis
    colour: str = '#2164b0'
    alpha: float = 0.6


    @classmethod
    def fromListCoords(cls, l: t.List[t.List[NDArray[np.float32]]], 
            axis: mat.axis.Axis, 
            colour: str ='#2164b0', 
            alpha: float = 0.6):

        xcoords = []
        ycoords = []
        for li in l:
            
            n = len(li)
            x = np.full(n, 0.0, dtype='float32')
            y = np.full(n, 0.0, dtype='float32')

            for j, (a, b) in enumerate(li):
                x[j] = a
                y[j] = b
                
            xcoords.append(x)
            ycoords.append(y)

            

        return cls(xcoords, ycoords, axis, colour, alpha)


class ScatterAnimation:
    
    # every a in args:
    # a = (x, y, c, a)
    #   x, y is lists of lists where sublists contain x, y coordinates 
    #   len(x) = len(y) < numframes
    # 
    #   c is the colour of the plotted points: (rgb_string, alpha)
    #   a is the axis to plot
    def __init__(self, numframes: int = 100, fig: mat.figure.Figure = None, data: t.List[Datapoints] = None) -> None:
        
        if(data is None):
            raise BadData() 

        for d in data:
            if ((len(d.xcoords) != len(d.ycoords)) or (len(d.ycoords) < numframes)):
                raise BadData()

        self.data = data 
        self.numframes: int = numframes
        self.camera = Camera(fig)

    def createAnimation(self) -> mat.animation.ArtistAnimation:
        for i in range(self.numframes): 
            for d in self.data:
                d.axis.scatter(x = d.xcoords[i], y = d.ycoords[i], c = d.colour, alpha = d.alpha)
                
            self.camera.snap()

        anim = self.camera.animate()
        return anim

def createFunctionAnimation(funcObj: Function2D, axis: mat.axis.Axis, filesavepath: str, sa: ScatterAnimation):
    anim = sa.createAnimation()
    funcObj.show(axis)
    anim.save(filesavepath)

if __name__ == '__main__':
    fig, ax1 = plt.subplots(nrows = 1, ncols = 1, figsize=(12, 8), dpi = 80)
    sf = ShafferF62D(xshift = np.float32(30.0), yshift = np.float32(-30.0))
    numframes = 10
    x1 = [] 
    y1 = []
    
    x2 = [] 
    y2 = [] 

    rng = np.random.default_rng()
    for j in range(numframes):
        x1.append(rng.uniform(low = -100, high = 100, size = 10))
        y1.append(rng.uniform(low = -100, high = 100, size = 10))

        x2.append(rng.uniform(low = -100, high = 100, size = 10))
        y2.append(rng.uniform(low = -100, high = 100, size = 10))
 
    
    d1 = Datapoints(x1, y1, ax1)
    d2 = Datapoints(x2, y2, ax1, '#25ba6b')

    sa = ScatterAnimation(numframes, fig, [d1, d2])
    createFunctionAnimation(sf, ax1, './images/hello2.gif', sa)

