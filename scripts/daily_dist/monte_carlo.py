import numpy as np
import random

daily_dist = '../../Load-Data/dist_before_2013.txt'

def read_dist(daily_dist):
	with open(daily_dist) as f:
		times = f.read().split('\n')[:-1]
		dists = [item.split(',')[:-1] for item in times]
		dists = [[item.split(':') for item in j] for j in dists]
		return [[[float(x) for x in y] for y in z] for z in dists]


# def Monte_Carlo(dist):
# 	probs = np.asarray(dist)[:, 1]
# 	print(probs.sum())

# def run(daily_dist):
# 	dists = read_dist(daily_dist)
# 	for i in range(48):
# 		Monte_Carlo(dists[i])

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
		self.dists = dists
		
	def 


if __name__ == '__main__':
	# read_dist(daily_dist)
	run(daily_dist)