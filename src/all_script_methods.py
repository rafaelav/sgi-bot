'''
Created on Nov 11, 2013

This one runs once per day
@author: rafaela
'''
from actions import main

screen_name = "jennifer_s_life"

####################################################### SAVING DATA FOR FUTURE DAYS
def save_data_until_today_script():
    # data/ids (either everything or just ids)
    data = main.save_get_today_friends_list(screen_name, "data")
    print "Friends data retrieved: ",len(data)
    
    # data/ids (either everything or just ids)
    data = main.save_get_today_followers_list(screen_name, "data")
    print "Followers data retrieved: ",len(data)

def follow_script(option, initial_users, froam_each_user_count, from_initial_users_count=None):    
    if option == "random":       
        # get random in order to get from their followers some new friends
        picked = main.pick_random_users_from_list(initial_users, from_initial_users_count)
    elif option == "given":
        picked = initial_users
    
    picked_with_count = main.gen_random_follow_count(picked, froam_each_user_count)
    # start following
    main.follow_users_followers(picked, picked_with_count, screen_name)    
    
    
############################################## MAIN 
    
###################### SAVE PART
#save_data_until_today_script()