import numpy as np
import random
from daily_dist import *

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
	def __init__(self, dists):
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
		self.dists = np.asarray(dists)

	def _simulation(self, adist, number):
		values = adist[:, 0]
		probs = adist[:, 1]
		probs = probs/sum(probs)
		accumulate_probs = np.asarray([sum(probs[:i+1]) for i in range(len(probs))])
		p_list = [random.random() for i in range(number)]
		loc_list = [np.where(accumulate_probs <= p_list[i])[0][-1] for i in range(number)]
		return [values[i] for i in loc_list]

	def simulation(self, number):
		return([self._simulation(adist, number) for adist in self.dists])




if __name__ == '__main__':
	# read_dist(daily_dist)
	run(daily_dist)