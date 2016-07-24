# Carbon Trading Spyder
import requests as rq
import os, sys, io
from bs4 import BeautifulSoup as bs
import pandas as pd
import json

if os.name == 'nt': # Check if the system is Windows-NT
	sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8') # Change the standard output codec to UTF-8

class carbon_spyder:
	def __init__(self):
		self.url = 'http://k.tanjiaoyi.com/#l'
		self.headers = {
			'Host': 'k.tanjiaoyi.com',
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0',
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
			'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
			# Accept-Encoding: gzip, deflate
			'Cookie': 'JSESSIONID=-8gvvuKfV8ZtHuPxbZXMYV5J.undefined',
			'Connection': 'keep-alive',
			'If-Modified-Since': 'Thu, 07 Jul 2016 04:12:40 GMT',
			'If-None-Match': "aac75acd5d8d11:0",
			'Cache-Control': 'max-age=0'
			}

	def get_data(self, page):
		data_url = 'http://k.tanjiaoyi.com:8080/KDataController/datumlist4Embed.do?jsoncallback=jQuery1112005652110036604996_1469397332598&lcnK=7b56aba5e6e2b29d01587bf76dd3aa95&page='+str(page)+'&rows=20&_=1469397332602'
		data = rq.get(data_url, headers = self.headers).content.decode('utf-8')[43:][:-8]
		js_data = json.loads(data)
		rows = js_data["rows"]
		nrows = []
		for row in rows:
			nrow = {}
			nrow['subTypeName'] = row['subTypeName']
			nrow['dealnum'] = row['dealnum']
			nrow['close'] = row['close']
			nrow['open'] = row['open']
			nrow['low'] = row['low']
			nrow['average'] = row['average']
			nrow['dealamount'] = row['dealamount']
			nrow['indate'] = row['indate']
			nrow['high'] = row['high']
			nrow['deal'] = row['deal']
			nrows.append(row)
		# print(rows)
		self.datalist.extend(nrows)

	def run(self):
		self.datalist = []
		col = ['subTypeName', 'dealnum', 'close', 'open', 'low', 'average', 'dealamount', 'indate', 'high', 'deal']
		for i in range(1, 330):
			print(i)
			self.get_data(i)
		print
		data = pd.DataFrame(self.datalist, columns=col)
		data.to_csv('E:\\Desktop\\carbon_trading_data.csv')



if __name__ == '__main__':
	a = carbon_spyder()
	a.run()