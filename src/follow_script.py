'''
Created on Nov 9, 2013

Automatically follows people who are following the initial ones

@author: rafaela
'''
import all_script_methods
from random import randint
from datastore import load
from time import sleep
from actions import main
import datetime
from actions.training import train_hb
from actions.main import DIR_TR,bots_filename,humans_filename

start = datetime.datetime.now()
my_screen_name = "jennifer_s_life"
from_where = 1#randint(1,3) # 1 from Boston, 2 from followers of friends (legacies)

if from_where == 1:
    print "[FOLLOW] Following from BOSTON"
    
    list_sn = main.get_boston_screen_name()
    print "Before eliminating duplicates: ",len(list_sn)
    
    # eliminate duplicated ids
    list_no_duplicates = list(set(list_sn))
    print "After eliminating duplicates: ",len(list_no_duplicates)
    
    # one turn of following random x followers (where x can be at most 150 and at least 50)
    follow_count = randint(100,150)
    print "Trying to follow about: ",follow_count
    
    picked = main.pick_random_users_from_list(list_no_duplicates, follow_count)
    print "Just picked random ",len(picked)," from ",len(list_no_duplicates)," existing"
    
    #train the human/bot classifier
    hb_clas = train_hb(DIR_TR+bots_filename,DIR_TR+humans_filename)
    
    have_followed = main.follow_users(picked,my_screen_name,hb_clas)
elif from_where == 2:  
    print "[FOLLOW] Following from LEGACIES' FOLLOWERS"  
    # random number of turns for following (1 or 2 per day)
    random_turns_fol = randint(1,3) # one turn
    print "Following turns: ",random_turns_fol
        
    # initial users (can be friends/followers/legacy friends
    initial_users = load.load_list_from_file("core_friends_data")
    # random number of initial users (based also on number of turns)
    from_initial_users_count = randint (4/random_turns_fol, 11/random_turns_fol)     
    
    #train the human/bot classifier
    hb_clas = train_hb(DIR_TR+bots_filename,DIR_TR+humans_filename)
    
    # given users (if we want to follow from specific users)
    given_initial_users_screen_names = []
    given_initial_users_list = []
    for user in initial_users:
        if user["screen_name"] in given_initial_users_screen_names:
            given_initial_users_list.append(user)
            
    have_followed = 0
            
    # +1 because it can't be range (1,1)
    for i in range(1,random_turns_fol+1):
        if len(given_initial_users_list) > 0:
            # random number of how many to follow from each user
            print "Given"
            print given_initial_users_list
            
            # depends in number of users and of turns
            from_each_user_count = (150/len(given_initial_users_list))/random_turns_fol
            print "From each user: ", from_each_user_count
            
            have_followed = all_script_methods.follow_script("given", given_initial_users_list,from_each_user_count,hb_clas) + have_followed
        else:
            print "Random"
            print "Number of random users: ",from_initial_users_count
            
            # depends in number of users and of turns
            from_each_user_count = (150/from_initial_users_count)/random_turns_fol
            print "From each user (max to foll): ", from_each_user_count
            
            have_followed = all_script_methods.follow_script("random", initial_users,from_each_user_count,hb_clas,from_initial_users_count=from_initial_users_count) + have_followed
            # generating random waiting time before next round
        wait_time = randint(60*60,2*60*60) # between 1h and 2h
        print "Sleep time ... ",wait_time/60 
        sleep(wait_time)

end = datetime.datetime.now()
print "[FOLLOW] Started at: ",start
print "[FOLLOW] Ended at: ",end
print "[FOLLOW] Have followed today: ",have_followed