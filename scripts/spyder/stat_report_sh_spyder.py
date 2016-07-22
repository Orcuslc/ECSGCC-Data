import requests as rq
import html.parser as hp
import io
import sys
import os
import lxml
from bs4 import BeautifulSoup as bs
import pandas as pd

if os.name == 'nt': # Check if the system is Windows-NT
	sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8') # Change the standard output codec to UTF-8

class stat_downloader:
	def __init__(self):
		self.headers = {
				'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
				'Referer': 'http://www.stats-sh.gov.cn/tjnj/nj15.htm?d1=2015tjnj/C0101.htm',
				'Accept-Language':'zh-Hans-CN,zh-Hans;q=0.8,en-US;q=0.5,en;q=0.3',
				'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393',
				# 'Accept-Encoding': gzip, deflate
				'Host': 'www.stats-sh.gov.cn',
				'Connection': 'Keep-Alive',
				'Cookie': 'JSESSIONID=369BCFE97476A350D024B9F4BB8FAC2A; _gscu_721522134=691545152pvr8s12; _gscs_721522134=691545157gwllk12|pv:1; _gscbrs_721522134=1'
					}
		self.query_url = "http://218.242.177.36/zwzy/yearbook/toQueryYearlyReports.do"
		self.url = "http://218.242.177.36/zwzy/yearbook/toDownloadReportFile.do"
		self.years = [2014, 2013, 2012]

	def post(self, year, index):
		# post_data = 'pageSize=10&qtype=t&pageNo='+str(index)+'&year='+str(year)+'&reportName=.&indexKeyWords=&specIdx=ALL'
		post_data = {
			"dfyear":str(year),
			"dftabnum":str(index)
		}
		r = rq.post(self.url, data = post_data)
		return r

	def iter(self):
		for year in self.years:
			for i in range(25):
				if i <= 9:
					i = '0' + str(i)
				else:
					i = str(i)
				for j in range(40):
					if j <= 9:
						j = '0' + str(j)
					else:
						j = str(j)
					index = 'C'+i+j
					try:
						r = self.post(year, index)
						if r.status_code == 200:
							with open('E:\\Desktop\\stat\\'+str(year)+'\\'+str(index)+'.csv', 'wb') as f:
								f.write(r.content)
						else:
							continue
					except BaseException:
						continue

a = stat_downloader()
a.iter()



class stat_spyder:
	def __init__(self):
		self.url = "http://www.stats-sh.gov.cn/tjnj"
# url = "http://www.stats-sh.gov.cn/tjnj/2015tjnj/C01/C0107A.htm"
		self.headers = {
				'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
				'Referer': 'http://www.stats-sh.gov.cn/tjnj/nj15.htm?d1=2015tjnj/C0101.htm',
				'Accept-Language':'zh-Hans-CN,zh-Hans;q=0.8,en-US;q=0.5,en;q=0.3',
				'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393',
				# 'Accept-Encoding': gzip, deflate
				'Host': 'www.stats-sh.gov.cn',
				'Connection': 'Keep-Alive',
				'Cookie': 'JSESSIONID=369BCFE97476A350D024B9F4BB8FAC2A; _gscu_721522134=691545152pvr8s12; _gscs_721522134=691545157gwllk12|pv:1; _gscbrs_721522134=1'
					}
		self.year = [2015, 2014, 2013, 2012]
# file = rq.get(url, headers=headers).content.decode('gbk')
# soup = bs(open('E:\\Desktop\\C0101.htm'), "lxml")	
	def get_html(self, year, ):
		html_list = []


	def handle_html(self, html):
		result_list = []
		soup = bs(html, "lxml")
		body = soup.body
		tag = body.tr
		while True:
			try:
				res = tag.getText().split('\n')
				tag = tag.findNextSibling()
				result_list.append(res)
			except AttributeError:
				break
		return result_lis

		
