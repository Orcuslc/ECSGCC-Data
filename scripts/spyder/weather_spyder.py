import requests as rq
from bs4 import BeautifulSoup as bs
import os, sys, io
import datetime as dt
import pandas as pd
import numpy as np

if os.name == 'nt': # Check if the system is Windows-NT
	sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8') # Change the standard output codec to UTF-8

def handle_empty(s):
	return s and s.strip()

class weather_spyder:
	def __init__(self):
		self.url = 'http://lishi.tianqi.com/'
		self.headers = {
			# GET /20160601.html HTTP/1.1
			'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
			'Accept-Language': 'zh-Hans-CN,zh-Hans;q=0.8,en-US;q=0.5,en;q=0.3',
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393',
			# 'Accept-Encoding': 'gzip, deflate',
			'Host': 'shanghai.tianqi.com',
			'Connection': 'Keep-Alive',
			'Cookie': 'Hm_lvt_ab6a683aa97a52202eab5b3a9042a8d2=1469240418; BAIDU_SSP_lcr=https://www.baidu.com/link?url=87VHQgOUzyO4TH6Sj4UOXwWlppbvPRaeZGtiCGUgf58251y2I2yPvG845AE5r-2g&wd=&eqid=92ed76940013e6fb000000045792c0c2; Hm_lpvt_ab6a683aa97a52202eab5b3a9042a8d2=1469240439; CNZZDATA1259566218=2073371739-1469236901-http%253A%252F%252Flishi.tianqi.com%252F%7C1469236901; a8205_pages=1; a8205_times=1'
			}
	
	def get_data(self, city, time):
		# url = self.url[:7]+city+'.'+self.url[7:]+'/'+time+'.html'
		url = self.url+city+'/'+time+'.html'
		page = rq.get(url, headers=self.headers)
		self.soup = bs(page.content.decode('gbk'), "lxml")
		# print(self.soup.prettify())
		tag = self.soup.div
		while True:
			try:
				# print(tag)
				a = tag["class"]
				# print(a[0])
				if a[0] == 'tqtongji2':
					return tag.getText()
				else:
					tag = tag.findNext()
			except BaseException:
				tag = tag.findNext()

	def run(self):
		col = ['日期', '最高气温', '最低气温', '天气', '风向', '风力']
		cities = ['shanghai']
		# start = dt.date(2011, 1, 1)
		# dates = [(start+dt.timedelta(days=i)).strftime('%Y%m%d') for i in range(2008)]
		years = ['2011', '2012', '2013', '2014', '2015', '2016']
		months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
		dates = [i+j for i in years for j in months][:-6]

		for city in cities:
			rowlist = []
			# table = pd.DataFrame(columns = col)
			for date in dates:
				a = self.get_data(city, date)
				data = list(filter(handle_empty, a.split('\n')))[6:]
				for i in range(int(len(data)/6)):
					row = zip(col, data[6*i:6*i+6])
					# print(dict(row))
					# table.append(dict(row), ignore_index=True)
					rowlist.append(dict(row))
			table = pd.DataFrame(rowlist, columns=col)
			table.to_csv('E:\\Desktop\\data\\'+city+'.csv', if_exists = 'replace')

if __name__ == '__main__':
	a = weather_spyder()
	a.run()


