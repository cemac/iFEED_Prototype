#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
General Error Library

Created on Thu Jan 30 15:01:49 2020

@author: chmcsy
"""

from sys import stderr, exit

class ArgumentsError(Exception):
    '''
    Exception raised when there is an error detected in the argument list.
    '''
    def __init__(self, msg):
        stderr.write('[FATAL ERROR] : %s' % msg )
        exit(9)
        
class FatalError(Exception):
    '''
    Exception raised when there is an error detected in the argument list.
    '''
    def __init__(self, msg):
        stderr.write('[FATAL ERROR] : %s' % msg )
        exit(9)

class FileError(Exception):
    '''
    Exception raised when contents of files are not as expected
    '''
    def __init__(self,msg):
        stderr.write('[FILE ERROR] : %s' % msg )
        exit(9)

class NonFatal(Exception):
    '''
    Exception raised for non-fatal errors
    '''
    def __init__(self,msg):
        stderr.write('[WARNING] : %s\n\nContinuing...\n' % msg )
        