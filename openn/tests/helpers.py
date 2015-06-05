# -*- coding: utf-8 -*-

import os
from pprint import PrettyPrinter

def touch(filename, times=None):
    with(open(filename,'a')):
        os.utime(filename, times)

def pp(thing):
    pprinter = PrettyPrinter(indent=2)
    pprinter.pprint(thing)
