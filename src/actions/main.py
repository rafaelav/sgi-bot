'''
Created on Nov 9, 2013

Actions which are part of the bot's strategy
* follow people
* unfollow people
* verifying user's "rate" in order to follow (seeing if it's worth following)
* retweet 
* tweet

@author: rafaela
'''

from connection import twitterapi
from actions import followers, users, friends
from datastore import save
from random import randint
import datetime

twitter_api = twitterapi.oauth_login()
now = datetime.datetime.now()
today_followers_file = "_followers_" +str(now.day)+"."+str(now.month)+"."+str(now.year)
today_friends_file = "_friends_"+str(now.day)+"."+str(now.month)+"."+str(now.year)
DIR_FOL = "Followers/"
DIR_FR = "Friends/"

# get and save today's friends list (the list is saved but is also returned)
def save_get_today_friends_list(screen_name, option):
    """Get and save today's friends list (the list is saved but is also returned)"""
    
    list_user = [screen_name]
    
    # get info on user so that we can access its friends count
    user_info = users.get_info_about_users(screen_names=list_user)
    
    if option == "data":
        # get info for all friends of user
        user_friends = friends.get_info_about_friends(-1, user_info[0]["friends_count"] , screen_name=screen_name)
    elif option == "ids":
        # get info for all friends of user
        user_friends = friends.get_friends_ids(-1, user_info[0]["friends_count"] , screen_name=screen_name)
    
    # saving today's list
    save.save_list_to_file(user_friends, DIR_FR+screen_name+"_"+option+"_"+today_friends_file)
    
    return followers
    
#TESTED
def save_get_today_followers_list(screen_name, option):
    """Get and save today's followers list (the list is saved but is also returned)"""
    
    list_user = [screen_name]
    # get info on user so that we can access its followers count
    user_info = users.get_info_about_users(screen_names=list_user)
    
    if option == "data":
        # get info for all followers of user
        user_followers = followers.get_info_about_followers(-1, user_info[0]["followers_count"] , screen_name=screen_name)
    elif option == "ids":
        user_followers = followers.get_followers_ids(-1, user_info[0]["followers_count"] , screen_name=screen_name)
    
    # saving today's list
    save.save_list_to_file(user_followers, DIR_FOL+screen_name+"_"+option+"_"+today_followers_file)
    
    return followers
        
def is_worth_following(user):
    """TODO - Checks if a user is worth following and returns True/False"""
    
    return True

# TESTED                    
def pick_random_users_from_list(users, count):
    """Randomly selects users from user list (at most count)"""
    
    # when asking for more than exist, just return all followers
    if count > len(users):
        return users
    
    # list with picked followers
    picked_users = []
    
    # generating random 'count' numbers in between 0 and the total number of followers
    for i in range(0,count):
        r = randint(0,len(users))
        picked_users.append(users[r])
    
    return picked_users

# TESTED
def gen_random_follow_count(users, max_count=10):
    """Returns a dictionari with keys = screen_names and values between 0 and max_count with tell how many we want to follow associated with that screen_name (either friends of or followers of)"""
    rand_dict = dict()
    
    for user in users:
        r = randint(0,max_count)
        rand_dict[user["screen_name"]] = r
    
    return rand_dict
    
# follows a number of users randomly from the pool of friends of a list of people

# TESTED
def follow_users_followers(users_list, follow_count_each, my_screen_name):
    """Follows a number of users randomly from the pool of followers of a list of people"""
    MAX = 5000
    for user in users_list:
        # will keep track of how many people have been followed from followers of user
        followed = 0
        
        # get first 5000 ids of followers
        followers_ids = followers.get_followers_ids(-1, MAX, screen_name=user["screen_name"])
        print "[INFO] Retrieved ",len(followers_ids)," followers ids from ", user["screen_name"]
        
        # keep track where we are in the list of retrieved id's
        crt = 0 
        
        while followed < follow_count_each[user["screen_name"]] and crt < len(followers_ids):
            ids_list = [followers_ids[crt]]
            print "[INFO] Trying to add follower ",ids_list, " from ", user["screen_name"]
            potential_friend = users.get_info_about_users(user_ids=ids_list)
            crt = crt + 1
            
            # if not following already we'll follow
            if potential_friend[0]["follow_request_sent"] != True and potential_friend[0]["following"] != True and potential_friend[0]["screen_name"]!=my_screen_name:  
                worth_following = is_worth_following(potential_friend)
            else:
                print "[INFO] NOT added (following) ",potential_friend[0]["screen_name"]," - ",potential_friend[0]["id_str"]
                
            # if yes -> follow and increase followed count
            if worth_following:
                twitter_api.friendships.create(screen_name=potential_friend[0]["screen_name"])
                print "[INFO] Added ",potential_friend[0]["screen_name"]," - ",potential_friend[0]["id_str"]
                followed = followed + 1
            else:
                print "[INFO] NOT added (not worth) ",potential_friend[0]["screen_name"]," - ",potential_friend[0]["id_str"]                      