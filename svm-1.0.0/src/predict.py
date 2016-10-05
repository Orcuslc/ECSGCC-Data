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

		Returns of `self._read()`
		-------
		data : matrix-like
			Each line of `data` is a record point.
			The first n rows of data is regarded as training data, the `n:-1` rows of `data` as testing data.
			If `n` == `len(data) - 1`:
				we regard test data as an empty list.

		Raises
		------
		IndexError:
			If `n` >= `len(data)`.
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
			The first `n` rows of `data` is regarded as training data, the `n:-1` rows of `data` as testing data.
			If `n` == `len(data) - 1`:
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

	def predict(self, x = None, y = None, evaluate = False, error_list = [0.1, 0.2]):
		"""
		Predict the values with the pre-trained model self.clf.

		Parameters
		----------
		x : matrix-like, optional
			Record attributes for prediction.
			if there is no input `x`, then we regard `x` to be `self._testing_x`

		y : matrix-like, optional
			Record target for prediction.
			if there is no input `y`, and `evaluate` == True: we use `self._testing_y` as `y`.
			if `evaluate` == False: `y` is not necessary.

		`evaluate` : Boolen, optional
			If performance evaluating is necessary or not.

		Returns
		-------
		pred : array-like
			The prediction of target based on the model and input attributes

		avgerr : float
			The average relative error of prediction and real values.
			Default: None

		maxerr : float
			The max relative error of prediction and real values
			Default: None

		error_num : array-like
			The list containing values for calculating the number of data points that the error is above those values.
			Default: None

		Raises
		------
		AttributeError:
			If `len(x)` == 0 or
				`len(y) == 0 and `evaluate` == True
		"""
		if x == None:
			x = self._testing_x
		if len(x) == 0:
			raise AttributeError("There should be something to predict upon!")
		if y == None:
			y = self._testing_y
		if evaluate == True and len(y) == 0:
			raise AttributeError("If evaluation is needed, there should be a real target value!")
		pred = self.clf.predict(x)
		if evaluate == False:
			return pred, None, None, None
		else:
			avgerr, maxerr, error_num = self.evaluate(pred, y)
			return pred, avgerr, maxerr, error_num


	def evaluate(self, pred, real, error_list = [0.1, 0.2]):
		"""
		Evaluate the performance of prediction by calculating relative error.

		Parameters
		----------
		pred : array-like
			The prediction for target

		real : array-like
			The real values of target

		error_list : array-like, optional
			The list containing values for calculating the number of data points that the error is above those values.

		Returns
		-------
		avgerr : float
			The average error of the prediction

		maxerr : float
			The max error of the prediction

		error_num : array-like
			The number of error points over the error_list

		Raises
		------
		None
		"""
		err = abs(np.asarray(pred)-np.asarray(real))/np.asarray(real)
		avgerr = np.average(err)
		maxerr = max(err)
		error_num = []
		for i in error_list:
			error_num.append(len(np.where(err > error_list[i])[0]))
		return avgerr, maxerr, error_num

	def plot(self, begin, pred, real = None):
		"""
		Plot the prediction, real values and the relative error curve.

		Parameters
		----------
		begin : string, 8-len
			The begining of the prediction; have a length of 8.

		pred : array-like
			The prediction array.

		real : array-like, optional
			The real array.
		"""
		td = dt.date(2011, 1, 2) - dt.date(2011, 1, 1)
		begin = dt.date(int(begin[:4]), int(begin[4:6]) , int(begin[6:]))
		date_num = len(pred)
		date_list = [begin + td * i for i in range(date_num)]

		if real != None:
			pred, real = np.asarray(pred), np.asarray(real)
			p1 = plt.subplot(211)
			line1, = p1.plot(date_list, real, label = 'real', color = 'r')
			line2, = p1.plot(date_list, pred, label = 'pred', color = 'b')
			p1.legend(handles = [line1, line2])
			p2 = plt.subplot(212)
			line3, = p2.plot(date_list, abs(real-pred)/real, label = 'error', color = 'g')
			p2.legend(handles = [line3])
			p1.grid(True)
			p2.grid(True)
			plt.show()
		else:
			line1, = plt.plot(date_list, pred, label = 'pred', color = 'b')
			plt.legend(handles = [line1])
			plt.grid(True)
			plt.show()