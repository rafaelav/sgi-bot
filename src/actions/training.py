from sklearn.naive_bayes import GaussianNB
import time
import datetime
import calendar

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
    user_core.append(str(user['followers_count']))
    user_core.append(str(user['friends_count']))
    user_core.append(str(user['statuses_count']))
    user_core.append(str(tweets_per_hour))
    
    return user_core 

#return true for bot, false for human
def check_hb(user,hb_class):
 
    user_core = create_user_core(user)
    result = hb_class.predict(user_core)
    
    if result[0] == 1:
        return True
    else:
        return False
        
 