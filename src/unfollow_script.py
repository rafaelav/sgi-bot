'''
Created on Nov 13, 2013

@author: rafaela
'''

import all_script_methods
from random import randint
from datastore import load
from time import sleep
import datetime

screen_name = "jennifer_s_life"
now = datetime.datetime.now()
today_friends_file = screen_name+"_data"+"_friends_"+str(now.day)+"."+str(now.month)+"."+str(now.year)
today_followers_file = screen_name+"_data"+"_followers_"+str(now.day)+"."+str(now.month)+"."+str(now.year)
core_friends_screen_names_file = "core_friends_screen_names"
DIR_FR = "Friends/"
DIR_FOL = "Followers/"


# random number of turns for unfollowing (1 - 3 per day)
random_turns_unfol = randint(1,3) # one turn
print "Unfollowing turns: ",random_turns_unfol

max_number_to_unfollow = randint (10/random_turns_unfol , 50/random_turns_unfol)
print "Decided to randomly unfollow at most: ", max_number_to_unfollow

friends_list = load.load_list_from_file(DIR_FR+today_friends_file)
followers_list = load.load_list_from_file(DIR_FOL+today_followers_file)
special_users_screen_names_list = load.load_list_from_file(core_friends_screen_names_file)
print special_users_screen_names_list

for i in range(1,random_turns_unfol+1):
    all_script_methods.unfollow_script(friends_list, followers_list, special_users_screen_names_list, max_number_to_unfollow)
    # generating random waiting time before next round
    wait_time = randint(20*60,5*60*60) # between (20mins) and 5h 
    print "Sleep time ... ",wait_time/60
    sleep(wait_time)
