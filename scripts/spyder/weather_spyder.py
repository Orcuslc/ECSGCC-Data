import requests as rq
from bs4 import BeautifulSoup as bs
import os, sys, io

if os.name == 'nt': # Check if the system is Windows-NT
	sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8') # Change the standard output codec to UTF-8


class weather_spyder:
	def __init__(self):
		self.url = 'http://tianqi.com'
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
		url = self.url[:7]+city+'.'+self.url[7:]+'/'+time+'.html'
		page = rq.get(url, headers=self.headers)
		self.soup = bs(page.text, "lxml")
		# print(self.soup.prettify())
		tag = self.soup.div
		while True:
			try:
				# print(tag)
				a = tag["class"]
				# print(a[0])
				if a[0] == 'tqshow':
					print(tag.getText())
					break
				else:
					tag = tag.findNext()
			except BaseException:
				tag = tag.findNext()

		# print(self.soup.prettify())



	def run(self):
		city = 'shanghai'
		time = '20160601'
		self.get_data(city, time)

if __name__ == '__main__':
	a = weather_spyder()
	a.run()


