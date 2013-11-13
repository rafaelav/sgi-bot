'''
Created on Nov 9, 2013

All load methods

@author: rafaela
'''
import io
import ast

#TESTED
def load_list_from_file(filename):
    """ Loads content of file with the given filename"""
    with io.open('{0}'.format(filename), encoding='utf-8') as f:
        elem = f.read()
        return ast.literal_eval(elem)
