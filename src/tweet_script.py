'''
Created on Nov 23, 2013

@author: teo
'''

import all_script_methods
from actions import main
from datastore import load
from random import randint
from time import sleep
import datetime

start = datetime.datetime.now()

with open(main.DIR_TW + 'statistics.txt','at') as f:
    f.write('Script started at: ' + start + '\n')

#decide on how many tweets we have today
no_tweets = randint(1,3) 

#sleep for a while, no need to start tweeting as soon as we start the script
initial_wait_time = randint(1,120) #minutes
sleep(60*initial_wait_time)

#actually start tweeting
for i in range(0,no_tweets):
    #tweet then wait a while
    main.tweet_one_time()
    
    tt = datetime.datetime.now()
    with open(main.DIR_TW + 'statistics.txt','at') as f:
        f.write('Tweet at: ' + tt + '\n')    
    
    sleep(60*randint(120,240))
    
endt = datetime.datetime.now()
with open(main.DIR_TW + 'statistics.txt','at') as f:
        f.write('Script ended at: ' + endt + '\n')   