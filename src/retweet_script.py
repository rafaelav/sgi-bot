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

with open(main.DIR_RT + 'statistics.txt','at') as f:
    f.write('Script started at: ' + start + '\n')
    
no_retweets = randint(2,4) 

#sleep for a while, no need to start tweeting as soon as we start the script
initial_wait_time = randint(1,120) #minutes
sleep(60*initial_wait_time)

for i in range(0,no_retweets):
    #tweet then wait a while
    main.retweet_one_time()
    
    tt = datetime.datetime.now()
    with open(main.DIR_RT + 'statistics.txt','at') as f:
        f.write('Retweet at: ' + tt + '\n')    
    
    sleep(60*randint(120,240))
    
endt = datetime.datetime.now()
with open(main.DIR_RT + 'statistics.txt','at') as f:
        f.write('Script ended at: ' + endt + '\n')       