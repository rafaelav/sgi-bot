'''
Created on Nov 9, 2013

All load methods

@author: rafaela
'''
import io

def load_list_from_file(filename):
    with io.open('{0}'.format(filename), encoding='utf-8') as f:
        return f.read()