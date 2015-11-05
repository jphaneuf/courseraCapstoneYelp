setwd('/Users/jphaneuf/joeWorksspace/courseraCapstoneYelp')
dataSetURL <- "https://d396qusza40orc.cloudfront.net/dsscapstone/dataset/yelp_dataset_challenge_academic_dataset.zip"

if (!file.exists('yelp_dataset_challenge_academic_dataset.zip')){
  dataSetZipFileName <- 'yelpDataSet.zip'
  download.file(dataSetURL,dataSetZipFileName,method='curl')
  unzip(dataSetZipFileName)
}
biz <- sapply(readLines("yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_business.json",n=100),fromJSON)
#checkin <- fromJSON(file="yelp_academic_dataset_checkin.json")
#review <- fromJSON(file="yelp_academic_dataset_review.json")
#tip <- fromJSON(file="yelp_academic_dataset_tip.json")
#user <- fromJSON(file="yelp_academic_dataset_user.json")

#q11
#      funny>1   fans>1
#TRUE  29324       51964
#FALSE 337391      314751
funnyfansfisher <-
  matrix(c(29324,337391,51964,314751),
         nrow = 2,
         dimnames = list(Truth = c("TRUE", "FALSE"),
                         thing = c("funnyg1", "fansg1")))
                         