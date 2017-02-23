# -*- coding: utf-8 -*-

import os
import shutil
import tempfile
import subprocess
from pprint import PrettyPrinter
from sys import platform


def touch(filename, times=None):
    with(open(filename,'a')):
        os.utime(filename, times)

def pp(thing):
    pprinter = PrettyPrinter(indent=2)
    pprinter.pprint(thing)

def save_and_open(file):
    """ Copy file to a temp location and open it using the Mac os """
    ext = os.path.splitext(file)
    with tempfile.NamedTemporaryFile(suffix=ext) as tmp:
        shutil.copy(file, tmp)
        if platform == "linux" or platform == "linux2":
            print "==== Copied %s to %s ===" % (file, tmp.name)
            subprocess.call(["cat", tmp.name])
        elif platform == "darwin":
            os.system("open " + tmp.name)
        elif platform == "win32":
            os.system("start " + tmp.name)
