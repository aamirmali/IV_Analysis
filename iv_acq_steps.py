import Pyro4
import numpy as np
import os
import argparse
import time

parser = argparse.ArgumentParser(description='arguments')
parser.add_argument('filename', help='filename format for each IV acquisition')
parser.add_argument('--min_temp', type=float, default=100, help = 'minimum temperature of sweep in K, default 100 mK')
parser.add_argument('--max_temp', type=float, default=240, help = 'maximum temperature of sweep in K, default 240 mK')
parser.add_argument('--temp_step', type = float, default=2, help ='resolution of temperature steps, default 2 mK')
parser.add_argument('--file_directory', type=str, default='/data/cryo/current_data/', help = 'file directory')
args = parser.parse_args()

min_temp = args.min_temp
max_temp = args.max_temp
temp_step = args.temp_step
filename = args.filename
file_directory = args.file_directory

num_pts = int((max_temp-min_temp)/temp_step)
num_pts = num_pts + 1

a = time.time()
a = str(a)
dir_name = str(file_directory)



srs = Pyro4.Proxy('PYRONAME:MisterW.SRS')

#time.sleep(21600)
for i in xrange(num_pts):
    temp = min_temp + i*temp_step
    temp = temp/1000.
    srs.configure_pid_temperature(temp)
    time.sleep(600)
    os.system('auto_setup')
    time.sleep(10)
    x = time.time()
    x = str(x)
    temp = temp*1000.
    temp = str(temp)
    os.system('ramp_tes_bias iv_%s s 24000 -50 480 0.1 1 30000 1' % (temp))

srs.configure_pid_temperature(0.1)

#for i in num_points





