from connection import twitterapi
from actions import users, main, followers
from datastore import load, save
# authenticati
twitter_api = twitterapi.oauth_login()

# username
username = "rafaela0621"

######################################### TESTING followers
######################################### PART 0 - followers functions
# get all followers' ids
foll = followers.get_followers_ids(-1, 5, screen_name=username)
print foll

######################################### PART 1 - user_ids
# getting info about users with ids
ids_list = [2177746279, 811802060, 20177741, 14340145, 913023014]

info = users.get_info_about_users(user_ids=ids_list)
print info

# get screen_names from ids
screen_names = users.get_screen_names_from_ids(ids_list)
print "SCRNMS from IDS: ",screen_names

# getting screen_names from list with user info
screen_names = users.get_users_screen_names_from_list_users(info)
print "SCRNMS from user info: ",screen_names

######################################### PART 2 - screen_names
sns_list = [u'BostonsJessica', u'networkqos', u'EffectiveMktg', u'usabilitycounts', u'Macaren07802926']

# getting info about users with ids
info = users.get_info_about_users(screen_names=sns_list)
print info

# get ids from screen_names
ids = users.get_ids_from_screen_names(sns_list)
print "IDS from SCRNMS: ",ids

# getting ids from list with user info
ids = users.get_users_ids_from_list_users(info)
print "IDS from user info: ",ids


######################################### TESTING datastore
def test_datastore():
    save.save_list_to_file(["ana","are","mere"], "test_save")
    loaded_list = load.load_list_from_file("test_save")
    print "TEST datastore: save/load list to/from file: ", loaded_list

######################################### TESTING main actions
def test_main_actions():
    print "TEST actions: get and save today's followers list"
    main.save_get_today_followers_list(username)
    
test_datastore()
test_main_actions()