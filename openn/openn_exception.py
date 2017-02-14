# -*- coding: utf-8 -*-
import traceback

class OPennException(Exception):
    def __init__(self, message, cause=None, cause_text=None):
        if cause is None:
            super(OPennException, self).__init__(message)
        else:
            super(OPennException, self).__init__(message + u', caused by ' + repr(cause))
        self.cause = cause
        self.cause_text = cause_text

    def print_cause(self):
        print self.cause_text

class InvalidOptionsException(OPennException):
    """ Exception for invalid script options """
    def __init__(self, *args, **kwargs):
        super(InvalidOptionsException, self).__init__(*args, **kwargs)
