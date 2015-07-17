import sys
import analyse
import math
import numpy           # For mean and var
from pylab import *    # For creating plots 

config_file_name = sys.argv[1]
result = analyse.get_result(config_file_name)

result = result.group_by(["n", "run"])
mean = result.reducev(lambda x : numpy.mean(x))
var = result.reducev(lambda x : numpy.var(x))

mean_mean = numpy.array(mean.group_by(["n"]).reducev(lambda x : numpy.mean(x)).items())
mean_stdev = numpy.array(mean.group_by(["n"]).reducev(lambda x : math.sqrt(numpy.var(x))).items())

var_mean = numpy.array(var.group_by(["n"]).reducev(lambda x : numpy.mean(x)).items())
var_stdev = numpy.array(var.group_by(["n"]).reducev(lambda x : math.sqrt(numpy.var(x))).items())

subplot(2, 1, 1)
errorbar(mean_mean[:,0], mean_mean[:, 1], mean_stdev[:, 1])
xlabel('number of samples')
ylabel('mean')
xlim([0, 110])

subplot(2, 1, 2)
errorbar(var_mean[:,0], var_mean[:, 1], var_stdev[:, 1])
xlabel('number of samples')
ylabel('variance')
xlim([0, 110])

show()
