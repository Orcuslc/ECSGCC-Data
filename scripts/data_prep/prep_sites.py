import pandas as pd
import codecs
import sys



# print(len(set(nf_index)))

def clean_data(data):
	index = data.index.tolist()
	def _handle(item):
		if len(item) <= 10:
			item = item + ' 00:00:00'
		plist = item.split(' ')
		date = plist[0].split('/')
		time = plist[1].split(':')
		if len(date[2]) == 1:
			date[2] = '0'+date[2]
		if len(date[1]) == 1:
			date[1] = '0'+date[1]
		if len(time[1]) == 1:
			time[1] = '0'+time[1]
		if len(time[0]) == 1:
			time[0] = '0'+time[0]
		return date[0]+'/'+date[1]+'/'+date[2]+' '+time[0]+':'+time[1]+':'+time[2]
	index = list(map(_handle, index))
	data.index = pd.Series(index, name = 'T_ID')
	data.to_csv('../../Site-Data/secinfo.csv')

def get_instinct_index(nf_index):
	index_list = [nf_index[0]]
	for i in range(1, len(nf_index)):
		if nf_index[i-1] != nf_index[i]:
			index_list.append(nf_index[i])
	return index_list


def add_content(index_list):
	#df = pd.DataFrame(index = index_list)
	content_list = []
	count = 0
	for index in index_list:
		count += 1
		try:
			content = nf.loc[index]['NAME'].tolist()
			content = '|'.join(content)
		except AttributeError:
			content = nf.loc[index]['NAME']
			#print(content)
		content_list.append(content)
		#print(count)
		#s = pd.Series(content_list, name = index).to_csv('/media/Library/Chuan/Documents/GitHub/ECSGCC-data/secinfo_cleaned.csv', mode = 'w+')
	#df = dict(zip(index_list, content_list))
	#df = pd.DataFrame(df, index = index_list)
	#df.to_csv('/media/Library/Chuan/Documents/GitHub/ECSGCC-data/secinfo_cleaned.csv', chunk_size = 1000)
	with open('../../Site-Data/secinfo_cleaned.txt', 'w') as f:
		for i in range(len(index_list)):
			f.write(index_list[i]+'|'+content_list[i]+'\n')
	f.close()

if __name__ == '__main__':
	# path = '../../Site-Data/secinfo.csv'
	# nf = pd.read_csv(path, index_col = 'T_ID', encoding='gbk').sort_index()
	# clean_data(nf)
	nf = pd.read_csv(path, index_col = 'T_ID', encoding='gbk').sort_index()
	nf_index = nf.index.tolist()
	print(len(nf_index))
	index_list = get_instinct_index(nf_index)
	add_content(index_list)