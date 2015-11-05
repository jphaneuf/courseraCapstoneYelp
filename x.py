# -*- coding: utf-8 -*-
"""
Created on Mon Nov  2 18:41:34 2015

@author: jphaneuf
"""

import json,re
from pprint import pprint
import pylab as p
import pandas

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


#exploratory
##look at businesses in pittsburgh, PA

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