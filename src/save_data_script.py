'''
Created on Nov 11, 2013

@author: rafaela
'''

from actions import main

screen_name = "jennifer_s_life"

# data/ids (either everything or just ids)
main.save_get_today_friends_list(screen_name, "data")

# data/ids (either everything or just ids)
main.save_get_today_followers_list(screen_name, "data")