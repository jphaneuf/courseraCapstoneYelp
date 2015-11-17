library(caret)
this.dir <- dirname(parent.frame(2)$ofile)
setwd(this.dir)
biz <- read.csv('bizcats.csv')
#for city: count total businesses
#for each category in a city: what percentage of business share
# does it account for?  i.e.

#category,city,total businesses in city, nCategory,nCategory/totalbiz,mean(category)
#thai,nyc,1000,50,0.05,3
#merge city and state into column to determine unique

biz$cityState <- paste0(biz$city,rep(';',nrow(biz)),biz$state)
biz$catCityState <- paste0(biz$category,rep(';',nrow(biz)),biz$cityState)
businessTotalsInCity <- table(biz$cityState)
catTotalsInCity <- table(biz$catCityState)
uniqueCities <- names(businessTotalsInCity)

population <- read.csv('SUB-EST2014_ALL.csv')
#All cities have city/town suffix, remove please
population$NAME <- sapply(population$NAME,function(x) sub(' town','',x))
population$NAME <- sapply(population$NAME,function(x) sub(' city','',x))

#population$cityState <- paste0(population$NAME,rep(';',nrow(population)),population$STNAME)
stab <- read.csv('stateAbbreviations.csv',header=TRUE) 
#stab$abbreviation[stab$state=='Alabama']
abbreviateState <- function(state){
  state <- as.character(state)
  if(state %in% stab$state){
    index<-which(stab$state==state)
    return(as.character(stab$abbreviation[index]))
  }else{
    return(NA)
  }
}

population$cityState <- paste0(population$NAME,rep(';',nrow(population)),
                    sapply(population$STNAME,abbreviateState))
population <- population[!duplicated(population$cityState),]
getPopulation <- function(cityState){
  cityState <- as.character(cityState)
  if(cityState %in% population$cityState){
    index<-which(population$cityState==cityState)
    print(index)
    return(as.character(population$POPESTIMATE2014[index]))
  }else{
    return(NA)
  }
} 


xdf <- data.frame()
for(i in 1:nrow(biz)){
  newLine= biz[i,c('category','city','state','cityState','catCityState')]
  #total businesses in city
  newLine$nBusinesses <- businessTotalsInCity[newLine$cityState]
  #number of category in a city
  newLine$nCategories <- catTotalsInCity[newLine$catCityState]
  #compute nCategoryInCity/totalbiz
  newLine$categoryRatio <- newLine$nCategories/newLine$nBusinesses
  #compute mean stars for city
  newLine$meanStars <- mean(subset(biz,catCityState == newLine$catCityState)[,'stars'])
  xdf <- rbind(xdf,newLine)
}
xdf <-read.csv('xdf.csv')
}
ndxdf <- xdf[!duplicated(xdf),]#remove duplicates

ndxdfp <- read.csv('ndxdfp.csv')
ndxdfp <- ndxdfp[!duplicated(ndxdfp),]#remove duplicates
ndxdfp <- subset(ndxdfp,!is.na(population))
inTraining <- createDataPartition(y=1:nrow(ndxdfp),p=0.6,list=FALSE)
inTesting <- (1:nrow(ndxdfp))[-inTraining]
t1 <- inTraining[1:6000]
t2 <- inTraining[-t1]
rfModel <- train(meanStars ~ categoryRatio+population, data=ndxdfp[t1,],method='gbm')
predicted <- predict(rfModel,ndxdfp[t2,])
print(predict(rfModel,ndxdfp[t2,]))
plot(ndxdfp[t2,]$meanStars,predicted)
confusionMatrix(ndxdfp[t2,]$meanStars,predicted)
names(getModelInfo())
#businessTotalsInCity[uniqueCities[100]] #using cityState, grab business totals

#how many thai restaurants in New York?
