setwd("~/Desktop/国家电网/UTF8")
ld = read.csv("load.csv",T)
tem = read.csv("temp.csv",T)
usage = read.csv("usage.csv",T)
w = read.csv("weather.csv",T)
usg2011 = ld$用电负荷含抽水_MW[which(match(substr(ld$T_ID,1,4),"2009") == 1)]
