'''
Created on Nov 21, 2013

@author: rafaela
'''

import all_script_methods
from actions import main
from datastore import load
from random import randint
from time import sleep
import datetime

start = datetime.datetime.now()

DIR_FR = "Friends/"

features_file = "legacies_features"
now = datetime.datetime.now()
today_friends_file = "friends_"+str(now.day)+"."+str(now.month)+"."+str(now.year)

# random number of fav (1-4)
random_fav = randint(1,4)
print "[FAV] Random number of fav: ",random_fav

# load friends list
list_users = load.load_list_from_file(DIR_FR+"jennifer_s_life"+"_data_"+today_friends_file)

for i in range(1,random_fav+1):
    # get no_tweets tweets from friends
    nr_tweets = 100
    print "[FAV] Trying to get tweets..."
    tweets = main.get_live_tweets_from_users(list_users, nr_tweets)

    # calculate features for these tweets
    list_candidates_for_fav = main.get_features_of_given_tweets(tweets)
    
    #get features of legacies
    list_featured_features = load.load_list_from_file(features_file)
    
    # normalize features
    # we concatenate the 2 list, normlaize and after that split it again
    nr_featured = len(list_featured_features)
    nr_candidates = len(list_candidates_for_fav)
    complete_list = list_featured_features+list_candidates_for_fav
    norm_features = main.normalize_features(complete_list)
    list_featured_features = norm_features[:nr_featured]
    list_candidates_for_fav = norm_features[nr_featured:]
    
    # ordonate based on possibile rt count
    aproxim = all_script_methods.aproximate_rts(list_featured_features, list_candidates_for_fav)
    
    # favorite the most rt-ed
    last = len(aproxim)
    for i in range(last):
        status = all_script_methods.favorite_tweet(aproxim[last-1][0])
        if status != None:
            print "[FAV] Favorited one with estimation ",aproxim[last-1][1]," rts and id - ",aproxim[last-1][0]
            break
        else:
            print "[FAV] Couldn't fav - None returned"
        last = last - 1

    # random waiting time before starting next follow
    wait_time = randint(10*60,60*60) # between 10 and 60 mins
    print "[FAV] Sleep time ... ",wait_time/60," min"
    sleep(wait_time)
    
end = datetime.datetime.now()
print "[FAV] Started at: ",start
print "[FAV] Ended at: ",end
print "[FAV] Have fav today: ",random_fav