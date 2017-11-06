#########################################################
##Preparation
options(stringsAsFactors = FALSE)
library(e1071)
#library(wavelets)
library(zoo)
normalize <- function(x,min,max) {
  x <- sweep(x, 2, min)
  sweep(x, 2, max-min, "/")
}
denormalize <- function(x, min, max) {
  x * (max - min) + min
}
wh = read.csv("data/hourly_temp.csv", header = T)

wh$POSIXtime = as.POSIXlt(paste(wh$date, ":00:00", sep = ""), tz = "GMT")
#time axis for plotting
idxy = vector("list", 6)
idxh = vector("list", 24)
for (i in 1:6) {
  idxy[[i]] = wh$POSIXtime$year == 110 + i
}

for (i in 1:24) {
  idxh[[i]] = wh$POSIXtime$hour == i - 1
}
#build "data" formulated as: data$year$hour$[PISIXtime,max_load,degree,hol,weekday] e.g. data$`2011`$`0`$[]
#separate by 24 hour per day
data = vector("list", 6)
for (i in 1:6) {
  data[[i]] = vector("list", 24)
}
names(data) = c("2011", "2012", "2013", "2014", "2015", "2016")
temp = c("POSIXtime", "max_load", "degree", "hol")
for (i in 1:6) {
  names(data[[i]]) = as.character(0:23)
  for (j in 1:24) {
    data[[i]][[j]] = wh[idxy[[i]] & idxh[[j]], temp]
    data[[i]][[j]]$weekday = factor(
      weekdays(data[[i]][[j]]$POSIXtime),
      levels = c("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
    )
    data[[i]][[j]]$hol = data[[i]][[j]]$hol == "小长假"
    data[[i]][[j]]$weekend = unclass(data[[i]][[j]]$weekday) >= 6
    data[[i]][[j]]$sat = unclass(data[[i]][[j]]$weekday) == 6
    data[[i]][[j]]$sun = unclass(data[[i]][[j]]$weekday) == 7
    data[[i]][[j]]$mon = unclass(data[[i]][[j]]$weekday) == 1
  }
}
#########################################################
#template load data from 2011 to 2015 in each of the 24 groups
#very large plot, output as pic before viewing
# j = 1# can be 1 to 24 for 0:00:00 to 23:00:00
# par(mfrow = c(5, 1))
# for (i in 1:5) {
#   plot(
#     data[[i]][[j]]$POSIXtime,
#     data[[i]][[j]]$max_load,
#     type = "l",
#     xlab = "time",
#     ylab = as.character(i)
#   )
# }

#########################################################
#initialize 24 svm models
training = vector("list", 24)
training_n = vector("list", 24)
result_training = vector("list", 24)
result_test = vector("list", 24)
model = vector("list", 24)
test = vector("list", 24)
##test_n = vector("list", 24)
min = vector("list", 24)
max = vector("list", 24)

for(i in 1:24){
  #divide data by hour
  temp = rbind(data$`2011`[[i]],data$`2012`[[i]],data$`2013`[[i]],data$`2014`[[i]])
  n = length(temp$max_load)
  training[[i]] = data.frame(l1 = temp$max_load[8:n],
                             l0 = temp$max_load[7:(n - 1)],
                             l_6 = temp$max_load[1:(n - 7)],
                             t = temp$degree[8:n],
                             sat = temp$sat[8:n],
                             sun = temp$sun[8:n],
                             mon = temp$mon[8:n])
}

