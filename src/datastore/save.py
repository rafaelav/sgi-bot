'''
Created on Nov 9, 2013

All save functions

@author: rafaela
'''

import io

def save_list_to_file(list_item, filename):
    with io.open('{0}'.format(filename), 'w', encoding='utf-8') as f:
        f.write(unicode(list_item))