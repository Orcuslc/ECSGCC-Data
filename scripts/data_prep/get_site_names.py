import os, sys

site_path = '../../Site-Data/secinfo_cleaned.txt'
site_set_path = '../../Site-Data/site_set.txt'
with open(site_path) as f:
	lines = f.read().split('\n')

# print(len(lines))
#print(lines[-1])
time_list = []
site_list = []
#count = 0
for line in lines:
	line = line.split('|')
	time_list.append(line[0])
	site_list.extend(line[1:])
	#for i in line[1:]:
		#if len(i) == 1:
			#print(count, line)
	#count+=1
	#print(time_list)
	#break
#site_list.extend(line[1:])
print(len(site_list))
site_set = set(site_list)
#print(len(site_set))
#nsite_list = []
#for item in site_list:1
#	if item not in nsite_list:
#		nsite_list.append(item)
#print(len(nsite_list))
#print(site_set)
with open(site_set_path, 'w') as f:
	for item in site_set:
		f.write(item+'\n')