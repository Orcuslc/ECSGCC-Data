#########################################################
#produce data
source("lsvm_preparation.R") 
#note: names(data$`2011`$`0`)= "POSIXtime" "max_load" "degree" "hol" "weekday" "weekend" "sat" "sun" "mon"



message("Print the average l1 loss of the model (24 hours respectively):")
for (i in 1:24) {
  #train
  ##min[[i]] = min(training[[i]]$l1)
  ##max[[i]] = max(training[[i]]$l1)
  ##training_n[[i]] = normalize(training[[i]],min[[i]],max[[i]])
  model[[i]] = svm(
    l1 ~ . ,
    ##data = training_n[[i]],
    data = training[[i]],
    epsilon = 0.001,
    gamma = .5 / 7 ^ 2,
    cost = 10
  )
  ##result_training[[i]] = denormalize(predict(model[[i]], training_n[[i]][-1]), min[[i]], max[[i]])
  result_training[[i]] = predict(model[[i]], training[[i]][-1])
  #print(sum(abs(result_training[[i]] / training[[i]]$l1 - 1)) / length(result_test[[i]]))
  
  #test
  temp = data$`2015`[[i]]
  n = length(temp$max_load)
  idxr = temp$POSIXtime[8:n]
  test[[i]] = data.frame(l1 = temp$max_load[8:n],
                         l0 = temp$max_load[7:(n - 1)],
                         l_6 = temp$max_load[1:(n - 7)],
                         t = temp$degree[8:n],
                         sat = temp$sat[8:n],
                         sun = temp$sun[8:n],
                         mon = temp$mon[8:n])
  ##test_n[[i]] = normalize(test[[i]],min[[i]],max[[i]])
  ##result_test[[i]] = denormalize(predict(model[[i]], test_n[[i]][-1]), min[[i]], max[[i]])
  result_test[[i]] = predict(model[[i]], test[[i]][-1])
  
  print(sum(abs(result_test[[i]] / test[[i]]$l1 - 1)) / length(result_test[[i]]))
}


#combine hourly tests
result_t = c(do.call(rbind, lapply(1:24, function(x) {
  result_test[[x]]
})))
test_t = c(do.call(rbind, lapply(1:24, function(x) {
  test[[x]]$l1
})))
idxt = c(do.call(rbind, lapply(1:24, function(x) {
  as.character(as.POSIXct(data$`2015`[[x]]$POSIXtime[8:365]))
})))

idx = -grep(":",idxt)
idxt[idx] = paste(idxt[idx],"00:00:00",sep = " ")
idxt = as.POSIXct(idxt,tz="GMT")

result_t = zoo(result_t,idxt)
test_t = zoo(test_t,idxt)
par(mfrow = c(1,1))
idx = 1:500
plot(result_t[idx], type = "l", lty = 2)
lines(test_t[idx], lty = 1)
sum(abs(result_t / test_t - 1)) / length(result_t)#result
n = length(test_t);sum(abs(test_t[-(1:24)] / test_t[-((n-23):n)] - 1)) / length(result_t-24)#blind forecasting: 0.05635233
err_t = result_t/test_t-1#residue error
