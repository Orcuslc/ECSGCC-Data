## The Structure of NN

## Usage for NN in Forecasting:
	1. Reason for using NN: 
		1.1 Quantitative forecasting is based on extracting patterns from observed past events and extrapolating them into the future.
		1.2 NN can be seen as multivariate, nonlinear and nonparametric methods, which can be expected to model complex nonlinear relationships better than traditional linear models.
		1.3 NN are data-driven methods, and it's not nec. for researchers to postulate tentative models and estimate parameters.
	2. Overview of NN-based Forecasting System
		2.1 The multilayer perceptrons can be classified into two groups:
			2.1.1 One output node, used to forecast next hour's load, next day's PEAK load or TOTAL load.
			2.1.2 Several output nodes, used to forecast a sequence of hourly loads; Typically have 24 nodes, to forecast the next 24 hours.
		2.2 Structure of The NNs 
			2.2.1 The first group:
				2.2.1.1 Some examples of different NN structures.
				2.2.1.2 Ways to forecast profiles
					2.2.1.2.1 Repeatedly forecasting one hourly load at a time.
					2.2.1.2.2 Use a system with 24 NNs in parallel, one for each hour.
			2.2.2 The second group:
				2.2.2.1 Some examples of NNs with several input nodes to forecast profiles
				2.2.2.2 Examples of models in which several NNs work together to compute the forecasts.
					2.2.2.2.1 12NNs, each for a month.
					2.2.2.2.2 38NNs, for Monthly, daily and weekly modules, results are linearly combined.
					2.2.2.2.3 24NNs, each for an hour of the day.
				2.2.2.3 Examples with TWO NNs: One of them was trained to produce a first forecast of tomorrow’s profile. The other one was trained to estimate tomorrow’s load changes with respect to today’s loads; these changes, added to today’s loads, made up a second forecast of tomorrow’s profile. The forecasts produced by both methods were linearly combined. The second NN allow the system to adapt more quickly to abrupt changes in temperature.
				2.2.2.4 Hourly Loads classified according to season(7 classes), day of the week(3 classes), period of the day(5 classes), each of the classes modeled by one of the INDEPENDENT NNs.
			2.2.3 Examples about Usage of FUSSY LOGIC in NNs
				2.2.3.1 fussy processor, receive quantitative and qualitative data, put 4 fussy numbers measure expected load change in each of the 4 periods of the day. The numbers and temperature data are fed into the NN.
				2.2.3.2 fussy processor after the NN.
				2.2.3.3 Devide the load to a normal load and a weather sensitive load. Normal is modeled by 3 NNs(weekday, Satur, Sun), weather sen. load modeledny a fussy engine.
	3. Issues in designning a NN-based Forecasting system
		3.1 Data pre-processing
			3.1.1 Reduce data demension, clean the data;
				Partition the input space and design a model for each subspace.
			3.1.2 In load forecasting, it can be done by classifying data(past load profiles, weather)
			3.1.3 The most important factor is the calendar date(weekday, weekend); Monday, Fridays sometimes need special models; The number of classes can rise to 11; should be classified according to month or season;
			3.1.4 Holidays: with weekdays or reserve special classes;
			3.1.5 Weather: days classified with statistical methods of similarity; by fuzzy engines;
			3.1.6 handling of classifying:
				3.1.6.1 class label to each profiles in sample;
				3.1.6.2 build different NNs for each class;
				3.1.6.3 build a NN with seperate set of weights for each class;
		3.2 NN designning
			3.2.1 Most: Normal NN; some recursive; Most fully-connected;
			3.2.2 number of hidden layers, input nodes, neurons per layer, type of activation functions;
				3.2.2.1 One or two hidden layers
				3.2.2.2 logistic, hyperbolic tangent function;
				3.2.2.3 number of neurons:
					1. output neurons: (by forecasting methods)
						1.1 Iterative Forecasting:(h+1 based on 1, 2, ..., h): recursive NN
							 If the model is an ARIMA, it may be shown that the forecasts will eventually converge to the series average. However, it is not clear what happens if the model is a MLP.
						1.2 Multi-Model Forecasting:
							multi NNs in parallel, not likely to overfitted
						1.3 Single-Model Multivariate Forecasting:
							each file is a vector
							Drawback: 1.  MLPs must be very large
									2.  treating each day as a vector means that one year of data will yield only 365 data points, which seems to be too few for the large MLPs required.
					2. Number of Input Nodes: priori knowledge about the system and the output of teh system;
						2.1 the load series; according to the structures of model
						2.2 air temperature, humidity, wind speed
					3. Number of hidden neurons: by trial and experience
		3.3 NN implementation: training
			Most common: BP 
			stop after a fixed number of iterations; or errors below .
		3.4 Validation: test by tesing examples;
	4. Guildlines
		



