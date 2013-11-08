from connection import twitterapi
from retrievers import followers
# authenticati
twitter_api = twitterapi.oauth_login()

# username
username = "jennifer_s_life"

# get all followers' ids
foll = followers.get_followers_ids(twitter_api, -1, 1, screen_name=username)

print foll



