# -*- coding: utf-8 -*-
import json,re
from pprint import pprint

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
    
    
    
#business has info specific to the business (hours, location etc...)
#checkin has some shit?  what does this do?
#a review entry has text of review, stars, and links to user and business ids
    #also votes, date
#tips are little tip blurbs, not sure if this is snippets from review or not
#user info has average review score, compliment frequency,
    #user was elite in what years?, fans, friend ids
    #name,nReviews,type,votes, yelping_since
    
#Quiz
#q1: 7 files in data set
#q2:data files in json format
#q3: one million lines (order of magnuitde) in reviews
#q4: going to grab and eat for 20 years
#q5: % of 5 star reviews
n5stars = 0
for r in review:
    if r['stars'] == 5:
        n5stars += 1
percent5stars = n5stars/float(len(review)) #0.369
#q6: ~60k
#q7: 
#Wi-Fi types are 'no', 'free', and 'paid'
nfreewifi = 0
nwifientries = 0
for b in biz:
    if b['attributes']:
        if 'Wi-Fi' in b['attributes'].keys():
            nwifientries += 1
            wifiType = b['attributes']['Wi-Fi']
            if wifiType == 'free':
                nfreewifi += 1
print nfreewifi/float(nwifientries)
    #if 'wifi' in biz['attributes'].keys():
     #   nreportedwifi += 1
#q8: ~500000
#q9: service
#q10: What is the name of the user with over 10,000 compliment votes of type
    #"funny"
for u in user:
    if 'funny' in u['compliments'].keys():
        if u['compliments']['funny'] > 10000:
            print u['name']
            print u['user_id']
    #Fucking...Brian
#q11: Create a 2 by 2 cross tabulation table of when a user has more than 1 
   #fans to if the user has more than 1 compliment vote of type "funny". 
   #Treat missing values as 0 (fans or votes of that type). Pass the 2 by 2 
   #table to fisher.test in R. What is the P-value for the 
   #test of independence?
fansg1TRUE = 0 #fans greater than 1
fansg1FALSE = 0 # fans not greater than 1
funnyg1TRUE = 0 #funny compliments greater than 1
funnyg1FALSE = 0 #funny compliments not greater than 1

for u in user:
    if 'funny' in u['compliments'].keys():
        if u['compliments']['funny'] > 1:
            funnyg1TRUE += 1
        else:
            funnyg1FALSE +=1
    else:
        funnyg1FALSE +=1
    if u['fans'] > 1:
        fansg1TRUE +=1
    else:
        fansg1FALSE +=1
    #      funny>1   fans>1
    #TRUE  29324       51964
    #FALSE 337391      314751
#using r fisher.test() get p-value of 2*10^-16, so < 0.01
        
    
