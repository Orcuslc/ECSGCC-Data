setwd("~/Desktop/国家电网/UTF8")
ld = read.csv("load.csv",T)
tem = read.csv("temp.csv",T)
usage = read.csv("usage.csv",T)
w = read.csv("weather.csv",T)
f = ld$用电负荷含抽水_MW[which(match(substr(usage$T_ID,1,4),"2011") == 1 & match(usage$峰腰谷总,"F") == 1)]
y = ld$用电负荷含抽水_MW[which(match(substr(usage$T_ID,1,4),"2011") == 1 & match(usage$峰腰谷总,"Y") == 1)]
g = ld$用电负荷含抽水_MW[which(match(substr(usage$T_ID,1,4),"2011") == 1 & match(usage$峰腰谷总,"G") == 1)]
z = ld$用电负荷含抽水_MW[which(match(substr(usage$T_ID,1,4),"2011") == 1 & match(usage$峰腰谷总,"Z") == 1)]
date = substring(usage$T_ID[which(match(substr(usage$T_ID,1,4),"2011") == 1 & match(usage$峰腰谷总,"Z") == 1)],6)
a=which(match(substring(tem$T_ID,1,4),"2011") == 1)
b=grep("*8:",tem$T_ID)
c=intersect(a,b)
temprature = tem$温度[c]
pattern = "[[:num:]]-[[:num:]][[:space:]]"
m = regexpr(pattern,tem$T_ID[c])
regmatches(tem$T_ID[c],m)
temprature_date = 
usg2011 = data.frame(date,f,y,g,z)