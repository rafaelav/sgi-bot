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

y_fol = [20,30,21,10,7,13,11,5,4,21,17,61,27,82,23,50,36,68,39]#550
y_unfol = [0,5,8,3,6,4,5,4,10,12,7,34,49,31,36,41,45,30,29]#399 -> 150 foll din refollow (+ ce mai sunt extra))
histogram(y_fol,y_unfol,"Number of follows(red) and unfollows(blue)","Follows/unfollows made each day","fol_unfol.png")