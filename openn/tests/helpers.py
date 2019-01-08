# -*- coding: utf-8 -*-

import os
import shutil
import tempfile
import subprocess
import logging
from pprint import PrettyPrinter
from sys import platform


from openn.models import Document
from openn.curated.membership_manager import MembershipManager
import openn.openn_functions as opfunc

def ensure_file(file_path):
    opfunc.mkdir_p(os.path.dirname(file_path))
    touch(file_path)

def touch(filename, times=None):
    with(open(filename, 'a')):
        os.utime(filename, times)

def pp(thing):
    pprinter = PrettyPrinter(indent=2)
    pprinter.pprint(thing)

def save_and_open(file):
    """ Copy file to a temp location and open it using the Mac os """
    ext = os.path.splitext(file)[1]
    with tempfile.NamedTemporaryFile(suffix=ext) as tmp:
        shutil.copy(file, tmp)
        if platform == "linux" or platform == "linux2":
            print "==== Copied %s to %s ===" % (file, tmp.name)
            subprocess.call(["cat", tmp.name])
        elif platform == "darwin":
            os.system("open " + tmp.name)
        elif platform == "win32":
            os.system("start " + tmp.name)

def cat(file):
    subprocess.call(["cat", file])

def add_to_curated(curated_tag, base_dir='mscodex1223'):
    doc = Document.objects.get(base_dir=base_dir)
    doc.is_online = True
    doc.save()
    MembershipManager().add_document(curated_tag, base_dir)

def format_logging(msgs):
    if msgs is None or msgs == []:
        return ""

    out_msgs = []
    for lvl, msg in msgs:
        out_msgs.append("%s - %s" % (lvl, msg))

    return '\n'.join(out_msgs)

# http://stackoverflow.com/a/20553331
class MockLoggingHandler(logging.Handler):
    """Mock logging handler to check for expected logs.

    Messages are available from an instance's ``messages`` dict, in order, indexed by
    a lowercase log level string (e.g., 'debug', 'info', etc.).
    """

    def __init__(self, *args, **kwargs):
        self.messages = []
        # self.messages = {'debug': [], 'info': [], 'warning': [], 'error': [],
        #                  'critical': []}
        super(MockLoggingHandler, self).__init__(*args, **kwargs)

    def emit(self, record):
        "Store a message from ``record`` in the instance's ``messages`` dict."
        self.acquire()
        try:
            # self.messages[record.levelname.lower()].append(record.getMessage())
            self.messages.append([record.levelname, record.getMessage()])
        finally:
            self.release()

    def reset(self):
        self.acquire()
        try:
            del self.messages[:]
            # for message_list in self.messages.values():
            #     del message_list[:]
        finally:
            self.release()

# Sample from http://stackoverflow.com/a/20553331
#
# import unittest
# import logging
# import foo
#
# class TestFoo(unittest.TestCase):
#
#     @classmethod
#     def setUpClass(cls):
#         super(TestFoo, cls).setUpClass()
#         # Assuming you follow Python's logging module's documentation's
#         # recommendation about naming your module's logs after the module's
#         # __name__,the following getLogger call should fetch the same logger
#         # you use in the foo module
#         foo_log = logging.getLogger(foo.__name__)
#         cls._foo_log_handler = MockLoggingHandler(level='DEBUG')
#         foo_log.addHandler(cls.foo_log_handler)
#         cls.foo_log_messages = cls._foo_log_handler.messages
#
#     def setUp(self):
#         super(TestFoo, self).setUp()
#         self._foo_log_handler.reset() # So each test is independent
#
#     def test_foo_objects_fromble_nicely(self):
#         # Do a bunch of frombling with foo objects
#         # Now check that they've logged 5 frombling messages at the INFO level
#         self.assertEqual(len(self.foo_log_messages['info']), 5)
#         for info_message in self.foo_log_messages['info']:
#             self.assertIn('fromble', info_message)
