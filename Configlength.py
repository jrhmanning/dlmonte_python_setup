import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument('file', type=str, help='A DL_MONTE config file to be cut to an arbitrary length')
parser.add_argument('length', type=int, help='The number of molecules you want in your config file.')
parser.add_argument('-o', type=str, default='CONFIG.out', help='The output filename and location (optional)')
args = parser.parse_args()
print(args)

input = args.file
print(input)
alldata = []
with open(input, "r") as f:
    for line in f:
        alldata.append(line.split())
if int(alldata[5][1])<args.length:
    print('Uh-oh! Looks like your configuration is already shorter than your desired length!\n'
          'Please try again with a longer config file or shorter desired length. I\'m quitting now.')
    sys.exit()

newdata = []
for line in alldata[0:((args.length*7)+6)]:
    newdata.append(line)
newdata[5][1] = str(args.length)

with open(args.o, 'w') as f:
    for i in newdata:
        f.write(' '.join([j for j in i]))
        f.write('\n')
print('Done!')
