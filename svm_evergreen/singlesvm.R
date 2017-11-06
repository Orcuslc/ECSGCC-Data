options(stringsAsFactors = FALSE)
#setwd("~/Desktop/ECGC/R_workspace")
library(e1071)
library(zoo)
lagday=function(x,m,l=0){
  n=length(x)
  x[(m-l+1):(n-l)]
}

singlesvm=function(load,time0=time(load),holiday,t, epsilon = 0.001,#
                   gamma = .5 / 7 ^ 2,#
                   cost = 27#
){
  # if(class(time)!="POSIXlt"
  #    time=as.POSIXlt(time)
  # t0 = 16;t = abs(t-t0)
  load=coredata(load)
  wholedata=as.zoo(
    cbind.data.frame(l1=lagday(load,7),
                     l0=lagday(load,7,1),
                     l_1=lagday(load,7,2),
                     l_6=lagday(load,7,7),
                     t=lagday(t,7),
                     holiday=lagday(holiday,7)),
    lagday(time0,7)
  )
  data=list();model=list()
  n=dim(wholedata)[1]
  for(i in 1:7){
    data[[i]]=wholedata[seq(i,n,7),]
    model[[i]] = svm(l1~.,
        data = data[[i]]
        , epsilon = epsilon,
        gamma = gamma,#
        cost = cost#
        )
  }
  list(model= model,data=data,wholedata=wholedata)
}

singlepredict=function(SVM,load,time0=time(load),holiday,t){
  t0 = 16#
  #t = abs(t-t0)
  wholedata=as.zoo(
    cbind.data.frame(l1=lagday(load,7),
                     l0=lagday(load,7,1),
                     l_1=lagday(load,7,2),
                     l_6=lagday(load,7,7),
                     t=lagday(t,7),
                     holiday=lagday(holiday,7)),
    lagday(time0,7)
    )
  data=list();PREDICT=list()
  n=dim(wholedata)[1]
  for(i in 1:7){
    data[[i]]=wholedata[seq(i,n,7),]
    timei=time(data[[i]])
    PREDICT[[i]] = zoo(predict(SVM$model[[i]],data[[i]]),timei)
  }
  return(list(PREDICT=PREDICT,WHOLEPREDICT=do.call(c,PREDICT),data=data,wholedata=wholedata))
}

load("load_usage.RData")
# load_usage$holiday=as.numeric(load_usage$holiday=="TRUE")
# load_usage=cbind(lapply(load_usage,as.numeric))
# load_usage = zoo(load_usage,time)
# save(load_usage,file = "load_usage.RData")

#param search

par(mfrow=c(1,1))
testidx=1100:1456 #2014
testidx=1100:1456 #2015
trainidx=setdiff(1:2032,testidx)
data=load_usage$load #
Eij=matrix(0,10,10)
for(k in 10){
for(j in 10:20){
  for(i in 7){
SVM=singlesvm(load=data[trainidx],time0=time(load_usage$F[trainidx]),holiday = load_usage$holiday[trainidx],t=load_usage$temprature[trainidx],
              epsilon = 0.0001*k,gamma = .5/i^2,cost = j)
PREDICT=singlepredict(SVM,data[testidx],time0=time(load_usage$F[testidx]),holiday = load_usage$holiday[testidx],t=load_usage$temprature[testidx])
prediction=PREDICT$WHOLEPREDICT
actual=lagday(data[testidx],7)
error=prediction/actual-1
#plot(error)
#Eij[i,j] = mean(abs(error))
print(paste(mean(abs(error)),i,j))
#plot(prediction,col=2)
#lines(actual,col=3)
}}}

#5fold
par(mfrow=c(5,1))
for(i in 0:4){
  testidx=58*7*i+1:406
  trainidx=setdiff(1:2030,testidx)
SVM=singlesvm(load=load_usage$F[trainidx],time0=time(load_usage$F[trainidx]),holiday = load_usage$holiday[trainidx],t=load_usage$temprature[trainidx])
PREDICT=singlepredict(SVM,load_usage$F[testidx],time0=time(load_usage$F[testidx]),holiday = load_usage$holiday[testidx],t=load_usage$temprature[testidx])
prediction=PREDICT$WHOLEPREDICT
actual=lagday(load_usage$F[testidx],7)
error=prediction/actual-1
#plot(error)
print(paste('mean',mean(abs(error)),"max",max(abs(error))))

 plot(prediction,col=2,xlab = 'time')
 lines(actual,col=3)
}
par(mfrow=c(1,1))

#long-term forecasting
data=load_usage$F
trainidx=(1:1015)
SVM=singlesvm(load=load_usage$F[trainidx],time0=time(load_usage$F[trainidx]),holiday = load_usage$holiday[trainidx],t=load_usage$temprature[trainidx])
predictdata=coredata(data[trainidx])
for(length in 1015:2029){
  temp=cbind.data.frame(l0=predictdata[length],
                     l_1=predictdata[length-1],
                     l_6=predictdata[length-6],
                     t=load_usage$t[length+1],
                     holiday=load_usage$holiday[length+1])
  predictdata[length+1]=predict(SVM$model[[length%%7+1]],temp)
}
predictdata=zoo(predictdata,time(data))

plot(data,col=2,xlab = 'time') 
lines(predictdata,col=3)
err=(abs(data-predictdata)/data)[1016:2030]
mean(err)


#2-day
data=load_usage$F
data=data[1:(length(data)-2)]
TIME=time(data)
data=coredata(data)
n=length(data)
trainidx=(1:1015)
SVM=singlesvm(load=load_usage$F[trainidx],
              time0=time(load_usage$F[trainidx]),
              holiday = load_usage$holiday[trainidx],
              t=load_usage$temprature[trainidx])
predictdata=rep(0,n)
predictdata[trainidx]=data[trainidx]
for(i in 0:508){
  for(k in 0:1){
  t=i*2+k+1015
  temp=cbind.data.frame(l0=ifelse(k==0,data[t],predictdata[t]),
                        l_1=ifelse(k==0|k==1,data[t],predictdata[t-1]),
                        l_6=data[t-6],
                        t=load_usage$t[t+1],
                        holiday=load_usage$holiday[t+1])
  predictdata[t+1]=predict(SVM$model[[(t-1)%%7+1]],temp)
  }
#  predictdata[t+1]=20000
}
data=data[1:2030]
data=zoo(data,TIME)
predictdata=zoo(predictdata,TIME)
plot(data,col=2)
lines(predictdata,col=3)
testidx=1016:2030
err=abs((predictdata-data)/data)[testidx]

summary(coredata(err))
idx=!(load_usage$holiday)[testidx]
summary(coredata(err)[idx])

#7-day
data=load_usage$F
data=data[1:(length(data)-2)]
TIME=time(data)
data=coredata(data)
n=length(data)
trainidx=(1:1015)
SVM=singlesvm(load=load_usage$F[trainidx],
              time0=time(load_usage$F[trainidx]),
              holiday = load_usage$holiday[trainidx],
              t=load_usage$temprature[trainidx])
predictdata=rep(0,n)
predictdata[trainidx]=data[trainidx]
for(i in 0:145){
  for(k in 0:7){
    t=i*7+k+1015
    temp=cbind.data.frame(l0=ifelse(k==0,data[t],predictdata[t]),
                          l_1=ifelse(k==0|k==1,data[t],predictdata[t-1]),
                          l_6=data[t-6],
                          t=load_usage$t[t+1],
                          holiday=load_usage$holiday[t+1])
    predictdata[t+1]=predict(SVM$model[[(t-1)%%7+1]],temp)
  }
  #  predictdata[t+1]=20000
}
data=zoo(data,TIME)
predictdata=zoo(predictdata,TIME)
plot(data,col=2)
lines(predictdata,col=3)
err=abs((predictdata-data)/data)
testidx=1015:2030
err=err[testidx]

summary(coredata(err))
idx=!(load_usage$holiday)[testidx]
summary(coredata(err)[idx])