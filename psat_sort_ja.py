import Pyro4
import numpy as np
import os
import argparse
import time

parser = argparse.ArgumentParser(description='arguments')
parser.add_argument('filename', help='filename format for each IV acquisition')
parser.add_argument('--min_temp', type=float, default=100, help = 'minimum temperature of sweep in K, default 100 mK')
parser.add_argument('--max_temp', type=float, default=220, help = 'maximum temperature of sweep in K, default 240 mK')
parser.add_argument('--temp_step', type = float, default=2, help ='resolution of temperature steps, default 2 mK')
parser.add_argument('--file_directory', type=str, default='/data/cryo/current_data/', help = 'file directory')
parser.add_argument('--num_col', type=int, default=8, help = 'number of columns to be organized')
parser.add_argument('--num_row', type=int, default=22, help = 'number of rows per column, default 22')


args = parser.parse_args()

min_temp = args.min_temp
max_temp = args.max_temp
temp_step = args.temp_step
filename = args.filename
file_directory = args.file_directory
num_col = args.num_col
num_row = args.num_row

num_pts = int((max_temp-min_temp)/temp_step)
num_pts = num_pts -1

a = time.time()
a = str(a)
dir_name = str(file_directory)





#time.sleep(21600)
psat_data_hdr = 'Temp'
for j in xrange(num_col):
    for k in xrange(num_row):
        psat_data_hdr = psat_data_hdr + ' C%sR%s' % (j,k)
 #np.append(psat_data_hdr, np.array('C%sR%s' % (j,k)))
    #psat_data_hdr = np.append(psat_data_hdr, np.array('Label'))

print "psat_data_hdr", psat_data_hdr
              
row_len = 1+(num_row)*(num_col)
psat_data_arr = np.zeros((row_len,))
psat_data_arr = np.reshape(psat_data_arr, (1,row_len))

for i in xrange(num_pts):
    temp = min_temp + i*temp_step
    temp = temp/1000.
    temp = temp*1000.
    fn = 'iv_%s.out' % (temp)
    data = np.loadtxt(file_directory+fn, dtype=str)
    arr_index = np.where(data=='<Psat_(pW)_C0>')
    data_a = np.array(temp)
    for j in xrange(num_col):
        arr_index = np.where(data=='<Psat_(pW)_C%s>' % j)
        data_b = data[arr_index[0]]
        data_b = data_b[:,1:]
        data_a = np.append(data_a, data_b)
        data_a = np.reshape(data_a, (1,-1))
    psat_data_arr = np.concatenate((psat_data_arr,data_a))
print 'psat_data_arr', psat_data_arr
print 'psat_data_arr shape', np.shape(psat_data_arr)
psat_data_arr = psat_data_arr.astype(np.float)
np.savetxt(file_directory+'psat_data.txt',psat_data_arr, header=psat_data_hdr) 


    #temp = str(temp)
    #os.system('ramp_tes_bias iv_%s s 24000 -50 480 0.1 1 30000 1' % (temp))

#srs.configure_pid_temperature(0.1)

#for i in num_points





