'''
Created on Nov 21, 2013

@author: rafaela
'''

import all_script_methods
from actions import main
from datastore import load
from random import randint
from time import sleep

features_file = "legacies_features"

# random number of fav (1-4)
random_fav = randint(1,4)

for i in range(1,random_fav+1):
    # get no_tweets tweets from friends
    nr_tweets = 500 
    tweets = main.get_live_tweets_from_users(list_users, nr_tweets)

    # calculate features for these tweets
    list_candidates_for_fav
    
    #get features of legacies
    list_featured_features = load.load_list_from_file(features_file)
    
    # ordonate based on possibile rt count
    aproxim = all_script_methods.aproximate_rts(list_featured_features, list_candidates_for_fav)
    
    # favorite the most rt-ed
    last = len(aproxim)
    all_script_methods.favorite_tweet(aproxim[last-1][1])
    print "[FAV] Favorited one with estimation ",aproxim[last-1][1]," rts"

    # random waiting time before starting next follow
    wait_time = randint(10*60,60*60) # between 10 and 60 mins
    print "[FAV] Sleep time ... ",wait_time/60 
    sleep(wait_time)