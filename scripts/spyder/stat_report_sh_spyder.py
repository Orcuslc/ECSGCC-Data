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

url = "http://www.stats-sh.gov.cn/tjnj/2015tjnj/C01/C0107A.htm"
headers = {
	'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
	'Referer': 'http://www.stats-sh.gov.cn/tjnj/nj15.htm?d1=2015tjnj/C0101.htm',
	'Accept-Language':'zh-Hans-CN,zh-Hans;q=0.8,en-US;q=0.5,en;q=0.3',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393',
	# 'Accept-Encoding': gzip, deflate
	'Host': 'www.stats-sh.gov.cn',
	'Connection': 'Keep-Alive',
	'Cookie': 'JSESSIONID=369BCFE97476A350D024B9F4BB8FAC2A; _gscu_721522134=691545152pvr8s12; _gscs_721522134=691545157gwllk12|pv:1; _gscbrs_721522134=1'
}

p = hp.HTMLParser()
file = rq.get(url, headers=headers).content.decode('gbk')
soup = bs(open('E:\\Desktop\\C0101.htm'), "lxml")


def handle_html(html):
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
		
print(handle_html(file))