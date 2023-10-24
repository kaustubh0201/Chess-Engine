from __future__ import annotations

import os 

import numpy as np
import matplotlib as mat
import matplotlib.pyplot as plt


import typing as t
import tqdm as bar

from testfunctions import ShafferF62D, Function2D, ValueOutOFRange, Rastrigin2D 
import animations as a

rng = np.random.default_rng()

def suppress_qt_warnings() -> None:
    os.environ["QT_DEVICE_PIXEL_RATIO"] = "0"
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    os.environ["QT_SCREEN_SCALE_FACTORS"] = "1"
    os.environ["QT_SCALE_FACTOR"] = "1"

def clamp(val, minval, maxval):
    return sorted((minval, val, maxval))[1]

class Organism:
    def __init__(self, chrom: np.ndarray = None) -> None:
        self.chromosome = chrom
        self.fitness : float = 0.0 
    
    
    @classmethod
    def createRandomOrg(cls, chromLen: int = 1, 
            chromMin: float = np.finfo('float32').min, 
            chromMax: float = np.finfo('float32').max) -> Organism:

        chromosome : np.ndarray = rng.uniform(size = chromLen, low = chromMin, high = chromMax) 
        return cls(chromosome) 

    def mutate(self, mRate):
        self.chromosome += rng.normal(loc = 0, scale = mRate, size = self.chromosome.shape)
    
    @staticmethod
    def getChild(parent1 : Organism, parent2 : Organism, interpolFac : float) -> Organism:
        childChrom = parent1.chromosome * interpolFac + (1 - interpolFac) * parent2.chromosome 

        return Organism(childChrom)
  
class Population:
    
    def __init__(self, 
            popSize: int = 100, 
            orgList: t.List = [],              
            fitness: Function2D = None 
            ) -> None:

        self.orgList: t.List = orgList 
        self.popSize: int = popSize
        self.fitFunc: Function2D = fitness
    
    @classmethod
    def initFromRandomOrgs(cls,
            popSize: int = 100, 
            orgData: t.Dict = {
                'len': 2, 
                'min': np.finfo('float32').min, 
                'max': np.finfo('float32').max
                }, 
            fitness: t.Callable = lambda x: np.max(x) 
            ) -> Population:

        orgList : t.List = [
                Organism.createRandomOrg(
                    chromLen = orgData['len'], 
                    chromMin = orgData['min'],
                    chromMax = orgData['max']) 
                for _ in range(popSize)] 

        return Population(popSize = popSize, 
                orgList = orgList,
                fitness = fitness)

   
    def truncationSelection(self, topCount: int) -> (t.List, t.List):
        for o in self.orgList:
            try:
                o.fitness = self.fitFunc.evaluateSingle(o.chromosome)
            except ValueOutOFRange:
                o.fitness = np.finfo('float32').min
        
        s = sorted(self.orgList, key = lambda o : o.fitness)
        parents = s[:topCount] 

        return parents, s[(topCount+1):]

    def updateOrgList(self, parentsList: t.List, childrenList: t.List):
        self.orgList = parentsList + childrenList

    def getOrgs(self, *args) -> t.List:
        out = []
        for arg in args:
            out.append(self.orgList[arg])
           
        return out 

class GeneticAlgorithm():  
    # kwarg: selectPer, interpolFac, mutationRate  
    def __init__(self, 
            population: Population = None, **kwargs
            ) -> None:

        selectPer: float   = kwargs.pop('selectPer', 0.20) 
        interpolFac: float = kwargs.pop('interpolFac', 0.5)
        mutationRate: float = kwargs.pop('mutationRate', 1.0)

        self.population: Population = population
        self.k:  int = int(population.popSize * clamp(selectPer, 0.0, 1.0))
        self.interpolFac: float = clamp(interpolFac, 0.0, 1.0)
        self.mutRate: float = mutationRate 

    @classmethod
    def initRandomPop(cls,
            popSize: int = 100, 
            orgData: t.Dict = {
                'len': 2, 
                'min': np.finfo('float32').min, 
                'max': np.finfo('float32').max
                }, 
            fitness: Function2D = None, 
            **kwargs,
            ) -> GeneticAlgorithm:

        p = Population.initFromRandomOrgs(popSize, orgData, fitness)  

        return cls(p, **kwargs)

    def selection(self) -> (t.List, t.List):
        # Using truncation selection 
        return self.population.truncationSelection(self.k) 

    def crossover(self, parentsList : t.List) -> t.List:
        numChildren = self.population.popSize - self.k 
        children : t.List = []
        high = len(parentsList) 
        for _ in range(0, numChildren):
            p : np.ndarray = rng.choice(a = high, size = 2) 

            p1 = parentsList[p[0]]
            p2 = parentsList[p[1]]

            children.append(Organism.getChild(p1, p2, self.interpolFac))

        return children

    def mutation(self, childrenList: t.List):
        for c in childrenList:
            c.mutate(self.mutRate)

    def updateOrgList(self, parentsList: t.List, childrenList: t.List):
        self.population.updateOrgList(parentsList, childrenList)


class DifferentialEvolution():

    # kwargs: p: crossover probability
    #         w: differential weight
    #         n: dimension of organism

    def __init__(self, population: Population = None, **kwargs):
        self.population: Population = population
        self.p: float = clamp(kwargs.pop('p', 0.5), 0.0, 1.0)
        self.w: float = clamp(kwargs.pop('w', 1.0), 0.0, 1.0)
        self.n: int = kwargs.pop('n', 2)
    
    @classmethod
    def initRandomPop(cls, popSize: int = 100, 
            orgData: t.Dict = {
                'len': 2, 
                'min': np.finfo('float32').min, 
                'max': np.finfo('float32').max
                }, 
            fitness: Function2D = None, **kwargs):

        p = Population.initFromRandomOrgs(popSize, orgData, fitness)  

        return cls(p, n = orgData['len'], **kwargs)
   
    def crossover(self, count: int = 3) -> None:

        genIndices: t.Callable =\
        lambda i: rng.choice(\
        np.concatenate((np.arange(0, i), np.arange(i + 1, self.population.popSize))),\
        size = count) 
        
        rand: t.Callable =\
                lambda : rng.uniform(size=1)
        
        for i, o in enumerate(self.population.orgList):
            t, u, v = genIndices(i) 
            [a, b, c] = self.population.getOrgs(t, u, v)
            
            x = o.chromosome
            z = a.chromosome + self.w * (b.chromosome - c.chromosome)
            new = np.full(self.n, 0.0, dtype='float32')

            j = rng.integers(low = 0, high = self.n, size = 1)

            for i in range(0, self.n):
                
                if(i == j):
                    new[i] = z[i]
                elif(rand() <= self.p):
                    new[i] = z[i]
                else:
                    new[i] = x[i]
            
            try:
                newfitness = self.population.fitFunc.evaluateSingle(new)
            except ValueOutOFRange: 
                newfitness = np.finfo('float32').min

            try:
                oldfitness = self.population.fitFunc.evaluateSingle(x) 
            except ValueOutOFRange: 
                oldfitness = np.finfo('float32').min

            if(newfitness > oldfitness):
                o.chromosome = new

def GA():
    sf = ShafferF62D(xshift = np.float32(30.0), yshift = np.float32(-30.0))

    ga = GeneticAlgorithm.initRandomPop(
            popSize = 100, 
            orgData = {'len': 2, 'min': -75.0, 'max': -50.0},
            fitness = sf,
            selectPer = 0.20,
            interpolFac = 0.5,
            mutationRate = 2.0
            )
    
    out1 = []
    out2 = []
    for g in bar.tqdm(range(0, 100)):
        
        parents, rejected = ga.selection()
        children = ga.crossover(parents)
        ga.mutation(children)
        ga.updateOrgList(parents, children)
        
        out2.append([p.chromosome for p in parents])
        out1.append([r.chromosome for r in rejected])

    fig, ax1 = plt.subplots(nrows = 1, ncols = 1, figsize=(12, 8), dpi = 80) 
    dp = a.Datapoints.fromListCoords(out1, ax1) 
    dp2 = a.Datapoints.fromListCoords(out2, ax1, colour='#25ba6b', alpha = 0.6) 
    sa = a.ScatterAnimation(100, fig, [dp, dp2])
    a.createFunctionAnimation(sf, ax1, './images/de2.gif', sa)


def DE():
    sf =  Rastrigin2D(xshift = np.float32(00.0), yshift = np.float32(-00.0))

    de = DifferentialEvolution.initRandomPop(
            popSize = 100, 
            orgData = {'len': 2, 'min': -5.12, 'max': +5.12},
            fitness = sf,
            p = 0.8, 
            w = 1.0)
    
    out = []
    for g in bar.tqdm(range(0, 100)):
        de.crossover(3)        
        out.append([p.chromosome for p in de.population.orgList])

    fig, ax1 = plt.subplots(nrows = 1, ncols = 1, figsize=(12, 8), dpi = 80) 
    dp = a.Datapoints.fromListCoords(out, ax1) 
    sa = a.ScatterAnimation(100, fig, [dp])
    a.createFunctionAnimation(sf, ax1, './images/de1.gif', sa)


if __name__ == '__main__':
    suppress_qt_warnings()
    DE()
    # GA()

