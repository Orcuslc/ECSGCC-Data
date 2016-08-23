import pandas as pd

nf = pd.read_csv('/media/Library/Desktop/ECSGCC/data/secinfo.csv', index_col = 'T_ID', encoding='gbk').sort_index()
nf_index = nf.index.tolist()

def get_instinct_index():
	index_list = [nf_index[0]]
	for i in range(len(nf_index)-1):
		if nf_index[i] != nf_index[i+1]:
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
			content = ' '.join(content)
		except AttributeError:
			content = nf.loc[index]['NAME']
		content_list.append(content)
		print(count)
		#s = pd.Series(content_list, name = index).to_csv('/media/Library/Chuan/Documents/GitHub/ECSGCC-data/secinfo_cleaned.csv', mode = 'w+')
	#df = dict(zip(index_list, content_list))
	#df = pd.DataFrame(df, index = index_list)
	#df.to_csv('/media/Library/Chuan/Documents/GitHub/ECSGCC-data/secinfo_cleaned.csv', chunk_size = 1000)
	with open('/media/Library/Chuan/Documents/GitHub/ECSGCC-data/secinfo_cleaned.csv', 'w') as f:
		for i in range(len(index_list)):
			f.write(index_list[i]+','+content_list[i]+'\n')
	f.close()

if __name__ == '__main__':
	index_list = get_instinct_index()
	print(len(index_list))
	add_content(index_list)