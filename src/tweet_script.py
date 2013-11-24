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
    f.write('Script started at: ' + str(start) + '\n')

#decide on how many tweets we have today
no_tweets = randint(1,3)
print 'Decided tweeting ' + str(no_tweets) + ' times' 

#sleep for a while, no need to start tweeting as soon as we start the script
initial_wait_time = randint(1,120) #minutes
print 'Waiting ' + str(initial_wait_time) + ' for program to start' 
sleep(60*initial_wait_time)

#actually start tweeting
for i in range(0,no_tweets):
    #tweet then wait a while
    main.tweet_one_time()
    
    tt = datetime.datetime.now()
    with open(main.DIR_TW + 'statistics.txt','at') as f:
        f.write('Tweet at: ' + str(tt) + '\n')    
    
    
    in_between_wait_time = randint(120,240)
    print 'Tweet succesfull, waiting for ' + str(in_between_wait_time) + ' minutes before next tweet'
    sleep(60*in_between_wait_time)
    
endt = datetime.datetime.now()
with open(main.DIR_TW + 'statistics.txt','at') as f:
        f.write('Script ended at: ' + str(endt) + '\n')   