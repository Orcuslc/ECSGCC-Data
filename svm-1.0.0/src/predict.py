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

		self._testing_data : matrix-like, maybe empty
			testing data, each line is a record point, the first of which is target, and 2:n is the attributes.
		
		self._training_x: matrix-like
			training data, the attributes.

		self._training_y : matrix-like
			training data, the targets.

		self._testing_x : matrix-like, maybe empty
			testing data, the attributes

		self._testing_y : matrix-like, maybe empty
			testing data, the target

	Public:
		self.clf : SVR model
			generated and trained by self.train()

		self.

	"""
	def __init__(self, attr_path, n):
		"""
		Initialize self.

		Parameters
		----------
		attr_path : string
			The path of attributes.

		n : int
			The number of record points;
			The first n points are used as training data, and the latter points as testing data(if exists)

		Returns of self._read()
		-------
		data : matrix-like
			Each line of `data` is a record point.
			The first n rows of data is regarded as training data, the n:-1 rows of data as testing data.
			If n == len(data) - 1:
				we regard test data as an empty list.

		Raises
		------
		IndexError:
			If n >= len(data).
		"""
		self._training_data, self._testing_data = self._read(attr_path, n)
		self._training_y = [float(record[0]) for record in self._training_data]
		self._training_x = [str2float(record[1:]) for record in self._training_data]
		self._testing_x = [str2float(record[1:]) for record in self._testing_data]
		self._testing_y = [float(record[0]) for record in self._testing_data]

	def _read(self, attr_path, n):
		"""
		Read attributes from files;
		Private function, used only in self.__init__()

		Parameters
		----------
		attr_path : string
			The path of attributes.

		n : int
			The number of training data points.

		Returns
		-------
		data : matrix-like
			Each line of `data` is a record point.
			The first n rows of data is regarded as training data, the n:-1 rows of data as testing data.
			If n == len(data) - 1:
				we regard test data as an empty list.

		Raises
		------
		IndexError:
			If n >= len(data).
		"""
		with open(attr_path) as f:
			data = f.read().split('\n')
		for index in range(len(data)):
			data[index] = data[index].split(' ')[:-1]
		if n >= len(index):
			raise IndexError("n must be less than the number of record points.")
		return data[:n], data[n:-1]

	def train(self):
		"""
		Generate and train the model with SVR.
		The model is saved as self.clf

		Parameters
		----------
		No input parameters need.

		Returns
		-------
		No returns.
		"""
		self.clf = SVR(C = C, gamma = gamma)
		self.clf.fit(self._training_x, self._training_y)

	def predict(self, x = None, y = None):
		"""
		Predict 

