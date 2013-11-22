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
from datastore import save,load
from random import randint
from time import sleep
import datetime
from nltk.corpus import stopwords
import string
import time
from training import check_hb
import twitter


twitter_api = twitterapi.oauth_login()
now = datetime.datetime.now()
today_followers_file = "followers_" +str(now.day)+"."+str(now.month)+"."+str(now.year)
today_friends_file = "friends_"+str(now.day)+"."+str(now.month)+"."+str(now.year)
today_black_list = "blacklist_"+str(now.day)+"."+str(now.month)+"."+str(now.year)
bio_bad_words = "bio_bad_words"
bio_good_words = "bio_good_words"
legacies_data_file = "core_friends_data"
features_file = "legacies_features"
stats_happyiness_file ="happiness_ratings.txt"
bots_filename = 'bots_features.txt'
humans_filename = 'users_features.txt'

if now.day == 1:
    yesterday_black_list = "blacklist_"+"30"+"."+str(now.month-1)+"."+str(now.year)
else:
    yesterday_black_list = "blacklist_"+str(now.day-1)+"."+str(now.month)+"."+str(now.year)
    
DIR_FOL = "Followers/"
DIR_FR = "Friends/"
DIR_BL = "Blacklist/"
DIR_LU = "LegaciesTweets/"
DIR_US = "UsersTweets/"
DIR_TR = 'Training/'

def get_live_tweets_from_users(list_users, nr_tweets):
    """ Starts listening to tweets from the given users and returns the first no_tweets it gets from any of them"""
    l=[]
    count = 0
    list_of_ids = ''
    filtering_list = []
    
    #build the list of users
    for user in list_users:
        if 'id_str' in user.keys():
            list_of_ids = list_of_ids + user['id_str']+','
            filtering_list.append(user['id_str'])
        else:
            print 'No id_str field in user parameter'
            
    list_of_ids = list_of_ids[:-1]            
    
    twitter_stream = twitter.TwitterStream(auth=twitter_api.auth)
    stream = twitter_stream.statuses.filter(follow = list_of_ids)
    
    for tweet in stream:
        if count == nr_tweets: #change back to 1000 or 2000 after testing
            break    
        if tweet['lang'] == 'en':
            if 'user' in tweet.keys():
                if tweet['user']['id_str'] in filtering_list:
                    l.append(tweet)
                    count  = count + 1
            
    return l

def get_boston_screen_name():
    l=[]
    count = 0
    
    twitter_stream = twitter.TwitterStream(auth=twitter_api.auth)
    stream = twitter_stream.statuses.filter(locations = '-71.7,42.19,70.59,42.24')
    
    for tweet in stream:
        if count == 500: #change back to 1000 or 2000 after testing
            break    
        if tweet['lang'] == 'en':
            if 'user' in tweet.keys():
                if 'screen_name' in tweet['user'].keys():
                    l.append(tweet['user']['screen_name'])
                    count  = count + 1
                    print "[GETTING From BOSTON] reached: ",count
    
    return l

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
    
    return user_friends
    
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
    
    return user_followers

# TESTED (in previous homework)
def get_words_from_text(text):
    """Removes punctuation and returns only the list of words - punctuation = !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""
    formated_text = "".join(l for l in text if l not in string.punctuation)
    return formated_text.split()

# TESTED (in previous homework)
def get_tokens(text):
    """Returns words of given text (tokens) but with lower letters and ignoring stopwords"""
    word_list_lower = []
    word_list = get_words_from_text(text)
    
    # convert all words to lower case
    for w in word_list:
        # we need to check if it's english word and if it's not stopword
        if w.lower() not in stopwords.words('english'):# and d.check(w) == True:
            word_list_lower.append(w.lower())
        
    return word_list_lower

def wait_random_time():
    wait_time = randint(45,5*60) # between 1min and 3min
    print "Sleep time before trying to follow/unfollow next user... ",wait_time," sec" 
    sleep(wait_time)

############ HAPPINESS ############
# TESTED in previous assignments
def get_happiness_of_words():
    """Returns a dictionary (key = word, value = happiness q)"""
    
    text = load.load_text_from_file(stats_happyiness_file)
    
    # skip initial non interesting things
    text = text[172:]
    
    # make list ignoring spaces
    text_list = text.split()
    #print text_list[:10]
    
    # getting words & ratings for them
    crt = 0
    word_list = []
    rating_list = []
    for word in text_list:
        if crt % 8 == 0:
            word_list.append(word)
            rating_list.append(text_list[crt+2])
        crt = crt + 1
    
    # making dictionary with data
    dictionary = dict()
    crt = 0
    while crt < len(word_list):
        dictionary[word_list[crt]]=rating_list[crt]
        crt = crt + 1
    return dictionary

# TESTED in other assignments
def get_tweets_text(user):
    """ Returns the concatenated text of the last 200 tweets of the user"""
    tweets = users.get_user_tweets(screen_name=user["screen_name"])
    
    # getting full text of tweets in this
    fulltext = ""
    
    for tweet in tweets:
        if tweet["lang"]=="en":        
            fulltext = fulltext +" "+tweet["text"] # full text    
    
    return fulltext

# TESTED in other assignments
def get_happiness_level(user):
    """Returns sum of happines values, happiness value (calculated only for words found in list, number of words found """
    fulltext = get_tweets_text(user)
    
    word_list_lower = []
    
    # all words used in the users tweets
    words_list = get_words_from_text(fulltext)

    # convert all words to lower case (this == This)
    for w in words_list:
        word_list_lower.append(w.lower())
    
    # sum of happiness per each word and then division to get average happiness
    happiness_dict = get_happiness_of_words()
    suma = 0.0
    used_words = 0
    for word in word_list_lower:
        if happiness_dict.get(word) is not None :
            suma = suma + float(happiness_dict.get(word))
            used_words = used_words + 1 #only found words for happiness we use in division
            
    # maybe no words from list where used
    if suma == 0:
        return suma, used_words,0
    
    #print "words = ",len(word_list_lower)," --- ",suma," / ",used_words," = ",suma/used_words
    return suma, used_words, suma/used_words

def get_tweet_happiness(tweet):
    # all words used in the users tweets
    words_list = get_words_from_text(tweet['text'])

    word_list_lower = []
    # convert all words to lower case (this == This)
    for w in words_list:
        word_list_lower.append(w.lower())
    
    # sum of happiness per each word and then division to get average happiness
    happiness_dict = get_happiness_of_words()
    suma = 0.0
    used_words = 0
    for word in word_list_lower:
        if happiness_dict.get(word) is not None :
            suma = suma + float(happiness_dict.get(word))
            used_words = used_words + 1 #only found words for happiness we use in division
            
    # maybe no words from list where used
    if suma == 0:
        return 4.5 # if no words where found we'll assume it's a slightly sad tweet
    
    #print "words = ",len(word_list_lower)," --- ",sum," / ",used_words," = ",sum/used_words
    return suma/used_words    
##########################################

# TESTED
def contains_any_from_tokens(words_lower, token_list):
    """Gets a list with words in lowercase and tests if they contain words from the second list"""
    for word in words_lower:
        if word in token_list:
            print "[User-2-Follow] Description contains word: ",word
            return True
    return False

def contains_sections(text):
    if "follow back" in text.lower():
        print "Description contains follow back"
        return True
    if "team follow" in text.lower():
        print "Description contains team follow"
        return True    
    return False

# tested up til now                
def is_worth_following(user,hb_clas):
    """TODO Checks if a user is worth following and returns True/False"""
    # check if in blacklist
    black_list = load.load_list_from_file(DIR_BL+yesterday_black_list)
    if user["id_str"] in black_list:
        return False
    
    # check language
    if user["lang"] != "en":
        return False
    
    # check followers count
    if user["followers_count"] < 50: #or user["followers_count"] > 3000:
        return False
    
    # analysing descrisption of the user
    description = user["description"]
    
    # no description (basically someone who didn't care how they look or who is not very good at using twitter)
    if len(description) < 1:
        return False 
    
    words_lower = get_tokens(description)
    bad_tokens = load.load_list_from_file(bio_bad_words)
    good_tokens = load.load_list_from_file(bio_good_words)
    
    # check some unwanted phrases
    if contains_sections(user["description"]):
        return False
    
    # if at least one of the bad words is identified -> we don't follow
    if contains_any_from_tokens(words_lower, bad_tokens):
        return False
    
    # if any of the good words are identified and there was no bad word -> follow
    if contains_any_from_tokens(words_lower, good_tokens):
        return True
    
    # if no good and no bad -> we decide based on happiness rating of last 200 tweets and frequency of posting
    suma, used_words, happiness = get_happiness_level(user)
    print "[",user["screen_name"],"] happiness: ", happiness, " = ",suma," : ",used_words
    if happiness<5.0:
        print "[",user["screen_name"],"] Not happy enough" 
        return False
    
    #if true, the user is a bot, and we dont follow bots
    if check_hb(user, hb_clas) == True:
        return False
    
    return True # to change to false when added the happiness & freq of posting

# TESTED                    
def pick_random_users_from_list(users, count, start=0, end=None):
    """Randomly selects users from user list (at most count)"""
    
    # when asking for more than exist, just return all followers
    if count > len(users):
        return users
    
    # list with picked followers
    picked_users = []
    
    # generating random 'count' numbers in between 0 (or start) and the total number of followers
    for i in range(0,count):
        if end is not None:
            r = randint(start,end) # -1 because it can generate also that number
        else:
            r = randint(start,len(users)-1) # -1 because it can generate also that number
        print r
        picked_users.append(users[r])
    
    return picked_users

# TESTED
def gen_random_follow_count(users, max_count=10):
    """Returns a dictionari with keys = screen_names and values between 0 and max_count with tell how many we want to follow associated with that screen_name (either friends of or followers of)"""
    rand_dict = dict()
    
    for user in users:
        r = randint(1,max_count)
        rand_dict[user["screen_name"]] = r
    
    return rand_dict
    
# follows a number of users randomly from the pool of friends of a list of people

# TESTED
def follow_users_followers(users_list, follow_count_each, my_screen_name,hb_clas):
    """Follows a number of users randomly from the pool of followers of a list of people"""
    MAX = 5000
    have_followed_in_total = 0
    for user in users_list:
        # will keep track of how many people have been followed from followers of user
        followed = 0
        
        print "[INFO] Need to follow -- ",follow_count_each[user["screen_name"]]," -- from -- ",user["screen_name"]
        
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
                worth_following = is_worth_following(potential_friend[0],hb_clas)
            else:
                print "[INFO] NOT added (following) ",potential_friend[0]["screen_name"]," - ",potential_friend[0]["id_str"]
                continue
                
            # if yes -> follow and increase followed count
            if worth_following:
                twitter_api.friendships.create(screen_name=potential_friend[0]["screen_name"])
                print "[INFO][",followed+1,"] Added ",potential_friend[0]["screen_name"]," - ",potential_friend[0]["id_str"]
                followed = followed + 1
                wait_random_time()
            else:
                print "[INFO] NOT added (not worth) ",potential_friend[0]["screen_name"]," - ",potential_friend[0]["id_str"]
        
        have_followed_in_total = have_followed_in_total + followed
    
    return have_followed_in_total

def follow_users(users_list,my_screen_name,hb_clas):
    have_followed_in_total = 0
    
    all_users_data = users.get_info_about_users(screen_names=users_list)
    for user in all_users_data:
        # if not following already we'll follow
        if user["follow_request_sent"] != True and user["following"] != True and user["screen_name"]!=my_screen_name:  
            worth_following = is_worth_following(user,hb_clas)
        else:
            print "[INFO] NOT added (following) ",user["screen_name"]," - ",user["id_str"]
            continue
                
        # if yes -> follow and increase followed count
        if worth_following:
            twitter_api.friendships.create(screen_name=user["screen_name"])
            print "[INFO][",have_followed_in_total+1,"] Added ",user["screen_name"]," - ",user["id_str"]
            have_followed_in_total = have_followed_in_total + 1
            wait_random_time()
        else:
            print "[INFO] NOT added (not worth) ",user["screen_name"]," - ",user["id_str"]
    
    return have_followed_in_total        
# TESTED        
def unfollow_unfollowers(users):
    """Unfollows the users in the given list"""
    for user in users:
        twitter_api.friendships.destroy(screen_name = user["screen_name"])
        # wait before trying to unfollow someone new
        wait_random_time()

# TESTED        
def check_if_follow_back(user, followers_ids):
    """Returns True if user follows back and False if note"""
    if user["id_str"] not in followers_ids:  
        return False
    return True       

# TESTED
def add_to_blacklist(users_ids):
    new_black_list = []
    new_black_list = new_black_list + load.load_list_from_file(DIR_BL+yesterday_black_list)
    print "Blacklist from before: ",new_black_list
    
    for user_id in users_ids:
        new_black_list.append(user_id)
    
    print "New blacklist from before: ",new_black_list    
    save.save_list_to_file(new_black_list, DIR_BL+today_black_list)

########################## REGRESSION PREDICTION RELATED CODE ####     
# TESTED
def get_tweets_from_legacies():
    """[RAN ONCE] Gets last 200 tweets from legacy friends and saves them in a file for each user"""
    legacies = load.load_list_from_file(legacies_data_file)
    
    for legacy in legacies:
        tweets = users.get_user_tweets(screen_name=legacy["screen_name"])
        save.save_list_to_file(tweets, DIR_LU+legacy["screen_name"])
        
# TESTED in assignment
def get_tweet_mentions(tweet):
    """ Returns the number of "@" in tweet"""
    
    if tweet["entities"].get("user_mentions") is None:
        return 0
    return len(tweet["entities"]["user_mentions"])

# TESTED in assignment
def get_tweet_links(tweet):
    """Returns the number of links in tweet"""
    
    if tweet["entities"].get("urls") is None:
        return 0
    return len(tweet["entities"]["urls"])

# TESTED in assignment
def get_tweet_hashes(tweet):
    """Returns the number of "#" in tweet"""
    
    if tweet["entities"].get("hashtags") is None:
        return 0
    return len(tweet["entities"]["hashtags"])

# TESTED in assignment
def get_unix_time_of_tweet_creation(tweet):
    """Returns the time at which the tweet was created"""
    
    # calculate time of last post in Unix epoch
    time_last_post = time.mktime(time.strptime(tweet['created_at'],"%a %b %d %H:%M:%S +0000 %Y"))
    return time_last_post

# TESTED in assignment
def get_tweet_len(tweet):
    """ Returns the number of chars in tweet"""
    return len(tweet['text'])

# TESTED in assignment
def get_tweet_sentiment(tweet):
    """ Returns the happiness level of tweet"""
    return get_tweet_happiness(tweet)
    
def get_features_of_legacies_tweets():
    """ Saves the features of the legacy friends' tweets"""
    list_users = load.load_list_from_file(legacies_data_file)
            
    # dictionaries with users, their no of friends, followers and ration between the two
    users_friends_count_dict = dict()
    users_followers_count_dict = dict()
    users_ratio_dict = dict()
    
    users_screen_names = []
    for user in list_users:
        users_screen_names.append(user["screen_name"])
        users_friends_count_dict[user['screen_name']] = user["friends_count"] 
        users_followers_count_dict[user['screen_name']] = user["followers_count"]
        users_ratio_dict[user['screen_name']] = (user["followers_count"]+1.0)/(user["friends_count"]+1.0)
    
    # good tweets will have more than 3 RT
    good_tweets = []
    
    for user in list_users:
        user_file = DIR_LU+user["screen_name"]
                          
        user_tweets = load.load_list_from_file(user_file)
        
        for tweet in user_tweets:
            # more than 2 RTs and it is not a RT-ed tweet
            if tweet["retweet_count"] >= 10 and tweet["retweeted"]==False:              
                good_tweets.append(tweet)
                
    print "[Fav] Identified good tweetis from legacies: ",len(good_tweets)
        #save_data("AllTweets",str(all_tweets_of_users))
        
    list_tweets_feat = []
        
    # get tweet features
    for tweet in good_tweets:
        mentions = get_tweet_mentions(tweet)
        links = get_tweet_links(tweet)
        hash_tags = get_tweet_hashes(tweet)
        time_of_creation = get_unix_time_of_tweet_creation(tweet)
        length_tweet = get_tweet_len(tweet)
        sentiment_tweet = get_tweet_sentiment(tweet)
        retweet_count = tweet['retweet_count']
        verified = tweet['user']['verified']
        listed_count = tweet['user']['listed_count']
        tweet_id = tweet['id']
            
        auth_followers = users_followers_count_dict[tweet['user']['screen_name']]
        auth_friends = users_friends_count_dict[tweet['user']['screen_name']]
        auth_ratio = users_ratio_dict[tweet['user']['screen_name']]
        tweet_info = dict()
            
        tweet_info["mentions"] = mentions
        tweet_info["links"] = links
        tweet_info["hash_tags"] = hash_tags
        tweet_info["time_of_creation"] = time_of_creation
        tweet_info["length_tweet"] = length_tweet
        tweet_info["sentiment_tweet"] = sentiment_tweet
        tweet_info["auth_followers"] = auth_followers
        tweet_info["auth_friends"] = auth_friends
        tweet_info["auth_ratio"] = auth_ratio
        tweet_info["retweet_count"] = retweet_count
        tweet_info["verified"] = verified
        tweet_info["listed_count"]= listed_count
        tweet_info["tweet_id"] = tweet_id
        
        list_tweets_feat.append(tweet_info)
    
    save.save_list_to_file(list_tweets_feat, features_file)

def normalize_features(features):
    """Normalizez the values calculated for legacies features of tweets"""
    # calculate max number of each element found in tweets (needed for normalization)
    max_hash_tags = 0
    max_links = 0
    max_mentions = 0
    max_len = 0
    max_sentiment = 0
    max_friends = 0
    max_followers = 0
    max_ratio = 0 # calculated as (no of followers + 1)/no friends
    max_time = 0 #most recent time
    max_rt_count = 0
    max_listed_count = 1
    max_rt_foll = 0
    for feat in features:
        # get max hash-tags
        if feat['hash_tags'] > max_hash_tags:
            max_hash_tags = feat['hash_tags']
        # get max links
        if feat['links'] > max_links:
            max_links = feat['links']
        # get max mentions
        if feat['mentions'] > max_mentions:
            max_mentions = feat['mentions']        
        # get length of tweet
        if feat['length_tweet'] > max_len:
            max_len = feat['length_tweet']    
        # get sentiment
        if feat['sentiment_tweet'] > max_sentiment:
            max_sentiment = feat['sentiment_tweet']    
        # get friends of user
        if feat['auth_friends'] > max_friends:
            max_friends = feat['auth_friends']    
        # get followers
        if feat['auth_followers'] > max_followers:
            max_followers = feat['auth_followers']    
        feat['real_followers_count']=feat['auth_followers']
        # get ratio
        if feat['auth_ratio'] > max_ratio:
            max_ratio = feat['auth_ratio']    
        # get time
        if feat['time_of_creation'] > max_time:
            max_time = feat['time_of_creation']    
        # get retweet_count
        if feat['retweet_count'] > max_rt_count:
            max_rt_count = feat['retweet_count']
        if (feat['retweet_count']+0.0)/feat['auth_followers'] > max_rt_foll:
            max_rt_foll = (feat['retweet_count']+0.0)/feat['auth_followers']
        feat['rt_foll']=(feat['retweet_count']+0.0)/feat["auth_followers"]
            # get retweet_count
        if feat['listed_count'] > max_listed_count:
            max_listed_count = feat['listed_count']
    
    # normalize data 
    for feat in features:
        # normalize hash-tags
        feat['hash_tags'] = (feat['hash_tags']+0.0)/max_hash_tags
        # normalize links
        feat['links'] = (feat['links']+0.0)/max_links
        # normalize mentions
        feat['mentions'] = (feat['mentions']+0.0)/max_mentions
        # normalize of tweet
        feat['length_tweet'] = (feat['length_tweet']+0.0)/max_len
        # normalize sentiment
        feat['sentiment_tweet'] = (feat['sentiment_tweet']+0.0)/max_sentiment
        # normalize friends of user
        feat['auth_friends'] = (feat['auth_friends']+0.0)/max_friends
        # normalize followers
        feat['auth_followers'] = (feat['auth_followers']+0.0)/max_followers
        # normalize ratio
        feat['auth_ratio'] = (feat['auth_ratio']+0.0)/max_ratio
        # normalize time
        feat['time_of_creation'] = (feat['time_of_creation']+0.0)/max_time
        # normalize listed count
        feat['listed_count'] = (feat['listed_count']+0.0)/max_listed_count
        # normalize ret/foll values
        feat['rt_foll'] = (feat['rt_foll']+0.0)/max_rt_foll
    
    # normalized features
    return features,max_hash_tags,max_links,max_mentions,max_len,max_sentiment,max_friends,max_followers,max_ratio,max_time,max_rt_count,max_listed_count,max_rt_foll

def favorite_a_tweet(tweet_id,my_screen_name):
    """ Favorites the tweet with the given id, if the given username hasn't already favorited that tweet"""
    # get last 20 favs and make sure this one is not among them
    favs = twitterapi.make_twitter_request(twitter_api.favorites.list, screen_name = my_screen_name)
    found = False
    
    for fav in favs:
        if fav["id"] == tweet_id:
            found = True
            break
        
    if found == False:
        twitterapi.make_twitter_request(twitter_api.favorites.create, tweet_id)
##################################################################
