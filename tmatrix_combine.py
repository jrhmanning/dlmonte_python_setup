import numpy as np
import argparse
import sys

def pullmatrix(file):
    alldata = []

    with open(file, "r") as f:
        for line in f:
            alldata.append(line.split())
    return alldata
#print(alldata[2:3:])
def convertmatrix(array):
    rawmatrx = np.asarray(array)
    matrx = rawmatrx.astype(np.float)
    return matrx

def outputmatrix(header, body, file="TMATRX.out"):
    with open(file, "w") as f:
        for line in header:
            f.write(" ".join([x for x in line]))
            f.write('\n')
        for i in body:
            for j in i:
                f.write("   {0:23.17E}".format(j))
#            f.write("   {}".join([x.astype(np.str) for x in i]))
            f.write('\n')

def pullandconv(file):
    x = pullmatrix(file)
    y = convertmatrix(x[2:])
    return y

parser = argparse.ArgumentParser()
parser.add_argument('-i', action='append', nargs='*', help='Your TMATRX output file paths go here')
parser.add_argument('-o', action='append', nargs = '*', help='your output directories go here')
args = parser.parse_args()
inputfiles = args.i[0]
try:
    outputdirectories = args.o[0]
except:
    outputdirectories = ['./']
print(inputfiles)
print(outputdirectories)
outputlocations = args.o
if len(inputfiles) == 0:
    sys.exit()
#input = "TMATRX.000"
#input2 = "TMATRX.002"

#inputfiles = [input, input2]

matrices = {}
inmatrix = pullmatrix(inputfiles[0])
for i in inputfiles:
    matrices[i] = pullandconv(i)
#newmatrix = pullandconv(input)
#newmatrix2 = pullandconv(input2)
#inmatrix = pullmatrix(input)
#inmatrix2 = pullmatrix(input2)
#newmatrix = convertmatrix(inmatrix[2:])
#newmatrix2 = convertmatrix(inmatrix2[2:])

outmatrix = np.zeros_like(matrices[inputfiles[0]])

for i in matrices.values():
    outmatrix += i
#doublematrix= newmatrix + newmatrix2
#print(np.sum(doublematrix.sum(axis=0, dtype=float)))
for i in outputdirectories:
    outputmatrix(inmatrix[:2], outmatrix, "{0}TMATRX".format(i))
print('Done!')