from sklearn.svm import SVR
from matplotlib import pyplot as plt
from matplotlib import dates as mdt
import numpy as np
import datetime as dt
from conf import *

str2float = lambda alist: [float(i) for i in alist]

class Predictor:
	"""
	The base class for prediction;

	Attributes
	----------
	Private:
		self._training_data : matrix-like
			training data, each line is a record point, the first of which is target, and 2:n is the attributes.
		
		self._x: matrix-like
			training data, the attributes.

		self._y : matrix-like
			training data, the targets.

	Public:


	Methods
	-------
	Public:

	"""
	def __init__(self, attr_path):
		self._training_data = self._read(attr_path)
		self._y = [float(record[0]) for record in self.training_data]
		self._x = [str2float(record[1:]) for record in self._training_data]

	def _read(self, attr_path):
		"""
		Read attributes from files;
		Private function, used only in self.__init__()

		Parameters
		----------
		attr_path : string
			The path of attributes.

		Returns
		-------
		data : matrix-like
			Each line of `data` is a record point.

		Raises
		------
		"""
		with open(attr_path) as f:
			data = f.read().split('\n')
		for index in range(len(data)):
			data[index] = data[index].split(' ')[:-1]
		return data[:-1]

	def train(self):
		

