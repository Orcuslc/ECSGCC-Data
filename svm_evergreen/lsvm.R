#########################################################
##dependencies
options(stringsAsFactors = FALSE)
library(e1071)
#library(wavelets)
normalize <- function(x, min, max) {
  x <- sweep(x, 2, min)
  sweep(x, 2, max - min, "/")
}
denormalize <- function(x, min, max) {
  x * (max - min) + min
}

#########################################################
lsvm <- function(time, load, t, hol) {
  POSIXtime = as.POSIXlt(time)
  #initialize 24 svm models
  data = vector("list", 24)
  names(data) = paste(as.character(0:23), ":00:00", sep = "")
  total = cbind.data.frame(POSIXtime, load, t, hol)
  idxh = vector("list", 24)
  training = vector("list", 24)
  ##training_n = vector("list", 24)
  #result_training = vector("list", 24)
  model = vector("list", 24)
  for (j in 1:24) {
    idxh[[j]] = POSIXtime$hour == j - 1
    data[[j]] = total[idxh[[j]],]
    data[[j]]$weekday = factor(
      weekdays(data[[j]]$POSIXtime),
      levels = c(
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
      )
    )
    #data[[j]]$weekend = unclass(data[[j]]$weekday) >= 6
    data[[j]]$sat = unclass(data[[j]]$weekday) == 6
    data[[j]]$sun = unclass(data[[j]]$weekday) == 7
    data[[j]]$mon = unclass(data[[j]]$weekday) == 1
    #divide data by hour
    temp = data[[j]]
    n = length(temp$load)
    training[[j]] = data.frame(
      l1 = temp$load[8:n],
      l0 = temp$load[7:(n - 1)],
      l_6 = temp$load[1:(n - 7)],
      t = temp$t[8:n],
      sat = temp$sat[8:n],
      sun = temp$sun[8:n],
      mon = temp$mon[8:n],
      hol = temp$hol[8:n]
    )
    #train
    ##min[[j]] = apply(training[[j]], 2, min)
    ##max[[j]] = apply(training[[j]], 2, max)
    ##training_n[[j]] = normalize(training[[j]], min[[j]], max[[j]])
    model[[j]] = svm(
      l1 ~ . ,
      ##data = training_n[[j]],
      data = training[[j]],
      epsilon = 0.001,
      gamma = .5 / 7 ^ 2,
      cost = 10
    )
    #result_training[[j]] = denormalize(predict(model[[j]], training_n[[j]][-1]), min, max)
    #print(sum(abs(result_training[[j]] / training[[j]]$l1 - 1)) / length(result_test[[j]]))
  }
  return(
    list(
      data = data,
      training = training,
      ##training_n = training_n,
      model = model
      ##min = min,
      ##max = max
    )
  )
}
#############################################
lpredict <- function(LSVM, time, load, t, hol, actual = NULL) {
  ##input time,load(24), t(1) ,'actual(24)' is optional, used for comparing the prediction
  POSIXtime = as.POSIXlt(time)
  #diff = as.difftime(-1,units = "days")
  n = length(load)
  l0 = load[n + (-23:0)]
  l_6 = load[n - 24 * 6 + (-23:0)]
  w = factor(
    weekdays(POSIXtime),
    levels = c(
      "Monday",
      "Tuesday",
      "Wednesday",
      "Thursday",
      "Friday",
      "Saturday",
      "Sunday"
    )
  )
  test = vector("list", 24)
  ##test_n = vector("list", 24)
  result_test = c()
  for (j in 1:24) {
    test[[j]] = data.frame(
      l0 = l0[j],
      l_6 = l_6[j],
      t = t,
      sat = w == 6,
      sun = w == 7,
      mon = w == 1,
      hol = hol
    )
    
    ##test_n[[j]] = normalize(test[[j]], LSVM$min[[j]], LSVM$max[[j]])
    ##result_test[j] = denormalize(predict(LSVM$model[[j]], test_n[[j]]), LSVM$min[[j]], LSVM$max[[j]])
    result_test[j] = predict(LSVM$model[[j]], test[[j]])
  }
  plot(
    result_test,
    type = "l",
    lty = 2,
    xlab = paste("date:", time),
    ylab = "load / MW"
  )
  if (!is.null(actual)) {
    lines(actual)
    message(paste("average error:", mean(abs(result_test / actual - 1))))
  }
  return(result_test)
}


###########################
##if you don't want to run the code, just load the "LSVM" object from trained.RData
#load("data/trained.RData")



##otherwise,load form the previous file
temp = wh[wh$POSIXtime$year <= 114,]
POSIXtime.train = temp$POSIXtime
load.train = temp$max_load
t.train = temp$degree
hol.train = temp$hol == "小长假"
write.csv(data.frame(POSIXtime.train,load.train,t.train,hol.train),"train.csv")
MODEL = lsvm(POSIXtime.train,load.train,t.train,hol.train)

temp = wh[wh$POSIXtime$year == 115,]
n = length(temp$POSIXtime)
POSIXtime.test = temp$POSIXtime[1:(n-7)]
load.test = temp$max_load[1:(n-7)]
t.test = temp$degree[8:n]
hol.test = (temp$hol == "小长假")[8:n]
write.csv(data.frame(POSIXtime.test,load.test,t.test,hol.test),"test.csv")
load.test_actural = temp$max_load[8:n]
lpredict(MODEL,POSIXtime.test,load.test,t.test,hol.test,actual = load.test_actural)

lpredict(MODEL,POSIXtime.train,load.train,t.train,hol.train)
  