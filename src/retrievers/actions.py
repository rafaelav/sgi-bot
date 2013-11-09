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
from retrievers import followers, general
from datastore import save
from datastore import load
from random import randint
import datetime

twitter_api = twitterapi.oauth_login()
now = datetime.datetime.now()
today_followers_file = "_followers_" +str(now.day)+"."+str(now.month)+"."+str(now.year)
today_friends_file = "_friends_"+str(now.day)+"."+str(now.month)+"."+str(now.year)
DIR_FOL = "Followers/"
DIR_FR = "Friends/"

# get and save today's friends list (the list is saved but is also returned)
#def save_get_today_friends_list(user):
    
def save_get_today_followers_list(screen_name):
    """Get and save today's followers list (the list is saved but is also returned)"""
    
    list_user = [screen_name]
    # get info on user so that we can access its followers count
    user_info = general.get_info_about_users(list_user)
    # get info for all followers of user
    followers = followers.get_info_about_followers(-1, user_info["followers_count"] , screen_name=screen_name)
    
    # saving today's list
    save.save_list_to_file(followers, DIR_FOL+screen_name+today_followers_file)
    
    return followers
        
def is_worth_following(user):
    """Checks if a user is worth following and returns True/False"""
    
    return True
                    
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

def gen_random_follow_count(users, max_count=10):
    """Returns a dictionari with keys = screen_names and values between 0 and max_count with tell how many we want to follow associated with that screen_name (either friends of or followers of)"""
    rand_dict = dict()
    
    for user in users:
        r = randint(0,max_count)
        rand_dict[user["screen_name"]] = r
    
    return rand_dict
    
# follows a number of users randomly from the pool of friends of a list of people

def follow_users_followers(users, follow_count_each):
    """Follows a number of users randomly from the pool of followers of a list of people"""
    for user in users:
        # will keep track of how many people have been followed from followers of user
        followed = 0
        while followed < follow_count_each[user["screen_name"]]:
            # getting info about followers starting with recent followers of the usr
            user_followers = followers.get_info_about_followers(-1, user["followers_count"], screen_name=user["screen_name"])
            
            # for each follower of the user on which we have info
            for follower in user_followers:
                # we test if it is worth following (based on our strategic picked features)
                worth_following = is_worth_following(follower)
                
                # if yes -> follow and increase followed count
                if worth_following:
                    twitter_api.friendships.create(screen_name=user["screen_name"])
                    followed = followed + 1
                       