# -*- coding: utf-8 -*-
import time
import os
import errno
import re
import sys
import traceback
import gc

from openn.openn_exception import OPennException
from openn.repository.configs import Configs
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

def get_repo_configs():
    return Configs(op_app.REPOSITORIES)

def get_repo_tags():
    return get_repo_configs().tags()

def get_repo_names():
    return get_repo_configs().all_values('name')

def get_repo_config(tag):
    return get_repo_configs().get_config_dict(tag)

def get_repo_wrapper(tag):
    return get_repo_configs().get_repository(tag)

def queryset_iterator(queryset, chunksize=1000):
    """
    From: https://djangosnippets.org/snippets/1949/

    Iterate over a Django Queryset ordered by the primary key

    This method loads a maximum of chunksize (default: 1000) rows in it's
    memory at the same time while django normally would load all rows in it's
    memory. Using the iterator() method only causes it to not preload all the
    classes.

    Usage:

        my_queryset = queryset_iterator(MyItem.objects.all())
        for item in my_queryset:
            item.do_something()

    Note that the implementation of the iterator does not support ordered query sets.
    """

    # Don't break if the queryset is empty
    if queryset.count() == 0:
        return

    pk = 0
    last_pk = queryset.order_by('-pk')[0].pk
    queryset = queryset.order_by('pk')
    while pk < last_pk:
        for row in queryset.filter(pk__gt=pk)[:chunksize]:
            pk = row.pk
            yield row
        gc.collect()

def ensure_dir(dir_path):
    parent = os.path.dirname(dir_path)
    if not os.path.exists(parent):
        ensure_dir(parent)
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
        os.chmod(dir_path, 0775)