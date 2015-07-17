import sys
import analyse
import math
import numpy           # For mean and var
from pylab import *    # For creating plots 

config_file_name = sys.argv[1]
result = analyse.get_result(config_file_name)

accuracy = numpy.array(result.group_by("c").map(lambda x: x[0]).items())

semilogx(accuracy[:, 0], accuracy[:, 1])
xlabel('c')
ylabel('cross validation accuracy')
show()
