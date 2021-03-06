import numpy as np
import random
from daily_dist import *

load_path = '../../Load-Data/load_before_2013_clean.csv'
daily_dist = '../../Load-Data/dist_before_2013.txt'

def read_dist(daily_dist):
	with open(daily_dist) as f:
		times = f.read().split('\n')[:-1]
		dists = [item.split(',')[:-1] for item in times]
		dists = [[item.split(':') for item in j] for j in dists]
		return [[[float(x) for x in y] for y in z] for z in dists]

class Monte_Carlo:
	'''
	The class for simulation using Monte Carlo Methods
	'''
	def __init__(self, dist_path):
		'''
			dists: A list of distributions, with each element is a distribution of a r.v.;
			The structure of each element is:
				[[a, b], [c, d]], which means the r.v. x obeys:
					p(x=a) = b, p(x=c) = d.
			e.g.:
				dists = [
							[[1, 0.11], [2, 0.89]],
							[[2, 0.12], [3, 0.13], [4, 0.75]]
						]
		'''
		dists = read_dist(dist_path)
		self.dists = dists
		# print(self.dists)

	def _simulation(self, adist, number):
		'''
			The simulation for a single distribution.
			adist: The distribution
			number: The number of outputs
		'''
		values = np.asarray([item[0] for item in adist])
		probs = np.asarray([item[1] for item in adist])
		probs = probs/sum(probs)
		accumulate_probs = np.asarray([sum(probs[:i+1]) for i in range(len(probs))])
		p_list = [random.random() for i in range(number)]
		loc_list = [np.where(accumulate_probs >=p_list[i])[0][0] for i in range(number)]
		return [values[i] for i in loc_list]

	def simulation(self, number):
		'''
			The simulation for users
			number: The length of output
		'''
		return([self._simulation(adist, number) for adist in self.dists])

	def simulation_mean(self, number):
		sim = self.simulation(number)
		return [[sum(item)/number] for item in self.simulation(number)]

	def calc_err(self, sim, data):
		return (np.avearge(np.asarray(sim), axis=1-np.average(np.asarray(data), axis=0)))

def draw(start, end, load_path):
	daily_load = get_load_data(start, end, load_path)
	avg = np.nanmean(daily_load, axis=0)
	plt = plot_load(daily_load)
	MC = Monte_Carlo(daily_dist)
	for number in [1, 10, 100, 1000]:
		predict = MC.simulation(number)
		pred = np.asarray([item[0] for item in predict]) + avg
		plt.plot(range(48), pred, linewidth=2)
	plt.show()

# def calc_err():



if __name__ == '__main__':
	# read_dist(daily_dist)
	# run(daily_dist)
	draw('20090911', '20130901', load_path)
