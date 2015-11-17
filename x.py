# -*- coding: utf-8 -*-
"""
Created on Mon Nov  2 18:41:34 2015

@author: jphaneuf
"""

import json,re
from pprint import pprint
import numpy as np
import pylab as p
import pandas
import random
import operator
populationData = pandas.read_csv('./SUB-EST2014_ALL.csv')

with open('./yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_business.json') as data_file:
    biz = [json.loads(x) for x in data_file]
with open('./yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_checkin.json') as data_file:
    checkin = [json.loads(x) for x in data_file]
with open('./yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_review.json') as data_file:
    review = [json.loads(x) for x in data_file]
with open('./yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_tip.json') as data_file:
    tip = [json.loads(x) for x in data_file]
with open('./yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_user.json') as data_file:
    user = [json.loads(x) for x in data_file]

"""
#generate list of cities/states and create training, validation, and test sets
cities= []
for x in biz:# generate list of cities/states (unique)
    newCity = {'city':x['city'],'state':x['state']}
    if newCity not in cities:
        cities.append(newCity) #
cities.sort(key=operator.itemgetter('city','state'))
"""
#data sets broken into training/testing/validation by city
"""
cityRandomizer = range(len(cities))
np.random.shuffle(cityRandomizer)
#Save for later
with open('cityRandomizedOrder.csv','w') as f:
    for n in cityRandomizer:
        print n        
        f.write(str(n)+'\n')
"""
with open('cityRandomizedOrder.csv','r') as f:
    cityRandomizer = f.read().split('\n')
cityRandomizer.pop() #remove last line
cityRandomizer = [int(x) for x in cityRandomizer]

"""
trn = int(round(0.6*len(cityRandomizer)))
tst = int(round(0.8*len(cityRandomizer)))
trainingCities = [cities[x] for x in cityRandomizer[:trn]]
"""

def makeNewLine(business):
    categories = ''
    for cat in business['categories']:
        categories += cat+';'
        #convert category list to ; separated string
    x = business['business_id']+','
    x+= business['city']+','
    x+= business['state']+','
    x+= str(business['review_count'])+','
    x+= str(business['stars'])+','
    x+= categories+'\n'
    return x

#DF should have categories,city,state,bizId,stars,review_count,
with open('biz.csv','w') as f:
    f.write('bizId,city,state,review_count,stars,categories\n')
    for b in biz:
        makeNewLine(b)
        f.write(makeNewLine(b).encode('utf8'))
with open('cats.csv','w') as f:
    #long form data set of each category entry with a biz id
    f.write('bizId,category\n')
    for b in biz:
        for c in b['categories']:
            category = re.sub(',',';',c) #replace commas with ;
            newLine = b['business_id']+','+category+'\n'
            f.write(newLine)
            
#or, combine those two dataframes
def makeNewLine(business):
    x = re.sub(',',';',business['business_id'])+','
    x+= re.sub(',',';',business['city'])+','
    x+= re.sub(',',';',business['state'])+','
    x+= re.sub(',',';',str(business['review_count']))+','
    x+= re.sub(',',';',str(business['stars']))+','
    return x

#DF should have categories,city,state,bizId,stars,review_count,
with open('bizcats.csv','w') as f:
    f.write('bizId,city,state,review_count,stars,category\n')
    for b in biz:
        for c in b['categories']:
            category = re.sub(',',';',c)
            newLine = makeNewLine(b).encode('utf8')+category.encode('utf8')+'\n'
            f.write(newLine)
    
    
"""
totalStates = []
for b in biz:
    if b['state'] not in totalStates:
        totalStates.append(b['state'])
        print b['state']
        if b['state'] =='OR':
            print b
        print b['latitude'],b['longitude']
"""
#exploratory
##look at businesses in pittsburgh, PA
#thoughts on approach:
#can do an inference.or create a training,test and validation set
#and try to make predictions
#can use the trainining dataset to look for factors that contribute
#i.e. population size, number of competing restaurants
#will do the latter
# so need to
"""
1) create dataframe
2) create function for processing a city
3) do exploratory plotting on trainiing dataset and look for factors that
 contribute to star rating
4) select an algorithm to apply
5) test it
"""


bizPitt = []
for b in biz:
    if b['city'] == 'Pittsburgh':
        bizPitt.append(b)
        
bizThai = []
for b in bizPitt:
    if 'Restaurants' in b['categories'] and 'Thai' in b['categories']:
        bizThai.append(b)
#now, go through reviews for those business IDs
ids = [x['business_id'] for x in bizThai]
thaiReviews = []
for r in review:
    if r['business_id'] in ids:
        thaiReviews.append(r)
stars = [x['stars'] for x in thaiReviews]        
n, bins, patches = p.hist(stars, 50, normed=1, histtype='stepfilled')
p.setp(patches, 'facecolor', 'g', 'alpha', 0.75)    

#for each city: generate percentage of 1,2,3,4,5 star reviews as function of
#number of restaurants in category, number of restaurants
#get population density


"""
Is the final report at most 5 pages with a readable font size and a standard (A4, 8.5x11) page size?
Was the manuscript organized as: title, intro, methods, results, discussion?
Was a primary question, hypothesis or prediction task of interest clearly stated in the introduction?
Was there at least one plot or table in the manuscript?
Was there exploratory data analysis (plots, summary tables) presented that interrogates the question of interest?
Was the (or multiple) statistical model, prediction algorithm or statistical inference described in the methods section?
Are all of the methods presented in the results section introduced in the methods section?
Is the primary statistical model, statistical inference or prediction output in the results summarized and interpreted or is raw output given without description or interpretation?
Is there a description of how the results relate to the primary questions of interest, or is it otherwise clear? In other words, do not give a point if the results seem unrelated to the question of interest and there is no apparent relationship.
Was the primary question of interest answered / refuted or was there a description of why no clear answer could be obtained?
Slide deck rubric
Does the link lead to a viewable 5 slide deck?
Was the presentation 5 slides?
Was the presentation done in Rstudio presenter and is an html presentation?
Does the presentation correspond to the manuscript?
Does the presentation present a primary question of interest?
Does the presentation present the methodology used?
Was there some data in the form of a plot, table or other output shown?
Does the presentation present an answer to the primary question, a refutation or a description of why no clear answer could be obtained?
"""