### This file evidently won't work any more for a while because I'm mid-coding somethign into it.
### I want to treat classes like they're functions i.e. one class does one thing.
### Specifically, a class will either hold data or a method for doing something
### TODO: Define all the appropriate classes and give them a scope
### TODO: Work out a scope fot  he plan of this whole thing
### TODO: Differentiate this from the package that Tom's already written (how?)


# This python file will take in a load of simulation data for a GCMC and mask it onto a dl_monte control template file
# Hopefully I'll be able to do it with classes, but we'll see
# To do this, I'm going to split the control file up into several blocks:
# Use block (including optional fed subblock)
# Physical data block
# Simulation data block
# GCMC block
import attr
import random
random.seed()

@attr.s
class Data:
    all_data = []
    @classmethod
    def update_parameter(cls, dict):
        if not cls.all_data:
            raise RuntimeError('There are no defined parameters to update!')
        kwargs = {k: v for k, v in dict.items() if k in cls.all_data}
        cls(**kwargs)

@attr.s
class Physics(Data):
    physics_data = ['T']
    Data.all_data + physics_data
    # Physics Parameters
    T: float = 77
    P: float = 0.001

@attr.s
class muVT(Physics): pass

@attr.s
class NVT(Physics): pass

@attr.s
class FreeEnergy(Data): pass

@attr.s
class Simulation(Data): pass

@attr.s
class MonteCarlo(Simulation, Physics): pass

@attr.s
class GCMC(MonteCarlo, muVT): pass

@attr.s
class BiasMonteCarlo(MonteCarlo, FreeEnergy): pass

@attr.s
class BiasGCMC(GCMC, FreeEnergy): pass


########################################################

class DLMONTEPhys(Physics, DLMONTEprinter): pass

    def GenerateFrequencies(self):
        output_frequency =  int(max(self.iterations / 1000, 1000))
class Simulations():
    # Simulation parameters
    iterations = 10000
    eqlength = 0
    statsize = int(max(iterations / 1000, min(1000, iterations))
    outfreq = int(max(iterations / 1000, 1000))
    statfreq = int(max(iterations / 1000, 1000))
    yamlfreq = int(max(iterations / 10000, 1000))
    archivefreq = int(max(iterations / 100, 10000))

    @classmethod
    def from_dict(cls, dict):
        cls(dict["iterations"],...)

class FED():
    # FED parameters
    fed = True
    FEDprintfreq = iterations
    updatefreq = 1000
    low = 0
    high = 250
    win = True
    winlow = 0
    winhigh = 10
    res = False

class dlmonte_control(Physics, Simulations, FED):
    # General parameters
    title = None

    # Chemical Parameters
    species = ''
    chempot = 0.0001

    def __init__(self):
        pass

    def __repr__(self):
        pass

    def updatefromdict(self, dictname):
        for key, value in dictname.items():
            setattr(self, key, value)

    def printfedblock(self):
        span = self.high-self.low
        if not self.res:
            cont = 'new'
        else:
            cont = 'res'
        output = ''
        output += 'use fed generic\n'
        output += 'fed method tm {0:1.1e} {1} {2}\n'.format(self.FEDprintfreq, self.updatefreq, cont)
        output += 'fed order nmols {0} {1} {2} 1 '.format(span, self.low, self.high)
        if self.win ==True:
            output += 'win {0} {1}\n'.format(self.winlow, self.winhigh)
        else:
            output += '\n'
        output += 'fed done\n\n'
        return output


    def printuseblock(self):
        output = ''
        output += 'use ortho\n'
        output += 'use gaspressure\n\n'
        if self.fed is not None:
            output += self.printfedblock()
        output += 'finish\n\n'
        return output


    def printphysblock(self):
        ran0 = random.randint(0, 99)
        ran1 = random.randint(0, 99)
        ran2 = random.randint(0, 99)
        ran3 = random.randint(0, 99)
        output = ''
        output += 'seeds {0} {1} {2} {3} #4 randomseeds between 0 and 168\n'.format(ran0, ran1, ran2, ran3)
        output += 'temperature {0} #T in K\n'.format(self.T)
        output += '#pressure {0} #kilo atmospheres?\n'.format(self.P)
        output += 'ewald prec 1e-6 #no electrostatics\n\n'
        return output

    def printdatablock(self):
        output = ''
        output += 'steps {0:1.1e}  # number of MC iteractions \n'.format(self.iterations)
        output += 'equilibration {0}  # number of equil steps \n'.format(self.eqlength)
        output +='stack {0:1.1e}  # blocks for statistics \n'.format(self.statsize)
        output +='print {0:1.1e}  # frequency of writing for output files\n'.format(self.outfreq)
        output +='stats {0:1.1e}  # frequency of writing to a stats files\n'.format(self.statfreq)
        output += 'yamldata {0:1.1e}\n\n'.format(self.yamlfreq)
        output += 'sample coordinates {0:1.1e} # how often to archive coordinates\n'.format(self.archivefreq)
        output += '# archiveformat dcd # format of the trajectory file (ARCHIVE/HISTORY/TRAJECTORY)\n'
        output += 'revconformat dlmonte # format of REVCON file (to replace CONFIG if restarting)\n\n'
        return output

    def printGCMCblock(self):
        output = ''
        output += 'move molecule 1 25 \n {0}\n'.format(self.species)
        output += 'move rotatemol 1 25 \n {0}\n'.format(self.species)
        output += 'move gcinsertmol 1 50 0.5 \n {0}  {1:1.4f}\n\n'.format(self.species, self.chempot)
        return output

    def printcontrol(self):
        output = ''
        if self.title:
            output += self.title
        else:
            output += 'An autogenerated DL_MONTE control file has no name\n'
        output += self.printuseblock()
        output += self.printphysblock()
        output += self.printdatablock()
        output += self.printGCMCblock()
        output += 'start simulation'
        return output



