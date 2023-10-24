from abc import ABC, abstractmethod

import numpy as np
from numpy.typing import NDArray 

import matplotlib as mat
import matplotlib.pyplot as plt

import os 
import typing as t

def suppress_qt_warnings() -> None:
    os.environ["QT_DEVICE_PIXEL_RATIO"] = "0"
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    os.environ["QT_SCREEN_SCALE_FACTORS"] = "1"
    os.environ["QT_SCALE_FACTOR"] = "1"


class ValueOutOFRange(Exception):
    def __init__(self, axis: str) -> None:
        super().__init__(f'Values given for {axis}-axis are out of range.')


class Function2D(ABC):
    _xmin = np.float32(-100.0)
    _xmax = np.float32(+100.0)
    _ymin = np.float32(-100.0)
    _ymax = np.float32(+100.0)
    _graphtitle = '-x-'

    def __init__(self, 
            xshift: np.float32 = np.float32(0.0), 
            yshift: np.float32 = np.float32(0.0), 
            xiter: np.int32 = np.int32(100), 
            yiter: np.int32 = np.int32(100)) -> None:
    
        self.xshift = xshift
        self.yshift = yshift
        self.xiter = xiter
        self.yiter = yiter 
    
    def _checkBounds(self, x: NDArray[np.float32], y: NDArray[np.float32]) -> t.Union[None, str]:
        if(np.any((self.xmin > x) | (x > self.xmax))):
            return 'x'

        if(np.any((self.ymin > y) | (y > self.ymax))):
            return 'y'


        return None 

    def evaluateSingle(self, v: NDArray[np.float32]) -> np.float32:
        axis: t.Union[None, str] = self._checkBounds(v[0], v[1])

        if(axis is not None):
            raise ValueOutOFRange(axis)

        return self._func(v[0], v[1]) 


    def evaluate(self, x: NDArray[np.float32], y: NDArray[np.float32]) -> NDArray[np.float32]:
        axis: t.Union[None, str] = self._checkBounds(x, y)

        if(axis is not None):
            raise ValueOutOFRange(axis)

        return self._func(x, y)
 
    def show(self, ax = None) -> None:
        x: NDArray[np.float32] = np.linspace(self.xmin, self.xmax, self.xiter) 
        y: NDArray[np.float32] = np.linspace(self.ymin, self.ymax, self.yiter) 
        
        x, y = np.meshgrid(x, y)

        z: NDArray[np.float32] = self._func(x, y)

        ax.imshow(z, interpolation='bilinear', 
            extent = [self.xmin, self.xmax, self.ymin, self.ymax], 
            origin = 'lower', 
            cmap = 'YlOrBr')

        ax.title.set_text(self.graphtitle) 


    @abstractmethod
    def _func(self, x: NDArray[np.float32], y: NDArray[np.float32]) -> NDArray[np.float32]:
        pass

    @property
    def xmin(self) -> np.float32:
        return self._xmin 

    @property
    def xmax(self) -> np.float32:
        return self._xmax 

    @property
    def ymin(self) -> np.float32:
        return self._ymin 

    @property
    def ymax(self) -> np.float32:
        return self._ymax 
    
    @property
    def xshift(self) -> np.float32:
        return self._xshift

    @xshift.setter
    def xshift(self, val: np.float32) -> None:
        self._xshift = val

    @property
    def yshift(self) -> np.float32:
        return self._yshift
    
    @yshift.setter
    def yshift(self, val: np.float32) -> None:
        self._yshift = val

    @property
    def xiter(self) -> np.int32:
        return self._xiter

    @xiter.setter
    def xiter(self, val: np.int32) -> None:
        self._xiter = val

    @property
    def yiter(self) -> np.int32:
        return self._yiter
    
    @yiter.setter
    def yiter(self, val: np.int32) -> None:
        self._yiter = val

    @property
    def graphtitle(self) -> str:
        return self._graphtitle

class ShafferF62D(Function2D):
    xmin = np.float32(-100.0)
    xmax = np.float32(+100.0)
    ymin = np.float32(-100.0)
    ymax = np.float32(+100.0)
    graphtitle = 'ShafferF6 - 2D'

    def __init__(self, 
            xshift: np.float32 = np.float32(0.0), 
            yshift: np.float32 = np.float32(0.0), 
            xiter: np.int32 = np.int32(500), 
            yiter: np.int32 = np.int32(500)) -> None:
        
        super().__init__(xshift, yshift, xiter, yiter)
        
    def _func(self, x: NDArray[np.float32], y: NDArray[np.float32]) -> NDArray[np.float32]:
        x += self.xshift
        y += self.yshift

        return 0.5 + ((np.sin(np.sqrt(x**2 + y**2)))**2 - 0.5)/((1 + 0.001 * (x**2 + y**2))**2)

class Rastrigin2D(Function2D):
    xmin = np.float32(-5.12)
    xmax = np.float32(+5.12)
    ymin = np.float32(-5.12)
    ymax = np.float32(+5.12)
    graphtitle = 'Rastrigin - 2D'
       
    def _func(self, x: NDArray[np.float32], y: NDArray[np.float32]) -> NDArray[np.float32]:
        x += self.xshift
        y += self.yshift

        return ((x**2 - 10.0 * np.cos(2.0 * np.pi * x)) + (y**2 - 10.0 * np.cos(2.0 * np.pi * y)) + 20.0) * -1.0



if __name__ == '__main__':
    suppress_qt_warnings()


    fig, ax1 = plt.subplots(nrows = 1, ncols = 1, figsize=(12, 8), dpi = 80)
    sf = ShafferF62D(xshift = np.float32(30.0), yshift = np.float32(-30.0))

    sf.evaluate([100.0, 100.0], [100.0, 100.0])

    sf.show(ax1)
    plt.show()
