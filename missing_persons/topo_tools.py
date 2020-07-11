import matplotlib.pyplot as plt
from scipy.interpolate import griddata
from scipy.interpolate import interp2d
import numpy as np
from scipy import linalg as la

from matplotlib.collections import LineCollection
import random

import math
import os

from time import time as TIME

class topo_tools:
	def __init__(self, topo_path, lons_path, lats_path):
		self.topo_name = topo_path.split('_')
		self.lons_name = lons_path.split('_')
		self.lats_name = lats_path.split('_')

		self.topo      = self.load_topo_npy(topo_path)
		self.lons, self.lon_left, self.lon_right, self.lon_n  = self.load_lons_npy(lons_path)
		self.lats, self.lat_low , self.lat_high , self.lat_n  = self.load_lats_npy(lats_path)

		# set the corners of the map
		self.bbox = [self.lon_left, self.lon_right, self.lat_low, self.lat_high]
		# lattitue and longitude with the correct number of steps.
		self.lon_domain = np.linspace(self.lon_left, self.lon_right, self.lon_n).astype('float32')
		self.lat_domain = np.linspace(self.lat_low, self.lat_high  , self.lat_n).astype('float32')

		# delta x and delta y, the difference between the first and second position
		# the difference between each step is the same
		self.xeps       = abs(self.lon_domain[0] - self.lon_domain[1])
		self.yeps       = abs(self.lat_domain[0] - self.lat_domain[1])

		# changes depending on where you are on the earth, for this region this is the value
		self.ykm_deg    = 111.13014012508017 # km per degree
		self.xkm_deg    = 90.97190820834038   # 81.21151090400674  # km per degree

		# kilometers per step size
		# this is the walkers step size
		self.ykm_step   = self.ykm_deg * self.yeps
		self.xkm_step   = self.xkm_deg * self.xeps

		# a person averages 3.2 km per hour, used to generate walking speed function
		self.xvel       = 3.2 #3.2-4.8 km/hour
		self.yvel       = 3.2

		# may or may not be used
		self.xdeg_hr    = self.xvel / self.xkm_deg #deg per hr
		self.ydeg_hr    = self.xvel / self.ykm_deg #deg per hr

		# polynomial that fits the fake walking speed data
		self.p          = self.fit_cheby(18)

		# (degrees (xeps) * kilometers per degree ) / (km/hr) = how many hours it takes to take a step at this speed.
		self.xdt        = self.xkm_step / self.xvel
		self.ydt        = self.ykm_step / self.yvel

		# NEEDS TO BE REVISED TO HAVE VELOCITY BE A VARIABLE. TO MAKE WALKERS TIME DEPENDET.
		self.dt         = max(self.xdt,self.ydt)

		# total X/Y distance
		self.xdist = self.xkm_deg * (self.lon_left - self.lon_right)
		self.ydist = self.ykm_deg * (self.lat_low - self.lat_high)

		# pythagoreum theorem to find the slope under the walekers feet.
		#self.gradx, self.grady = np.gradient(self.topo)
		#self.gradient   = np.degrees(np.arctan(self.grady / self.gradx))

		# the first element of the tuple is the vertical direction and the second is the horizontal direction
		self.map = {'E':(0,1), 'SE':(-1,1), 'S':(-1,0), 'SW':(-1,-1), 'W':(0, -1), 'NW':(1, -1), 'N':(1, 0), 'NE':(1, 1)}

	def plot(self, lons , lats , topo, levels = 80, alpha = 0.5, title = 'DEFAULT'):

		fig = plt.figure()
		ax = fig.add_subplot(111)
		cs = ax.contourf(lons, lats, topo, levels, alpha=alpha)
		plt.xlabel('longitude',fontsize=16)
		plt.ylabel('latitude',fontsize=16)
		#plt.clabel(cs, inline=1, fontsize = 10)
		plt.title(title)

		Xflat, Yflat, Zflat = lons.flatten(), lats.flatten(), topo.flatten()
		def fmt(x, y):
		    # get closest point with known data
		    dist = np.linalg.norm(np.vstack([Xflat - x, Yflat - y]), axis=0)
		    idx = np.argmin(dist)
		    z = Zflat[idx]
		    return 'x={x:.5f}  y={y:.5f}  z={z:.5f}'.format(x=x, y=y, z=z)
		plt.colorbar(cs)
		plt.gca().format_coord = fmt
		#plt.show()

	############## Utility functions, map between degrees and indecies, create new windows, load files etc #########
	################################################################################################################

	def topo_lookup(self, y):
		i,j = self.index_lookup(y)
		return self.topo[i][j]

	def fx_lookup(self, y):
		i, j = self.index_lookup(y)
		return self.gradx[i][j]

	def fy_lookup(self, y):
		i, j = self.index_lookup(y)
		return self.grady[i][j]

	def topo_m_to_km(self):
		self.topo = self.topo / 1000

	def load_topo_npy(self, filepath):
		return np.load(filepath)

	def load_lons_npy(self, filepath):
		lons  = np.load(filepath)
		left  = lons.min()
		right = lons.max()
		n     = lons.shape[1]
		return lons, left, right, n

	def load_lats_npy(self, filepath):
		lats = np.load(filepath)
		n    = lats.shape[0]
		low  = lats.min()
		high = lats.max()
		return lats, low, high, n

	def lon_lookup(self, lon):
		temp = np.abs(self.lon_domain) - abs(lon)
		return self.lon_domain[np.argmin(np.abs(temp))]

	def lat_lookup(self, lat):
		temp  = np.abs(self.lat_domain) -  abs(lat)
		return self.lat_domain[np.argmin(np.abs(temp))]

	def index_lookup(self, y):
		#This is to resolve reversed image problems when a new window is created
		# I don't totally understand why this is necessary, only that it works
		# I discovered this thru trial and error
		temp = self.lat_domain

		y         = y.astype('float32')
		lon_index = np.where( self.lon_lookup(y[0]) == self.lon_domain )
		lon_index = lon_index[0][0]

		lat_index = np.where( self.lat_lookup(y[1]) == temp)
		lat_index = lat_index[0][0]

		return lat_index, lon_index

	def new_window(self, bbox, window_num, dest = '.', plot = False): #bbox - left, right, low, high
		"""
		This function produces topo,lons,lats .npy files for a smaller 'window' with corners defined by bbox.
		If This function is called on a file that is produced by new_window the resulting window will be reversed.
		To avoid problems only make windows from the OG_*.npy files.
		Dest defines the directory where this file will be written.
		"""

		lon_left = self.lon_lookup(bbox[0])
		lon_right = self.lon_lookup(bbox[1])
		lat_down = self.lat_lookup(bbox[2])
		lat_up = self.lat_lookup(bbox[3])

		#generate new lats and lons by masking out the originals
		lon_domain = self.lon_domain[ self.lon_domain >= lon_left ]
		lon_domain = lon_domain[ lon_domain <= lon_right ]
		lat_domain = self.lat_domain[ self.lat_domain >= lat_down ]
		lat_domain = lat_domain[ lat_domain <= lat_up ]

		n = len(lon_domain)
		m = len(lat_domain)

		# create a new topography file from the new masked lats and lons
		z = np.zeros((m, n))

		i = 0
		for y in lat_domain[::-1]:
			j = 0
			for x in lon_domain:
				# k and l are the indicies of the smaller window
				# x and y are degrees and we need to map degrees into indicies
				k,l = self.index_lookup(np.array([x,y]))
				z[i][j] = self.topo[k][l]
				j += 1
			i += 1

		lons, lats = np.meshgrid(lon_domain, lat_domain)

		np.save(os.path.join(dest,'BOX' + str(window_num) + '_' + self.topo_name[-1]), z)
		np.save(os.path.join(dest,'BOX' + str(window_num) + '_' + self.lons_name[-1]), lons)
		np.save(os.path.join(dest,'BOX' + str(window_num) + '_' + self.lats_name[-1]), lats)

		if plot:
			self.plot(lons, lats,z, 80, alpha=0.5, title='New Window')

			self.plot(self.lons, self.lats, self.topo, title='Old Window')
			plt.plot([lon_left, lon_right], [lat_down, lat_down], '-r')
			plt.plot([lon_left, lon_right], [lat_up, lat_up], '-r')
			plt.plot([lon_left, lon_left], [lat_down, lat_up], '-r')
			plt.plot([lon_right, lon_right], [lat_down, lat_up], '-r')

			plt.show()

	def new_res(self, res, method = 'cubic', alpha = 0.5, levels = 80, show_three = False):
		xpos = self.lons.flatten()
		ypos = self.lats.flatten()
		zval = self.topo.flatten()

		xcoord = np.linspace(self.lon_left, self.lon_right, res)
		ycoord= np.linspace(self.lat_low, self.lat_high, res)
		lons, lats = np.meshgrid(xcoord,ycoord)

		if show_three:
			topo = griddata((xpos,ypos),zval,(lons,lats),method='nearest')

			fig = plt.figure()
			plt.rcParams['figure.figsize'] = [10, 10]
			ax = fig.add_subplot(221)
			plt.contourf(self.lons, self.lats, self.topo, 80, alpha=0.5)
			plt.title('Original')

			ax2 = fig.add_subplot(222)
			plt.contourf(lons, lats,topo, 80, alpha=0.5)
			plt.title('Nearest')

			topo = griddata((xpos,ypos),zval,(lons,lats),method='linear')
			ax3 = fig.add_subplot(223)
			plt.contourf(lons, lats,topo, 80, alpha=0.5)
			plt.title('Linear')

			topo = griddata((xpos,ypos),zval,(lons,lats),method='cubic')
			ax4 = fig.add_subplot(224)
			plt.contourf(lons, lats,topo, 80, alpha=0.5)
			plt.title('Cubic')

			plt.tight_layout()


		topo = griddata((xpos,ypos),zval,(lons,lats),method=method)

		np.save(self.topo_name[0] + '_' + str(res) + '_' + self.topo_name[-1], topo)
		np.save(self.lons_name[0] + '_' + str(res) + '_' + self.lons_name[-1], lons)
		np.save(self.lats_name[0] + '_' + str(res) + '_' + self.lats_name[-1], lats)

		if not show_three:
			self.plot(self.lons, self.lats, self.topo, levels, alpha, title = 'Old_res')
			self.plot(lons, lats, topo, levels, alpha, title='New Res')

	################### Functions used for random walk and generation of Adjacency matrix ############
	##################################################################################################

	def fit_cheby(self, n, plot = False, p_xy = False):
		x = np.array([ -90,  -80,  -66,  -45, -30, -15,   0,  15,  30,  45,   55,   72,   90])
		#x = x*-1 #posiive degrees are downhill for whatever reason
		y = np.array([1e-5, 1e-5, 1e-5, 1e-3, 0.5, 4.8, 3.2, 2.8, 2.3, 0.5, 1e-5, 1e-5, 1e-5])
		d = np.linspace(-90,90, 1000)
		p = np.polynomial.Chebyshev.fit(x, y, n)
		if plot:
			fig = plt.figure()
			plt.plot(x,y, '.k')
			plt.plot(d,p(d))
		if p_xy:
			print('x',x)
			print('y',y)
		if plot:
			return p, fig
		return p

	def func(self,x):
		if x < -31:
			return 1e-5
		elif x > 55:
			return 1e-5
		else:
			return np.abs(self.p(x))

	def check_steepness(self, y, plot= False):

		# point is the index lookup of the point that we are at.
		point = np.array([self.lon_lookup(y[0]), self.lat_lookup(y[1])])
		#point = np.array([obj.lon_lookup(-107.345), obj.lat_lookup(37.345)])

		if plot:
			self.plot(self.lons, self.lats, self.topo)
		# the 8 directions that you can go
		dirs  = [(0,1), (-1,1), (-1,0), (-1,-1), (0, -1), (1, -1), (1, 0), (1, 1)]

		speed = np.zeros(8)

		for idx, dir_ in enumerate(dirs):

			# for all 8 directions we do an index lookup
			# the index lookup takes in lat and lon and spits out coordinates
			i,j = self.index_lookup(point)
			z = self.topo[i][j]

			# this does the step in the direction that we want
			i += dir_[0]
			j += dir_[1]

			# skip if out of bounds
			if i >= self.lat_n or j >= self.lon_n:
				continue

			# calculate distance in both direction of the step
			xstep = dir_[0] * self.xkm_step
			ystep = dir_[1] * self.ykm_step
			step  = np.sqrt(xstep**2 + ystep**2)

			# find the altitude at the position that we have stepped to
			z1    = self.topo[i][j]

			# find the change in height from the last position to the current step
			h     = z1 - z
			theta = np.degrees(np.arctan(h/step))
			speed[idx] = self.func(theta)

			total_dist  = np.sqrt(h**2 + step**2)

			if plot:
				plt.plot(self.lons[i][j], self.lats[i][j], '.')
			#print(dir_,'{:.6} {:.6} {:.6}'.format(theta,z, z1))

		# you step whichever direction maximizes your speed.
		max_idx = np.argmax(speed)
		#print('speed', speed[max_idx], dirs[max_idx], self.map['E'])
		if plot:
			plt.plot(point[0],point[1],'.r')

		return dirs[max_idx], total_dist / speed[max_idx]

	def rand_dir(self):
		d = np.random.randint(1,9)

		if d == 1:
			return (0,1)
		elif d == 2:
			return (-1, 1)
		elif d == 3:
			return (-1,0)
		elif d == 4:
			return (-1,-1)
		elif d == 5:
			return (0,-1)
		elif d == 6:
			return (1, -1)
		elif d == 7:
			return (1,0)
		else:
			return (1,1)

	def rand_sign(self):
		d = np.random.randint(1,3)
		if d == 1:
			return 1
		else:
			return -1

	def random_walk(self, start, time = 8.0,proportion = 0.5, plot = False):
		"""
		Parameters:
		start     : ndarray (2,)  Starting position of the random walker
		time      : float 	      Time that will be consumed
		proportion: float         The porportion (probability) that the walker will optimize speed
		plot      : Bool 		  This is a debug option for plotting a single random walk (defaults to false)

		------
		Returns:
		x, y      : (tuple) ndarray The path of the random walker

		"""
		bbox = self.bbox
		x = np.array([start[0]])
		y = np.array([start[1]])

		# generate a random direction
		rand_dir = self.rand_dir()

		i = 0
		while time >= 0.0:
			# Through probability determine if the walker is optimizing speed or walking in a given direction
			num = np.random.random() #number between 0 and 1
			if num < proportion:
				dir_, dt = self.check_steepness(np.array([x[i],y[i]]))
				dt = np.min([1.,dt])
			else: # if the number is greater than the proportion then we walk in a particular direction
				#This is useful because it allows the random walkers to spread out instead of allways choosing
				#the same direction or getting caught in a local minimum.
				dir_ = rand_dir
				dt = self.dt

			#The degree step size is determined in each direction
			xstep = self.xeps * dir_[1]
			ystep = self.yeps * dir_[0]

			# i is current step
			x = np.append(x, x[i] + xstep)
			y = np.append(y, y[i] + ystep)

			# i+1 is the step we just took
			# if it is out of bounds repeat the step in the opposite direction
			if x[i+1] <= bbox[0]:
				x[i+1] = x[i] - xstep
			if x[i+1] >= bbox[1]:
				x[i+1] = x[i] - xstep
			if y[i+1] <= bbox[2]:
				y[i+1] = y[i] - ystep
			if y[i+1] >= bbox[3]:
				y[i+1] = y[i] - ystep

			i+=1
			time -= dt

		if plot:
			self.plot(self.lons,self.lats,self.topo)
			plt.plot(x,y)
			plt.show()
		return x, y

	def gen_walkers(self, bbox, walkers = 1, time = 8.0, proportion = 0.5, plot = False, p_idx = False):
		"""
		Parameters:
		bbox      : (list)  A list of the corners of the zone that the walkers will be generated in. bbox - left, right, low, high
		Walkers   : (int)   The number of walkers that will be generated from the center of the zone.
		time      : (float) The ammount of time that each walker will travel for.
		propotion : (float) The propotion that the walker will optimize speed vs travel direction

		Debug:
		plot  : (bool) Debug option for plotting results
		p_idx : (bool) Debug option for printing (x,y) coords

		------------
		Return:
		end : (list of tuples) Each entry is the end point of each random walk.
		"""

		#Find center
		xpt = (bbox[0] + bbox[1]) / 2
		ypt = (bbox[2] + bbox[3]) / 2
		center = np.array([xpt,ypt])

		#For each random walk, store its endpoint
		end = []
		if plot :
			self.plot(self.lons,self.lats,self.topo)
		for j in range(walkers):
			x,y = self.random_walk(center, time = time,proportion =proportion)
			if plot:
				plt.plot(x,y, label = str(j)  )
			end.append((x[-1], y[-1]))
		if plot:
			plt.show()
		return end

	def make_zones(self,n = 1):
		"""
		Parameters:
		n         : (int)  Number of cuts that will be made in the topography file (2 cuts == 9 cells)

		Returns   :
		zones     ; (list) A list of bboxes that define the corners of each cell. It reads Left to Right Top to Bottom
		"""

		# Use the number of cuts to define the step size (in degrees) that we will iterate over to define each cell
		dx = (self.lon_right - self.lon_left) / (n+1)
		dy = (self.lat_high - self.lat_low) / (n+1)

		# We use the indecies to count how many steps we take left to right top to bottom
		zones = []
		for j in range(1, n+2):
			for i in range(1, n+2):
				zones.append([self.lon_left + (i-1) * dx, self.lon_left + i * dx, self.lat_high - j*dy, self.lat_high - (j-1) * dy])

		return zones

	def get_stats(self, cuts = 1, walkers = 1,time = 8.0, proportion = 0.5, p_debug = False, plot = True):
		"""
		Parameters:
		cuts       : (int)   The number of vertical/horizontal partitions to topography file. (2 cuts == 9 cells)
		Walkers    : (int)   The number of walkers that will be generated from the center of the zone.
		time       : (float) The ammount of time that each walker will travel for.
		proportion : (float) The propotion that the walker will optimize speed vs travel direction

		Debug:
		plot    : (bool) Debug option for plotting results
		p_debug : (bool) Debug option for printing the zone index and adjacency matrix

		------------
		Return:
		end : (list of tuples) Each entry is the end point of each random walk.
		"""
		if plot:
			self.plot(self.lons,self.lats,self.topo)

		#collect all the zones
		zones = self.make_zones(cuts)
		A = np.zeros((len(zones), len(zones)))

		#FIRST  we generate a fixed quantity of random walkers for each zone
		ends = []
		for i, zone in enumerate(zones):
			end = self.gen_walkers(zone, walkers = walkers,time = time, plot = plot, proportion = proportion)
			if p_debug:
				print(i, A)

			#SECOND we figure out where all the walkers went for that zone
			for endpt in end:
				for j in range(len(zones)):
					if endpt[0] >= zones[j][0] and endpt[0] <= zones[j][1] and endpt[1] >= zones[j][2] and endpt[1] <= zones[j][3]:
						A[i][j] += 1

		return A / walkers

	def run(self, cuts = 1, walkers = 1,time = 8.0, proportion = 0.5,plot = False, size = 5,dir_str = 'DEFAULT', windows = None): #size == 5 makes 36 windows
		if windows == None:
			windows = self.make_zones(size)
			#TODO Look into the window being produced from wrong row problem
			print('creating windows...')
			start = TIME()
			for k,window in enumerate(windows):
				self.new_window(window, k, dest = dir_str)
			print('DONE', TIME() - start)
			load_dir = dir_str
		else:
			load_dir = windows

		#maybe do something with scipy.sparse so that we build a big matrix from block matricies
		Matricies = []
		#if files are already written then begin here
		print('creating Adjacency matricies...')
		for i in range((size + 1)**2):
			start = TIME()
			#Initialize topo_tools object of the window
			obj = topo_tools(os.path.join(load_dir, 'BOX'+str(i)+'_topo.npy'), \
							 os.path.join(load_dir, 'BOX'+str(i)+'_lons.npy'), \
							 os.path.join(load_dir, 'BOX'+str(i)+'_lats.npy'))
			# upsample???
			#####
			#Initialize topo_tools object of the upsampled window
			####
			#Produce Adjacency matrix
			adjacency_M = obj.get_stats(cuts = cuts, walkers = walkers, time = time, proportion = proportion, plot = plot )
			#Matricies.append(adjacency_M)
			print(i, TIME() - start)
			np.save(os.path.join(dir_str, 'BOX'+str(i)+'_ADJ'), adjacency_M)


#obj = topo_tools(os.path.join(dir_str, 'BOX0_topo.npy'), \
#os.path.join(dir_str, 'BOX0_lons.npy'), \
#os.path.join(dir_str, 'BOX0_lats.npy'))
