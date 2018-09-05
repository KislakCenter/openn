# -*- coding: utf-8 -*-
import time
import os
import errno
import re
import sys
import traceback
import gc
from datetime import datetime
import pytz
import string

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

def safe_isoformat(dtime):
    """ Return the ISO format date if dtime is an instance of datetime; else
        return dtime as a string.
    """
    return dtime.isoformat() if isinstance(dtime, datetime) else str(dtime)

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

def mtime_to_datetime(path):
    """ Get the path mtime and make it time-zone aware if possible. """
    stamp = os.path.getmtime(path)
    return timestamp_to_datetime(stamp)

def ctime_to_datetime(path):
    """ Get the path mtime and make it time-zone aware if possible. """
    stamp = os.path.getctime(path)
    return timestamp_to_datetime(stamp)

def atime_to_datetime(path):
    """ Get the path atime and make it time-zone aware if possible. """
    stamp = os.path.getatime(path)
    return timestamp_to_datetime(stamp)

def timestamp_to_datetime(stamp):
    """ Convert the given timestamp to time-zone aware date if possible;
    otherwise, return naive date.  """
    naive = datetime.utcfromtimestamp(stamp)

    try:
        tzone = pytz.timezone(op_app.TIME_ZONE)
        return tzone.localize(naive)
    except AttributeError:
        return naive

def localize_datetime(dtime):
    try:
        tzone = pytz.timezone(op_app.TIME_ZONE)
    except AttributeError:
        return dtime

    if dtime.tzinfo is None:
        return tzone.localize(dtime)
    else:
        return dtime.astimezone(tzone)

TITLE_SORT_RE = re.compile(r'^\s*(A|An|The)\s+', flags=re.IGNORECASE)

def sort_value(s):
    return TITLE_SORT_RE.sub('', s)

# query formatted string:
# taken from here:
#
#  http://www.trueblade.com/techblog/python-how-to-tell-if-a-format-string-contains-a-given-variable

class AnyFormatSpec(object):
    """ Rerturn any format; prevents breaking on weird formats. """
    def __format__(self, fmt):
        return ''

class QueryFormatter(string.Formatter):
    """ Sublcass of string.Formatter that we can query to see what keys are used. """
    def __init__(self):
        self.used = set()
    def get_value(self, key, args, kwargs):
        self.used.add(key)
        return AnyFormatSpec()

def is_used(var, format_string):
    """ Return true if var is found in format_string. """
    formatter = QueryFormatter()
    formatter.format(format_string)
    return var in formatter.used
