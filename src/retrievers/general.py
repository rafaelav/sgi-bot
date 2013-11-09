'''
Created on Nov 8, 2013

Methods that can be used for any twitter user in general (not only for friends/followers) 
@author: rafaela
'''
from connection import twitterapi
twitter_api = twitterapi.oauth_login()

# TESTED for both uID & scr_nms
# 100 users/request max 180 req/time limit 
MAX_USER_INFO = 100
def get_info_about_users(user_ids=None, screen_names=None):
    """Given a list of user_ids/list of screen names it will return information about them"""
    
    # Must have either screen_name or user_id (logical xor)
    assert (screen_names != None) != (user_ids != None), \
    "Must have screen_name or user_id, but not both"
    
    if user_ids != None:
        needed = len(user_ids)
    else:
        needed = len(screen_names)
    results = []
    
    first = 0
    
    while needed > 0:
        if needed > MAX_USER_INFO:
            limit = MAX_USER_INFO
        else:
            limit = needed
        
        last = first + limit
        
        # make string with ids or screen names
        users_string = ""
        if user_ids != None:
            for user in user_ids:
                users_string = users_string + str(user) + ","
        else:
            for user in screen_names:
                users_string = users_string + str(user) + ","      
        
        #removing last ","
        users_string = users_string[:-1]       
        
        if user_ids != None:
            results = results +  twitterapi.make_twitter_request(twitter_api.users.lookup, user_id = users_string)
        else:
            results = results +  twitterapi.make_twitter_request(twitter_api.users.lookup, screen_name = users_string)
        needed = needed - limit
        first = last
        last = limit
    
    return results

# TESTED
def get_screen_names_from_ids(user_ids):
    """Given a list with users' user_ids, it gets their screen_names"""
    
    users_info = get_info_about_users(user_ids = user_ids)
    result = []
    for user in users_info:
        result.append(user["screen_name"])
    return result

# TESTED
def get_ids_from_screen_names(screen_names):
    """Given a list with users' screen_names, it gets their ids"""
    
    users_info = get_info_about_users(screen_names = screen_names)
    result = []
    for user in users_info:
        result.append(user["id_str"])
    return result

# TESTED
def get_users_screen_names_from_list_users(users):
    """Gets only screen_names from list with users info // list is like [{user data}, {user data}...]"""

    result = []
    
    # go through all users from the users list
    for user in users:
        result.append(user["screen_name"])
    
    return result

# TESTED
def get_users_ids_from_list_users(users):
    """Gets only user_ids from list with users info // list is like [{user data}, {user data}...]"""

    result = []
    
    # go through all users from the users list
    for user in users:
        result.append(user["id_str"])
    
    return result        