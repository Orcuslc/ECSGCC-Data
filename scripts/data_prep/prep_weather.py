import pandas as pd

raw_weather_root = '../../Raw-Data/Weather/shanghai.csv'
weather = pd.read_csv(raw_weather_root, encoding='gbk'
	, index_col='date')
index = weather.index
for i in weather.loc[index].