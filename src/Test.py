from connection import twitterapi
from actions import users, main, followers, friends
from datastore import load, save
# authenticati
twitter_api = twitterapi.oauth_login()

# username
username = "rafaela0621"

######################################### TESTING actions
######################################### TEST followers
def test_actions_followers():
    print "TEST actions/followers"
    foll = followers.get_followers_ids(-1, 5, screen_name=username)
    print "get_followers_ids:"
    print foll
    
    foll = followers.get_info_about_followers (-1, 20, screen_name=username)
    print "get_info_about_followers:"
    print foll
    
######################################### TEST friends
def test_actions_friends():
    print "TEST actions/friends"
    foll = friends.get_friends_ids(-1, 5, screen_name=username)
    print "get_friends_ids:"
    print foll
    
    foll = friends.get_info_about_friends (-1, 20, screen_name=username)
    print "get_info_about_friends:"
    print foll
    for f in foll:
        print f["screen_name"]

######################################### TEST users
def test_actions_users():
    # getting info about users with ids
    ids_list = [2177746279, 811802060, 20177741, 14340145, 913023014]
    info = users.get_info_about_users(user_ids=ids_list)
    print "get_info_about_users(ids):"
    print info

    # get screen_names from ids
    screen_names = users.get_screen_names_from_ids(ids_list)
    print "get_screen_names_from_ids: "
    print screen_names

    # getting info about users with ids
    sns_list = [u'BostonsJessica', u'networkqos', u'EffectiveMktg', u'usabilitycounts', u'Macaren07802926']
    info = users.get_info_about_users(screen_names=sns_list)
    print "get_info_about_users(screen_names):"
    print info
    
    # get ids from screen names
    ids = users.get_ids_from_screen_names(sns_list)
    print "get_ids_from_screen_names:"
    print ids
    
    # getting screen_names from list with user info
    screen_names = users.get_users_screen_names_from_list_users(info)
    print "get_users_screen_names_from_list_users: "
    print screen_names
    
    # getting ids from list with user info
    ids = users.get_users_ids_from_list_users(info)
    print "get_users_ids_from_list_users:"
    print ids

######################################### TEST main
def test_actions_main():
    #print "TEST actions: get and save today's followers list"
    #main.save_get_today_followers_list("jennifer_s_life", "ids")
    """followers_data = load.load_list_from_file("Followers/rafaela0621_followers_9.11.2013")
    
    print "pick_random_users_from_list (for 10 - run it more times and see it's random):"
    picked_users = main.pick_random_users_from_list(followers_data, 2)
    print len(picked_users)
    for u in picked_users:
        print u["screen_name"]
    
    print "pick_random_follow_count ( run it more times and see it's random):"
    follow_count_dict = main.gen_random_follow_count(picked_users, max_count=2)
    for key, val in follow_count_dict.items():
        print key," -> ",val
        
    main.follow_users_followers(picked_users, follow_count_dict, username)"""
    
    # get today's friends list
    friends_list = load.load_list_from_file("Friends/jennifer_s_life_data_friends_14.11.2013")
    for user in friends_list:
        if main.is_worth_following(user):
            print user["screen_name"]," descriprion:"
            print user["description"]
            print user["screen_name"]," is worth following"
        else:
            print user["screen_name"]," descriprion:"
            print user["description"]
            print user["screen_name"]," is NOT worth following"
    
######################################### TESTING datastore 
######################################### TEST saves
def test_datastore_save():
    print "TEST datastore: save"
    save.save_list_to_file(["ana","are","mere"], "test_save")

######################################### TEST loads
def test_datastore_load():
    print "TEST datastore: load"
    loaded_list = load.load_list_from_file("test_save")
    print loaded_list
    
#test_datastore_save()
#test_datastore_load()
#test_actions_followers()
#test_actions_users()
#test_actions_main()
#test_actions_friends()

tweets_from_chrisbrogan = load.load_list_from_file("LegaciesTweets/chrisbrogan")
for tweet in tweets_from_chrisbrogan:
    print "Text: ",tweet["text"]
    print "Retweeted: ", tweet["retweeted"]
    print "Retweet count: ", tweet["retweet_count"]
    print "Belongs to: ", tweet['user']['screen_name']

# to save initial core friends of account jennifer_s_life
"""foll = friends.get_info_about_friends (-1, 80, screen_name="jennifer_s_life")
save.save_list_to_file(foll,"core_friends_data")
print "done data"
scr_nms = []
for f in foll:
    scr_nms.append(f["screen_name"])
save.save_list_to_file(scr_nms,"core_friends_screen_names")
print "done scr"

foll = friends.get_friends_ids(-1, 80, screen_name="jennifer_s_life")
save.save_list_to_file(foll,"core_friends_ids")
print "done ids"

print len(load.load_list_from_file("core_friends_screen_names"))
print len(load.load_list_from_file("core_friends_ids"))
print len(load.load_list_from_file("core_friends_data"))"""