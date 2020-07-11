import argparse
import os
import sys
from datetime import datetime


## SETUP: PARSE ARGUMENTS AND SET UP RUN DIRECTORY ##

#print the command line arguments
print("Command line arguments are:")
print(sys.argv)

#cuts = 1, walkers = 1, plot = True, proportion = 0.5, p_debug = False)
#set up command line arguments
parser = argparse.ArgumentParser(description='Run a topo_tools analysis.')
parser.add_argument('--cuts', dest='cuts', default=2,
                   help='The number of vertical/horizontal partitions (2 cuts = 9 cells)')
parser.add_argument('--walkers', dest='walkers', default=10,
                   help='The number of random walkers that will start in the center of each cell')
parser.add_argument('--plot', dest='plot', action='store_true',
                   help='plot output or not (default: False)')
parser.add_argument('--proportion', dest='proportion', default=0.5,
                   help='The proportion that the random walkers will optimize speed vs travel direction')
parser.add_argument('--time', dest='time', default=8.0,
                   help='The time that the random walkers will walk for')
parser.add_argument('--size', dest='size', default=5,
                   help='The number of vertical/horizontal partitions (size 5 = 36 cells)')
parser.add_argument('--windows', dest='windows', default=None,
                   help='The path to the directory with the already created windows')



#parse command line arguments
args = parser.parse_args()


## RUN THE SCENARIO ##

import sys
from topo_tools import topo_tools

date, curr_ = str(datetime.now()).split()
#print(curr_)
hour, min_, sec = curr_.split(':')
dir_str = "{}_{}.{}_{}_{}_{}_{}".format(date,hour,min_ ,args.time, args.size, args.cuts,args.walkers)
#print(dir_str)
os.system("mkdir -p {}".format(dir_str)) #make output directory

topo_file = 'OG_topo.npy'
lons_file = 'OG_lons.npy'
lats_file = 'OG_lats.npy'

#print('PLOT', args.plot, type(args.plot))
obj = topo_tools(topo_file, lons_file, lats_file)
obj.run(cuts       = int(args.cuts),  			\
		walkers    = int(args.walkers), 		\
		plot       = args.plot, 				\
		proportion = float(args.proportion),	\
		time       = float(args.time), 			\
		size       = int(args.size), 			\
		dir_str    = dir_str,					\
        windows    = args.windows               )

print("Scenario run complete. Results are in the run directory: ")
