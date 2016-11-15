import os, sys

site_set_path = '../../Data/Site-Data/site_set.txt'
secinfo_path = '../../Data/Site-Data/secinfo_cleaned.txt'
matrix_path = '../../Data/Site-Data/matrix.txt'

with open(site_set_path) as f:
	site_set = f.read().split('\n')
f.close()
time_list = []
site_list = []
with open(secinfo_path) as f:
	secinfo = f.read().split('\n')
	for record in secinfo:
		record = record.split('|')
		time_list.append(record[0])
		site_list.append(record[1:])
f.close()
print(time_list[-1])
matrix = [['0' if i not in site_list[j] else '1' for i in site_set] for j in range(len(time_list))]

with open(matrix_path, 'w') as f:
	f.write('time'+'|'+'|'.join(site_set)+'\n')
	for i in range(len(time_list)):
		f.write(time_list[i]+','+','.join(matrix[i])+'\n')
f.close()