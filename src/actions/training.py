from sklearn.naive_bayes import GaussianNB
import time
import datetime
import calendar
import math

#read the specific data files used in classification
def get_info_hb(filename):
    X=[]
    with open(filename,'rt') as f:
        for line in f:
            words = line.split()
            tmp = []
            for word in words[1:]:
                if float(word) < 0.0001:
                    tmp.append(0.0)
                else:    
                    tmp.append(float(word))
            X.append(tmp)
    return X

#train the classifier, 0 humans, 1 bots
def train_hb(bots_filename,humans_filename):
    users = get_info_hb(humans_filename)
    bots =  get_info_hb(bots_filename)
    
    train_set = []
    train_results = []
    
    for i in users:
        train_set.append(i)
        train_results.append(0)
     
    for i in bots:
        train_set.append(i)
        train_results.append(1)
        
    gnb = GaussianNB()
    gnb.fit(train_set,train_results)
    print 'Finished training succesfully'
    return gnb

def create_user_core(user):
# calculate time of last post in Unix epoch
    time_of_creation = time.mktime(time.strptime(user['created_at'],"%a %b %d %H:%M:%S +0000 %Y"))

    # calculate time of current moment in Unix epoch
    now = datetime.datetime.now()    
    time_now = calendar.timegm(now.utctimetuple())

    number_of_hours = (time_now - time_of_creation) / 60.0

    tweets_per_hour = int(str(user['statuses_count'])) / number_of_hours

    user_core = []
    user_core.append(float(user['followers_count']))
    user_core.append(float(user['friends_count']))
    user_core.append(float(user['statuses_count']))
    user_core.append(float(tweets_per_hour))
    
    return user_core 

#return true for bot, false for human
def check_hb(user,hb_class):
 
    user_core = create_user_core(user)
    result = hb_class.predict(user_core)
    
    if result[0] == 1:
        return True
    else:
        return False
    
########################## REGRESSION PREDICTION #####################
        
# returns the % error of the difference in estimation
def error_ratio(real,est):
    return abs(real-est)*100/(real+est)

# euclidian distance between 2 dicts of tweet features        
def euclidean(dict1,dict2):
    d=0.0
    d = d + (dict1['hash_tags']-dict2['hash_tags'])**2
    d = d + (dict1['links']-dict2['links'])**2
    d = d + (dict1['mentions']-dict2['mentions'])**2
    d = d + (dict1['length_tweet']-dict2['length_tweet'])**2
    d = d + (dict1['sentiment_tweet']-dict2['sentiment_tweet'])**2
    d = d + (dict1['auth_friends']-dict2['auth_friends'])**2
    d = d + (dict1['auth_followers']-dict2['auth_followers'])**2
    d = d + (dict1['auth_ratio']-dict2['auth_ratio'])**2
    d = d + (dict1['time_of_creation']-dict2['time_of_creation'])**2
    d = d + (dict1['listed_count']-dict2['listed_count'])**2
    d = d + (dict1['rt_foll']-dict2['rt_foll'])**2

    return math.sqrt(d)
    
def adapted_distance(dict1,dict2):
    d=0.0
    d = d + (dict1['hash_tags']-dict2['hash_tags'])**2
    d = d + (dict1['links']-dict2['links'])**2
    d = d + (dict1['mentions']-dict2['mentions'])**2
    d = d + (dict1['length_tweet']-dict2['length_tweet'])**2 * 2
    d = d + (dict1['sentiment_tweet']-dict2['sentiment_tweet'])**2 * 100
    d = d + (dict1['auth_friends']-dict2['auth_friends'])**2
    d = d + (dict1['auth_followers']-dict2['auth_followers'])**2 * 1000
    d = d + (dict1['auth_ratio']-dict2['auth_ratio'])**2 * 10
    d = d + (dict1['time_of_creation']-dict2['time_of_creation'])**2 * 1000

    return math.sqrt(d)
# receives a list of dict of features for tweets (the training set) and the dict for the tweet we are interested in
def getdistances(list_existing,dict_todo):
    distancelist=[]
    for i in range(len(list_existing)):
        dict_existing=list_existing[i]
        distancelist.append((euclidean(dict_todo,dict_existing),i))
        distancelist.sort( )
    return distancelist

def gaussian(dist,sigma=10.0):
    return math.e**(-dist**2/(2*sigma**2))

# using result and avereging the firs k
def wknnestimate(list_existing,dict_todo,k=3,weightf=gaussian):
    # Get sorted distances
    dlist=getdistances(list_existing,dict_todo)
    avg=0.0
    totalweight=0.0 #
    # Take the average of the top k results
    for i in range(k):
        dist=dlist[i][0]#
        idx=dlist[i][1]
        weight=weightf(dist)#
        avg+=weight*list_existing[idx]['retweet_count']#/list_existing[idx]['real_followers_count']#
        totalweight+=weight #
    avg=avg/totalweight
    return avg
########################## END REGRESSION PREDICTION ##################### 