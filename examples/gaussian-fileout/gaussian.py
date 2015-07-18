#!/usr/bin/env python
import random, sys, time

n = int(sys.argv[1])
outfile = sys.argv[2]

fout = open(outfile, 'w')

for i in xrange(n):
    fout.write('id %d value %f\n' % (i, random.normalvariate(0, 1)))

fout.close()
time.sleep(5)
