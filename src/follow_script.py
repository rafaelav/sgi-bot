'''
Created on Nov 9, 2013

Automatically follows people who are following the initial ones

@author: rafaela
'''

from datastore import load
from actions import main

screen_name = "jennifer_s_life"

# inirial users in order to start following some of their followers
initial_users = load.load_list_from_file("core_friends_data")

# get random 10 in order to get from their followers some new friends
picked = main.pick_random_users_from_list(initial_users, 10)
picked_with_count = main.gen_random_follow_count(picked, 10)

# start following
main.follow_users_followers(picked, picked_with_count, screen_name)
