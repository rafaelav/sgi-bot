"""
All the methods that deal with followers 
* getting any kind of information on followers of a user
"""
from connection import twitterapi

# The maximum number of ids that can be retriev in one call from twitter api 
MAX_ALLOWED_IDS = 5000
# maximum number of users that can be retrieved from api
MAX_ALLOWED_SCRNMS = 200
# twitter api connection
twitter_api = twitterapi.oauth_login()

# TESTED
def get_friends_ids(cursor, limit, screen_name=None, user_id=None):
    """Get a user's given number of friends ids (only ids). If a limit is not given than it means that all the friends' ids are needed (limit of calls = 15)"""
    
    # Must have either screen_name or user_id (logical xor)
    assert (screen_name != None) != (user_id != None), \
    "Must have screen_name or user_id, but not both"
    
    assert (limit > 0), "The requested number of ids must be higher than 0"
    
    result = []
    needed = limit
            
    # while there are friends to get and the needed number is still positive
    while cursor != 0 and needed > 0:
        # we can retrieve only 5000 at once
        if needed > MAX_ALLOWED_IDS:
            count_limit = MAX_ALLOWED_IDS
        else:
            count_limit = needed
    
        # depends if we have the screen_name or the id of the follower
        if screen_name != None:
            friends_ids = twitterapi.make_twitter_request(twitter_api.friends.ids, count=count_limit, screen_name=screen_name, cursor=cursor)
            result = result + friends_ids["ids"]
        else:
            friends_ids = twitterapi.make_twitter_request(twitter_api.friends.ids, count=count_limit, user_id=user_id, cursor=cursor)
            result = result + friends_ids["ids"]
            
        needed = needed - count_limit
        
        # move to next friends that were not retrieved
        cursor = friends_ids["next_cursor"]
        
    # returns the needed results
    return result[:limit]

# TESTED
def get_info_about_friends (cursor, limit, screen_name=None, user_id=None):
    """Get friends of screen_name/user_id information (all information on them)"""
        
    # Must have either screen_name or user_id (logical xor)
    assert (screen_name != None) != (user_id != None), \
    "Must have screen_name or user_id, but not both"
    
    assert (limit > 0), "The requested number of ids must be higher than 0"
    
    result = []
    needed = limit
            
    # while there are friends to get and the needed number is still positive
    while cursor != 0 and needed > 0:
        # we can retrieve only 5000 at once
        if needed > MAX_ALLOWED_SCRNMS:
            count_limit = MAX_ALLOWED_SCRNMS
        else:
            count_limit = needed
    
        # depends if we have the screen_name or the id of the follower
        if screen_name != None:
            friends_data = twitterapi.make_twitter_request(twitter_api.friends.list, count=count_limit, screen_name=screen_name, cursor=cursor)
            result = result + friends_data["users"]
        else:
            friends_data = twitterapi.make_twitter_request(twitter_api.friends.ids, count=count_limit, user_id=user_id, cursor=cursor)
            result = result + friends_data["users"]
            
        needed = needed - count_limit
        
        # move to next friends that were not retrieved
        cursor = friends_data["next_cursor"]
        
    # returns the needed results
    return result[:limit]