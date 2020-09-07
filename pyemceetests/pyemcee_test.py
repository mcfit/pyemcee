"""Tests for pyequib"""

import pyemcee
import numpy as np

def myfunc21(input1):
   result1 = np.sum(input1)
   result2 = input1[1] ** input1[0]
   return [result1, result2]

clevel = .9
use_gaussian = 0
walk_num = 30
iteration_num = 10

input1 = np.array([1., 2.])
input1_err = np.array([0.2, 0.5])
input1_err_p = input1_err
input1_err_m = -input1_err
output1 = myfunc21(input1)
output1_num = len(output1)

mcmc_sim = pyemcee.hammer(myfunc21, input1, input1_err_m, input1_err_p, output1, walk_num, iteration_num, use_gaussian)

output1_error = pyemcee.find_errors(output1, mcmc_sim, clevel)

