Notes
---
## Summary
- Goal: To predict daily load demand of a month (Mid-Term Forecasting)
- Info Given: 
	- Past two-year load demand data, half-hour recorded.
		- In the paper, max load is high in winter and low in summer
		- Load demand in weekend is lower than weekdays
		- Saturday is a little higher than Sunday
	- Previous four-year daily temperature
		- Conditions: temperature, humidity, illumination, special events(typhoon, sleet)
	- Local holiday events (Date of holidays)
		- In the paper, the load on holidays is lower
		- Effection related to the type of holidays
- Technique: SVM(SVR)
	- Training data: $(x_{i}, y_{i})$, where $x_{i}$ are input vectors and $y_{i}$ are output values.
	- Package: libsvm (In Python we use sklearn.svm.SVC)
- Evaluation: Error metric, stated with Mean Absolute Percentage Error(MAPE), 
	  $$MAPE = 100\frac{\Sigma_{i=1}^{n}|\frac{L_{i}-\hat L_{i}}{L_{i}}|}{n}$$
	- $n$: the number of days in the month
	- $L_{i}, \hat L_{i}$: the REAL and PREDICTED value of max daily load on $i$th day
- Conclusion: In 30-day-period forecasting, in which the temperature does not vary much, temp. data is useless.
---
## Experiments
1. Data Prep.
	1. Feature Selection: Use info from the same day and earlier as features.
		- Calendar Attributes (weekdays, holidays)
		- Weather (temperature, wind, sky cover, humidity); but in use of mid-term forecasting, the prediction of weather may not be accurate.
		- Time series style or NOT (choose the delta, the length of previous predictions)
	2. Data Segmentation: Consider a subset for load data (for seasonal pattern, etc)
		- For nonstationary time series, $$y_{t} = f_{i(t)}(x_{t}), \forall t = \Delta+1, ..., l.$$ where $x_{t} = (y_{t-1}, y_{t-2}, ..., y_{t-\Delta})$.
		- Steps:
			1. Linearly scale all load data to [0, 1], then incorporate load of last 7 days and weekday information to attributes to get time series style data.
			2. Follow [11] to analyze the data. (Unsupervised data segmentation) **
			3. After seperate the time series, it's better to consider only ONE segment related to the same series of the time to predict.
	3. Data Representation: Prepare combinations of training data sets.
		- Entry: (calender, temp.(opt.), past load(opt.))
		- Use 7 binaries to encode calender info:
			- weekdays, 5 (Monday as 000001, Tuesday as 000010, etc.)
			- weekends, 1 (Saturday as 100000, Sunday as 000000)
			- holidays, 1 (if is holiday then add 1 at the beginning, else add 0)
		- Use 1 numerical attribute for normalized temp. data
		- Use 7 numerics for past 7 daily max loads
		- Lack of future weather data:
			- Use the average of the past temp data as estimation
			- Use a linear combination of places near the target place
			- [15], but impractical
		- If the model can learn well on holidays, when the dataset is pretty small.
2. Implementation:
	- Build an SVM model: Parameters TBD
		- $\epsilon$, the width of insensitive tube, is FIXED to 0.5
		- Mapping func $\phi$, consider RBF kernel, $K(x_{i}, x_{j}) = e^{-\gamma||x_{i}-x_{j}||^2}$
		- N, the number of previous days to include, is chosen to 7.
		- Left:
			- Cost of error $C$
			- $\gamma$
	- Search for Proper parameters:
		- Divide the training data into 2 sets, one used to train, the other to validate and evaluate.
		- Validation:
			- For time-series-based approaches, extract some time periods to form the validation set.
			- For non-time-series models, conduct tenfold cross validation. Randomly divide training into 10 sets, using each set as validation, then train a model on the rest. 
			

