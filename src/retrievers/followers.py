"""
All the methods that deal with followers 
* getting any kind of information on followers of a user
"""
from connection import twitterapi
# 
MAX_ALLOWED = 5000

# get a user's given number of followers ids (only ids) - if a limit is not given
# than it means that all the followers' ids are needed
def get_followers_data(twitter_api, cursor, screen_name=None, user_id=None, limit=5000):    
    # Must have either screen_name or user_id (logical xor)
    assert (screen_name != None) != (user_id != None), \
    "Must have screen_name or user_id, but not both"
    
    retrieved = 0
    result = []
            
    # while there are followers to get and the needed number is stil positive
    while cursor != 0 and limit > 0:
        # we can retrieve only 5000 at once
        if limit > MAX_ALLOWED:
            count_limit = MAX_ALLOWED
        else:
            count_limit = limit
    
        # depends if we have the screen_name or the id of the follower
        if screen_name != None:
            followers_ids = twitterapi.make_twitter_request(twitter_api.followers.ids, count=count_limit, screen_name=screen_name, cursor=cursor)
            result = result + followers_ids
        else:
            followers_ids = twitterapi.make_twitter_request(twitter_api.followers.ids, count=count_limit, user_id=user_id, cursor=cursor)
            result = result + followers_ids
            
        limit = limit - count_limit
        
        # move to next followers that were not retrieved
        cursor = followers_ids["next_cursor"]
        
    # returns the needed results
    return followers_ids[:limit]


# get a user's followers screen names (only screen names)

# get information on a number of followers of a user
