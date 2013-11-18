'''
Created on Nov 11, 2013

@author: rafaela
'''

import all_script_methods
import datetime

start = datetime.datetime.now()
all_script_methods.save_data_until_today_script("data", "data")
end = datetime.datetime.now()
print "[SAVE-DATA] Started at: ",start
print "[SAVE-DATA] Ended at: ",end