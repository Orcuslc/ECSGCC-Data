#########################################################
##dependencies
options(stringsAsFactors = FALSE)
library(e1071)
library(wavelets)
normalize <- function(x, min, max) {
  x <- sweep(x, 2, min)
  sweep(x, 2, max - min, "/py")
}
denormalize <- function(x, min, max) {
  x * (max - min) + min
}



#########################################################
wtsvm <- function(time, load, t) {
  POSIXtime = as.POSIXlt(time)
  #initialize 24 svm models
  data = vector("list", 24)
  names(data) = paste(as.character(0:23), ":00:00", sep = "")
  total = cbind.data.frame(POSIXtime, load, t)
  idxh = vector("list", 24)
  training0 = vector("list", 24)
  training1 = vector("list", 24)
  training2 = vector("list", 24)
  #result_training = vector("list", 24)
  model0 = vector("list", 24)
  model1 = vector("list", 24)
  model2 = vector("list", 24)
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
  
    #data[[j]]$weekend = unclass(data[[j]]$weekday) >= 6
    data[[j]]$sat = unclass(data[[j]]$weekday) == 6
    data[[j]]$sun = unclass(data[[j]]$weekday) == 7
    data[[j]]$mon = unclass(data[[j]]$weekday) == 1
    #divide data by hour
    n = length(data[[j]]$load)
    temp0 = dwt(as.numeric(data[[j]]$load),filter = "d2",n.levels = 3)
    temp0@V$V1
    training0[[j]] = data.frame(
      l1 = temp0@V$V1[8:n],
      l0 = temp0@V$V1[7:(n - 1)],
      l_6 = temp0@V$V1[1:(n - 7)],
      t = data[[j]]$t[8:n],
      sat = data[[j]]$sat[8:n],
      sun = data[[j]]$sun[8:n],
      mon = data[[j]]$mon[8:n]
    )
    training1[[j]] = data.frame(
      l1 = temp0@W$W1[8:n],
      l0 = temp0@W$W1[7:(n - 1)],
      l_6 = temp0@W$W1[1:(n - 7)],
      t = temp0@W$W1[8:n],
      sat = data[[j]]$sat[8:n],
      sun = data[[j]]$sun[8:n],
      mon = data[[j]]$mon[8:n]
    )
    training2[[j]] = data.frame(
      l1 = temp0@W$W2[8:n],
      l0 = temp0@W$W2[7:(n - 1)],
      l_6 = temp0@W$W2[1:(n - 7)],
      t = temp0@W$W2[8:n],
      sat = data[[j]]$sat[8:n],
      sun = data[[j]]$sun[8:n],
      mon = data[[j]]$mon[8:n]
    )
    #train
    ######################Parameters#########################
    model0[[j]] = svm(
      l1 ~ . ,
      scale = T,
      data = training0[[j]],
      epsilon = 0.001,
      gamma = .5 / 7 ^ 2,
      cost = 10
    )
    model1[[j]] = svm(
      l1 ~ . ,
      scale = T,
      data = training1[[j]],
      epsilon = 0.001,
      gamma = .5 / 7 ^ 2,
      cost = 10
    )
    model2[[j]] = svm(
      l1 ~ . ,
      scale = T,
      data = training2[[j]],
      epsilon = 0.001,
      gamma = .5 / 7 ^ 2,
      cost = 10
    )
    ######################Parameters#########################
    #result_training[[j]] = denormalize(predict(model[[j]], training_n[[j]][-1]), min, max)
    #print(sum(abs(result_training[[j]] / training[[j]]$l1 - 1)) / length(result_test[[j]]))
  }
  return(
    list(
      data = data,
      model0 = model0,
      model1 = model1,
      model2 = model2
    )
  )
}



#############################################
wtpredict <- function(LSVM, time, load, t, actual = NULL) {
  POSIXtime = as.POSIXlt(time)
  #diff = as.difftime(-1,units = "days")
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
  )[1]
  test0 = vector("list", 12)
  test4 = vector("list", 6)
  test1 = vector("list", 12)
  test2 = vector("list", 6)
  #test_n = vector("list", 24)
  
  DWT = dwt(ts(load),filter = "d2",n.levels = 2)
  W0 = DWT@V$V1
  W1 = DWT@W$W1
  W4 = DWT@V$V2
  W2 = DWT@W$W2
  W0 = DWT@V$V1
  W1 = DWT@W$W1
  W4 = DWT@V$V2
  W2 = DWT@W$W2
  n = length(W0)
  W00 = W0[n + (-11:0)]
  W0_6 = W0[n - 12 * 6 + (-11:0)]
  W10 = W1[n + (-11:0)]
  W1_6 = W1[n - 12 * 6 + (-11:0)]
  W40 = W4[n/2 + (-5:0)]
  W4_6 = W4[n/2 - 6 * 6 + (-5:0)]
  W20 = W2[n/2 + (-5:0)]
  W2_6 = W2[n/2 - 6 * 6 + (-5:0)]
  
  sat = w == 6
  sun = w == 7
  mon = w == 1
  for (j in 1:n) {
    test0[[j]] = data.frame(
      l0 = W00[j],
      l_6 = W0_6[j],
      t = t,
      sat = sat,
      sun = sun,
      mon = mon
    )
    test1[[j]] = data.frame(
      l0 = W1[j],
      l_6 = W1[idx_6],
      t = t,
      sat = sat,
      sun = sun,
      mon = mon
    )
    DWT@V$V1[j] = predict(WTSVM$model0[[#########]], test0[[j]])
    DWT@W$W1[j] = predict(WTSVM$model1[[#########]], test1[[j]])
  }
  
  for(j in 1:n/2){
    test4[[j]] = data.frame(
      l0 = W4[idx0],
      l_6 = W4[idx_6],
      t = t,
      sat = sat,
      sun = sun,
      mon = mon
    )
    test2[[j]] = data.frame(
      l0 = W2[idx0],
      l_6 = W2[idx_6],
      t = t,
      sat = sat,
      sun = sun,
      mon = mon
    )
    
    DWT@V$V2[j] = predict(WTSVM$model0[[########]], test4[[j]])
    DWT@W$W2[j] = predict(WTSVM$model2[[########]], test2[[j]])
  }
  
  result_test[j] = idwt(DWT)
  plot(
    result_test,
    type = "l",
    lty = 2,
    ylab = "load / MW"
  )
  if (!is.null(actual)) {
    lines(actual)
    print(paste("average error:", sum(abs(
      result_test / actual - 1
    )) / 24))
  }
  return(result_test)
}

