from dlmonte_python_setup import Controlwriter as cw
#from tmatrix_combine import pullmatrix, convertmatrix, pullandconv, outmatrix
import os
from shutil import copyfile

iterations = 1e7
scanparams ={
'title' : "An autogenereated DL_MONTE control script to scan across windows using the transition matrix method\n",
'T' : 298,
'P' : 1.25e-6,
'iterations' : iterations,
'eqlength' : 0,
'statsize' : int(max(iterations / 1000, 1000)),
'outfreq' : int(max(iterations / 1000, 1000)),
'statfreq' : int(max(iterations / 1000, 1000)),
'yamlfreq' : int(max(iterations / 10000, 1000)),
'archivefreq' : int(max(iterations / 100, 10000)),
'fed' : True,
'FEDprintfreq' : iterations,
'updatefreq' : 1000,
'low' :0,
'high' : 540,
'win' : True,
'res' : False,
'species' : 'Methanol',
'chempot': 1.4e-5}

def directorymaker(dxout = "."):
    filename = "{0}/test.txt" .format(dxout) #Test file name
    if not os.path.exists(os.path.dirname(filename)): #Checks if the test file exists
        try:
            os.makedirs(os.path.dirname(filename)) #Makes the file
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    with open(filename, "w") as f:
        f.write("FOOBAR") #Writes something in the test file

def sim_setup(directory, object):
    directorymaker('../{0}'.format(directory))
    directorymaker('../{0}/archive'.format(directory))
    with open('../{0}/CONTROL'.format(directory), 'w') as f:
        f.write(object.printcontrol())
    copyfile('templates/CONFIG', '../{0}/CONFIG'.format(directory))
    copyfile('templates/FIELD', '../{0}/FIELD'.format(directory))


def windowscan(simulation, bottom, top, window_span, window_hop, series_name):
    directorylist = []
    for count, i in enumerate(range(bottom, top-window_span+1, window_hop)):
        simulation.winlow = i
        simulation.winhigh = i + window_span
        directory = '{0:02d}{1}'.format(count, series_name)
        sim_setup(directory, simulation)
        directrorylist.append(directory)
    return directorylist


foo = cw.dlmonte_control()
foo.updatefromdict(scanparams)
minimum  = -0.5
maximum = 180.5
windowspan = 10
foo.low = minimum
foo.high = maximum
scanfilelist = []
exploitfilelist = []
scanfilelist.append(windowscan(foo, minimum, maximum, windowspan, 1, scan))
#for count,i in enumerate(range(0,math.floor(maximum)-windowspan+1,5), 1):
#    foo.winlow = i-0.5
#    foo.winhigh = i+0.5+windowspan
#    directory = "{0:02d}scan".format(count)
#    directorymaker('../{0}'.format(directory))
#    directorymaker('../{0}/archive'.format(directory))
#    with open('../{0}/CONTROL'.format(directory), 'w') as f:
#        f.write(foo.printcontrol())
#    copyfile('templates/CONFIG', '../{0}/CONFIG'.format(directory))
#    copyfile('templates/FIELD', '../{0}/FIELD'.format(directory))
#    scanfilelist.append(directory)

with open('../taskfarm.scan', 'w') as f:
    f.write('#!/bin/bash\n')
    f.write('bash dlmonte.sh ' + '\nbash dlmonte.sh '.join(scanfilelist))

iterations = 1e8
exploitparams = {
    'iterations': iterations,
    'statsize': int(max(iterations / 1000, 1000)),
    'outfreq': int(max(iterations / 1000, 1000)),
    'statfreq': int(max(iterations / 1000, 1000)),
    'yamlfreq': int(max(iterations / 10000, 1000)),
    'archivefreq': int(max(iterations / 100, 10000)),
    'fed': True,
    'FEDprintfreq': int(max(iterations/100, 1e6)),
    'win': False,
    'res': True
}
foo.updatefromdict(exploitparams)

for count, i in enumerate(range(1,17), 1):
    directory = "{0:02d}exploit".format(count)
    sim_setup(directory, foo)
    exploitfilelist.append(directory)

with open('../taskfarm.exploit', 'w') as f:
    f.write('#!/bin/bash\n')
    f.write('bash dlmonte.sh ' + '\nbash dlmonte.sh '.join(exploitfilelist))

with open('../tm_combine.sh', 'w') as f:
    f.write('#!/bin/bash\n')
    f.write('python tmatrix_combine.py -i ' + '/TMATRX '.join(scanfilelist) + '/TMATRX -o ' + '/ '.join(exploitfilelist) + '/')
 

iterations = 1e4
finalparams = {
    'iterations': iterations,
    'statsize': int(max(iterations / 1000, 1000)),
    'outfreq': int(max(iterations / 1000, 1000)),
    'statfreq': int(max(iterations / 1000, 1000)),
    'yamlfreq': int(max(iterations / 10000, 1000)),
    'archivefreq': int(max(iterations / 100, 10000)),
    'fed': True,
    'FEDprintfreq': iterations,
    'win': False,
    'res': True
}
foo.updatefromdict(finalparams)

directorymaker('../finalcombine')
with open('../finalcombine/CONTROL'.format(directory), 'w') as f:
    f.write(foo.printcontrol())
copyfile('templates/CONFIG', '../finalcombine/CONFIG'.format(directory))
copyfile('templates/FIELD', '../finalcombine/FIELD'.format(directory))

with open('../tm_combine2.sh', 'w') as f:
    f.write('#!/bin/bash\n')
    f.write('python tmatrix_combine.py -i ' + '/TMATRX '.join(exploitfilelist) + '/TMATRX -o finalcombine/')


