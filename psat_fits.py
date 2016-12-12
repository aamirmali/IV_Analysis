import Pyro4
import numpy as np
import os
import argparse
import time
import matplotlib.pyplot as plt
from scipy.optimize import leastsq
#adding test comment to check that versioning is making sense
#changing it further to continue checking
#oja

parser = argparse.ArgumentParser(description='arguments')
parser.add_argument('filename', type=str, help='filename of sorted temp/psat data')
parser.add_argument('--file_directory', type=str, default='/data/cryo/current_data/', help = 'file directory')
# cols argument helps make sure we get our labels right. if total number doesn't agree with number of columns from data file then you'll get mislabling
parser.add_argument('--cols', nargs='+', type = int, help='list of columns to run on. total number should agree with numbers of columns  from data file')
# default = 0 1 2 3 4 5 6 7 8, help='list columns to run on')
parser.add_argument('--num_rows', type = int, default = 22, help='number of rows. default 22')

args = parser.parse_args()
filename = args.filename
cols = args.cols
num_rows = args.num_rows


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

def g(K,Tc):
    return 4.*K*(Tc**3.)

p0 = [1500,150]

# create list to define row column labeling
labels = []
for i in cols:
    for j in xrange(num_rows):
        labels.append('C%sR%s' % (i,j))

print 'labels', labels


# populate array with fit params 
for i in np.arange(np.size(data[0,:])-1):
    P_sat = data[:,i+1]
    where_good = np.where(P_sat>0)
    if np.size(where_good) > 2:
        P_sat = P_sat[where_good]
        T_bath = temp[where_good]
        #print 'size P_sat', np.size(P_sat)
        #print 'size T_bath', np.size(T_bath)
        fit = leastsq(residuals, p0, args=(P_sat,T_bath))
        fit_params = fit[0]
        x1 = fit_params[0]
        x2 = fit_params[1]
        G = g(x1,x2)
        #print 'G', G
        data_slice = [i, labels[i-1], x1, x2]
        print 'data_slice', data_slice



