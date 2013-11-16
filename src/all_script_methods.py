'''
Created on Nov 11, 2013

This one runs once per day
@author: rafaela
'''
from actions import main

screen_name = "jennifer_s_life"

####################################################### SAVING DATA FOR FUTURE DAYS
# TESTED
def save_data_until_today_script(option_friends, option_followers):
    # data/ids (either everything or just ids)
    data = main.save_get_today_friends_list(screen_name, option_friends)
    print "Friends data retrieved: ",len(data)
    
    # data/ids (either everything or just ids)
    data = main.save_get_today_followers_list(screen_name, option_followers)
    print "Followers data retrieved: ",len(data)

# TESTED
def follow_script(option, initial_users, from_each_user_count,hb_clas, from_initial_users_count=None): 
    print "Follow script started"   
    if option == "random":       
        # get random in order to get from their followers some new friends
        picked = main.pick_random_users_from_list(initial_users, from_initial_users_count)
    elif option == "given":
        picked = initial_users
    
    for user in picked:
        print "Picked - ",user["screen_name"]
    
    # can follow max from_each_user_count
    picked_with_count = main.gen_random_follow_count(picked, from_each_user_count)
    # start following
    main.follow_users_followers(picked, picked_with_count, screen_name,hb_clas)    

# TESTED
def unfollow_script(friends_list, followers_list, special_users_screen_names_list, max_number_to_unfollow):
    """Unfollows at most the given number of people randomly from the friends list 
    (if it can find as many who don't follow back and if they are not in the special_users_list)"""
    print "Unfollow script started"
    to_unfollow = []
    
    # get random in order to get from their followers some new friends
    picked = main.pick_random_users_from_list(friends_list, max_number_to_unfollow)   
    print "[INFO] ",len(picked)," chosen initially"
    
    # make list with ids to see which are duplicates (doesn't work on dict)  
    picked_ids = []
    for user in picked:
        picked_ids.append(user["id_str"])
        
    picked_ids_noduplicates = list(set(picked_ids))
    
    # re-make list with user data
    picked_noduplicates = []
    for user in picked:
        if user["id_str"] in picked_ids_noduplicates:
            picked_noduplicates.append(user)
            
    print "[INFO] ",len(picked_noduplicates)," remaining after removing duplicates"    
    
    # remove legacy friends
    users_to_unfollow = []
    for user in picked_noduplicates:
        if user["screen_name"] in special_users_screen_names_list:
            print user["screen_name"]," is in legacy friends"
        else:
            users_to_unfollow.append(user)
            
    print "[INFO] ", len(users_to_unfollow)," remaining after removing legacies"

    to_blacklist = []
    
    # get followers ids (so that we won't get them every time when checking)
    followers_ids = []
    for fol in followers_list:
        followers_ids.append(fol["id_str"])
    
    for user in users_to_unfollow:
        if main.check_if_follow_back(user, followers_ids) is False:
            print "[INFO] ",user["screen_name"]," not following back -> unfollow"
            to_unfollow.append(user)
            to_blacklist.append(user["id_str"])
    
    if len(to_unfollow)>0:
        main.unfollow_unfollowers(to_unfollow)
    
    return to_blacklist

def update_black_list(to_blacklist):
    main.add_to_blacklist(to_blacklist)
    
def retrieve_legacies_tweets():
    main.get_tweets_from_legacies()

def retrieve_legacies_features():
    main.get_features_of_legacies_tweets()