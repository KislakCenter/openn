# -*- coding: utf-8 -*-
import time
import os
import errno
import re
import sys
import traceback

from openn.openn_exception import OPennException
from openn.collections.configs import Configs
import openn.app as op_app

def get_class(kls):
    parts = kls.split('.')
    module = ".".join(parts[:-1])
    m = __import__( module )
    for comp in parts[1:]:
        m = getattr(m, comp)
    return m

def print_exc():
    exc_type, exc_value, exc_traceback = sys.exc_info()
    traceback.print_exception(exc_type, exc_value, exc_traceback,
                              file=sys.stdout)

def get_by_key(dicts, key_name, key_value):
    """From a list of list of dicts, get the all dicts with value ==
key_value for key == key_name.

    Arguments:
    - `dicts`: a list of dicts
    - `key_name`:  the name of the dictionary key
    - `key_value`: the value of the key

    """
    return [ x for x in dicts if x.get(key_name, None) == key_value ]

def tstamp():
    return time.strftime('%Y%m%dT%H%M%S')

def str_time():
    return time.strftime('%Y-%m-%dT%H:%M:%S')

def print_message(level, cmd, str):
    cmd_box = '[{0}]'.format(cmd)
    print "%-23s %-20s %-43s %s" % (cmd_box,str_time(),level,str)

def message(cmd, str):
    print_message('INFO', cmd, str)

def warning(cmd, str):
    print_message('WARNING', cmd, str)

def error_no_exit(cmd, str):
    print_message('ERROR', cmd, str)

def tstamptz():
    return time.strftime('%Y%m%dT%H%M%S%z', time.localtime())

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as ex:
        if ex.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

def sort_str(s):
    """Remove 'the ', 'a ', 'an ' from the begining of strings for purpose
    of alphabetization."""
    return re.sub(r'^(the|an?) +', '', s.lower())

def prep_config_tags():
    return op_app.PREP_CONFIGS.keys()

def get_coll_configs():
    return Configs(op_app.COLLECTIONS)

def get_coll_tags():
    return get_coll_configs().tags()

def get_coll_names():
    return get_coll_configs().all_values('name')

def get_coll_config(tag):
    return get_coll_configs().get_config(tag)

def get_coll_wrapper(tag):
    return get_coll_configs().get_collection(tag)
