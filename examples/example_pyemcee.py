# Example: pyemcee.hammer() and pemcee.hammer()
#     determine uncertainties of two functions
#     for given input parameters
# 
import pyemcee
import os
import numpy as np

def myfunc21(input1):
   result1 = np.sum(input1)
   result2 = input1[1] ** input1[0]
   return [result1, result2]

def myfunc22(input1, functargs=None):
   #result1 = functargs.scale1*np.sum(input1)
  # result2 = functargs.scale2*input1[1] ** input1[0]
   result1 = functargs['scale1']*np.sum(input1)
   result2 = functargs['scale2']*input1[1] ** input1[0]
   return [result1, result2]

base_dir = os.getcwd()
#image_dir = '/examples/images'
image_dir = '/images'
image_output_path = base_dir+image_dir

clevel = .9
use_gaussian = 0 # uniform distribution from min value to max value
#use_gaussian=1 ; gaussian distribution from min value to max value
#clevel=0.38292492 ; 0.5-sigma,
#clevel=0.68268949 ; 1.0-sigma,
#clevel=0.86638560 ; 1.5-sigma,
#clevel=0.90       ; 1.645-sigma,
#clevel=0.95       ; 1.960-sigma,
#clevel=0.95449974 ; 2.0-sigma,
#clevel=0.98758067 ; 2.5-sigma,
#clevel=0.99       ; 2.575-sigma,
#clevel=0.99730020 ; 3.0-sigma,
#clevel=0.99953474 ; 3.5-sigma,
#clevel=0.99993666 ; 4.0-sigma,
#clevel=0.99999320 ; 4.5-sigma,
#clevel=0.99999943 ; 5.0-sigma,
#clevel=0.99999996 ; 5.5-sigma,
#clevel=0.999999998; 6.0-sigma.
if use_gaussian == 1:   
   clevel = 0.98758067 # 2.5-sigma
else:   
   clevel = 0.90 # 1.645-sigma

walk_num = 30
iteration_num = 500

input1 = np.array([1., 2.])
input1_err = np.array([0.2, 0.5])
input1_err_p = input1_err
input1_err_m = -input1_err
output1 = myfunc21(input1)
output1_num = len(output1)

mcmc_sim = pyemcee.hammer(myfunc21, input1, input1_err_m, input1_err_p, 
                          output1, walk_num, iteration_num, 
                          use_gaussian, print_progress=1)

output1_error = pyemcee.find_errors(output1, mcmc_sim, clevel, do_plot=1, image_output_path=image_output_path)

for i in range(0, output1_num):
   print(output1[i], output1_error[i,:])

walk_num = 30
iteration_num = 100
#class fcnStruct(NamedTuple):
#   scale1: float
#   scale2: float
fcnargs = {'scale1':0.0, 'scale2':0.0}
input1 = np.array([1., 2.])
input1_err = np.array([0.2, 0.5])
input1_err_p = input1_err
input1_err_m = -input1_err
scale1=2.
scale2=3.
#fcnargs = fcnStruct(scale1, scale2)
fcnargs['scale1']=scale1
fcnargs['scale2']=scale2
output1 = myfunc22(input1, functargs=fcnargs)
output1_num = len(output1)

mcmc_sim = pyemcee.hammer(myfunc22, input1, input1_err_m, input1_err_p, 
                          output1, walk_num, iteration_num, 
                          use_gaussian, print_progress=1, functargs=fcnargs)
                          
output1_error = pyemcee.find_errors(output1, mcmc_sim, clevel, do_plot=1)

for i in range(0, output1_num):
   print(output1[i], output1_error[i,:])

