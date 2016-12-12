import Pyro4
import numpy as np
import os
import argparse
import time
import matplotlib.pyplot as plt
from scipy.optimize import leastsq

parser = argparse.ArgumentParser(description='arguments')
parser.add_argument('filename', type=str, help='filename of sorted temp/psat data')
parser.add_argument('--file_directory', type=str, default='/data/cryo/current_data/', help = 'file directory')

args = parser.parse_args()
filename = args.filename


#load psat data

data = np.loadtxt(filename)
header = data[0,:]
data = np.loadtxt(filename, skiprows=1)
temp = data[:,0]

#load temp array to serve as x-axis for fit
temp_arr = np.max(temp)-np.min(temp)
temp_arr = temp_arr*100.
temp_arr = np.arange(temp_arr)
temp_arr = temp_arr/100.
temp_arr = temp_arr + np.min(temp)

#So far Temps are both in mK. need to convert to K
temp = temp/1000.
temp_arr = temp_arr/1000.

# define functions that we'll be using to perform the fit
# here we assume that we are only fitting for K and Tc, n is fixed as 4
def residuals(p,y,x):
    K,Tc = p
    err = y - K*(Tc**4. - x**4.)
    return err

def Psat(x,p):
    return p[0]*(p[1]**4. - x**4.)

def G(K,Tc):
    return 4.*K*(Tc**3.)

p0 = [1500,150]

# create array to hold params and G value 
 
for i in np.arange(np.size(data[0,:])-1):
    P_sat = data[:,i+1]
    where_good = np.where(P_sat>0)
    if np.size(where_good) > 2:
        P_sat = P_sat[where_good]
        T_bath = temp[where_good]
        print 'size P_sat', np.size(P_sat)
        print 'size T_bath', np.size(T_bath)
        fit = leastsq(residuals, p0, args=(P_sat,T_bath))
        print 'i', i
        print 'fit params', fit[0]



