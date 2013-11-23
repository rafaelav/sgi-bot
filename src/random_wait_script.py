'''
Created on Nov 23, 2013

@author: rafaela
'''

from random import randint
from time import sleep
import datetime

start = datetime.datetime.now()

wait_time = randint(10*60,90*60) # between 10 and 90 mins
print "Wait before start - ",wait_time/60," min"
print "Started at ",start
sleep(wait_time)

end = datetime.datetime.now()
print "[WS] Started at: ",start
print "[WS] Ended at: ",end
