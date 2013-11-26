'''
Created on Nov 26, 2013

@author: rafaela
'''
import matplotlib.pyplot as plt
import numpy as np

def histogram(y_fol,y_unfol, y_meaning,given_title,filename):
    x_list = [7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25]
    print len(x_list)," ",len(y_fol)," ",len(y_unfol)
    
    pos = np.arange(6,int(max(x_list)+1),1)
    ax = plt.axes()
    ax.set_xticks(pos)
    
    plt.plot(x_list, y_fol, color='red')
    plt.plot(x_list,y_unfol,color='blue')
    plt.title(given_title)
    plt.xlabel('Days in which bot was active (November 2013)', fontsize=10)
    plt.ylabel(y_meaning, fontsize=10)    
    
    plt.savefig(filename) # <- saves the currently active figure (which is empty in your code)
    plt.show()
    
def histogram2(y_fol,y_unfol,y_ment, y_meaning,given_title,filename):
    x_list = [7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25]
    print len(x_list)," ",len(y_fol)," ",len(y_unfol)
    
    pos = np.arange(6,int(max(x_list)+1),1)
    ax = plt.axes()
    ax.set_xticks(pos)
    
    plt.plot(x_list,y_unfol,color='blue')
    plt.plot(x_list, y_fol, color='red')
    plt.plot(x_list,y_ment,color='black')
    plt.title(given_title)
    plt.xlabel('Days in which bot was active (November 2013)', fontsize=10)
    plt.ylabel(y_meaning, fontsize=10)    
    
    plt.savefig(filename) # <- saves the currently active figure (which is empty in your code)
    plt.show()
    
def histogram3(y_uptime,y_meaning,given_title,filename):
    x_list = [7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25]
    #print len(x_list)," ",len(y_fol)," ",len(y_unfol)
    
    pos = np.arange(6,int(max(x_list)+1),1)
    ax = plt.axes()
    ax.set_xticks(pos)
    
    plt.plot(x_list, y_uptime, color='black')
    plt.title(given_title)
    plt.xlabel('Days in which bot was active (November 2013)', fontsize=10)
    plt.ylabel(y_meaning, fontsize=10)    
    
    plt.savefig(filename) # <- saves the currently active figure (which is empty in your code)
    plt.show()

#y_fol = [20,30,21,35,27,33,31,35,24,21,19,61,27,82,23,50,36,68,39]#550+20+25+20+30+20+22
#y_unfol = [0,5,8,3,6,4,5,4,10,12,7,34,49,31,36,41,45,30,29]#359 -> 150 foll din refollow (+ ce mai sunt extra))
#histogram(y_fol,y_unfol,"Number of follows(red) and unfollows(blue)","Follows/unfollows made each day","fol_unfol.png")

#y_fol = [3,1,3,1,1,1,1,1,3,0,2,0,1,1,1,1,2,2,4]#550+20+25+20+30+20+22
#y_unfol = [1,2,3,1,2,3,3,2,1,2,1,4,0,2,2,2,3,4,2]#359 -> 150 foll din refollow (+ ce mai sunt extra))
#histogram(y_fol,y_unfol,"Number of retweets(red) and tweets(blue)","Retweets/tweets made each day","rt_t.png")

y_fol = [2,1,1,1,2,0,0,0,0,0,3,2,0,1,1,0,0,1,1]#550+20+25+20+30+20+22
#y_unfol = [0,0,0,1,1,2,0,0,0,0,0,1,0,0,0,2,1,5,1]#359 -> 150 foll din refollow (+ ce mai sunt extra))
#y_ment = [0,0,0,1,4,0,0,1,0,0,0,1,0,0,0,1,1,1,3]
#histogram2(y_fol,y_unfol,y_ment,"Number of retweets(red), favorites (blue) and mentions (black) received","Retweets/tweets/mentions from other users by day","inter.png")

# TODO - add uptime values in minutes for days 7-25 Nov
y_uptime = [138,124,214,260,246,301,289,421,392,462,473,512,442,617,430,532,505,560,494]
histogram3(y_uptime,"Up-time values (minutes)","Overview of bot up-time","up_time.png")