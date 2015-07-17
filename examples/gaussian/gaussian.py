#!/usr/bin/env python
import random, sys, time

n = int(sys.argv[1])

for i in xrange(n):
    print 'id %d value %f' % (i, random.normalvariate(0, 1))

f = open('a.txt', 'w')
f.write('12345')
f.close()

time.sleep(5)
